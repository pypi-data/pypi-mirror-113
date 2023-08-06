import torch
import torch.nn as nn
import numpy as np
import math


class hd_rp_encoder(nn.Module):
    def __init__(self, size_in, D=5000, p=0.5, quantize = True):
        super().__init__()
        self.dim = D
        self.quantize = quantize
        probs = torch.ones((size_in, D)) * p
        projection = 2 * torch.bernoulli(probs) - 1
        rand_proj = torch.rand(size = (size_in, D))
        projection = torch.where(rand_proj > 0.5, 1, -1).type(torch.float)
        self.hdweights = nn.Parameter(projection, requires_grad=False)
        self.flat = nn.Flatten()
        self.tan_actvn = nn.Tanh()
  
    def forward(self, x):
        x = self.flat(x)
        out = torch.matmul(x, self.hdweights.detach())
        
        if self.quantize:
            out = torch.sign(out)
        else:
            if self.training:
                out = self.tan_actvn(out)
            else:
                out = torch.sign(out)

        return out

class hd_rp_channel_encoder(nn.Module):
    def __init__(self, size_in, D=5000, p = 0.5, quantize = True):
        super().__init__()
        self.dim = D
        self.quantize = quantize
        self.h, self.w = size_in
    
        probs = torch.ones((self.w, D)) * p
        projection = 2 * torch.bernoulli(probs) - 1
        self.hdweights = nn.Parameter(projection, requires_grad = False)
        self.tan_actvn = nn.Tanh()

    def forward(self, x):
        out = torch.matmul(x, self.hdweights.detach())
        out = torch.sum(out, dim = 1)

        if self.quantize:
            out = torch.sign(out)
        else:
            if self.training:
                out = self.tan_actvn(out)
            else:
                out = torch.sign(out)

        return out

class hdsign(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input_):
        ctx.save_for_backward(input_)
        return torch.sign(input_)
    
    @staticmethod
    def backward(ctx, grad_output):
        input_, = ctx.saved_tensors
        grad_input = grad_output.clone()
        ret = grad_input * (1 - torch.square(torch.tanh(input_)))

        return ret


class pact_actvn(torch.autograd.Function):
    '''
    Code for the pact activation was taken from
    https://github.com/KwangHoonAn/PACT
    '''
    @staticmethod
    def forward(ctx, x, alpha, k):
        ctx.save_for_backward(x, alpha)
        #y_1 = 0.5 * (torch.abs(x) - torch.abs(x - alpha) + alpha)
        y = torch.clamp(x, min = 0, max = alpha.item())
        scale = (2 ** k - 1) / alpha
        y_q = torch.round(y * scale) / scale

        return y_q
    
    @staticmethod
    def backward(ctx, dLdy_q):
        # Backward function, I borrowed code from
        # https://github.com/obilaniu/GradOverride/blob/master/functional.py 
        # We get dL / dy_q as a gradient
        x, alpha, = ctx.saved_tensors
        # Weight gradient is only valid when [0, alpha] 
        # Actual gradient for alpha,
        # By applying Chain Rule, we get dL / dy_q * dy_q / dy * dy / dalpha
        # dL / dy_q = argument,  dy_q / dy * dy / dalpha = 0, 1 with x value range 
        lower_bound      = x < 0
        upper_bound      = x > alpha
        # x_range       = 1.0-lower_bound-upper_bound
        x_range = ~(lower_bound|upper_bound)
        grad_alpha = torch.sum(dLdy_q * torch.ge(x, alpha).float()).view(-1)

        return dLdy_q * x_range.float(), grad_alpha, None

class hd_id_lvl_encoder(nn.Module):
    def __init__(self, nfeats, D, qbins = 16, pact=True, k=3, max_val = None, min_val = None, sparsity = 0.5, quant=False):
        super().__init__()
        self.nfeats = nfeats
        self.D = D
        self.pact = pact
        self.quant = quant
        self.k = k - 1
        self.sparsity= sparsity

        if pact:
            self.k = k
            self.alpha = nn.Parameter(torch.tensor(2.0))
            self.maxval = 2 ** k
            self.minval = 0
            self.activn = pact_actvn.apply
        else:
            assert max_val is not None
            assert min_val is not None

            self.maxval = max_val
            self.minval = min_val


        self.bin_len = (self.maxval - self.minval) / qbins
        self.qbins = torch.tensor(qbins)
        intervals = torch.arange(self.minval, self.maxval, self.bin_len)
        self.intervals = nn.Parameter(intervals, requires_grad = False)
        
        #### Generate ID hypervectors
        temp = torch.ones(size=(nfeats, D)) * sparsity
        temp = 2 * torch.bernoulli(temp) - 1
        self.id_hvs = nn.Parameter(temp.type(torch.float), requires_grad = False)

        #### Generate Level hypervector
        lvl_hvs = []
        #temp = [-1]*int(D/2) + [1]*int(D/2)
        temp = [1] * int(D * sparsity) + [-1] * int(D * (1 - sparsity))
        np.random.shuffle(temp)
        lvl_hvs.append(temp)
        change_list = np.arange(0, D)
        np.random.shuffle(change_list)
        cnt_toChange = math.floor(D/2 / (qbins))
        for i in range(1, qbins + 1):
          temp = np.array(lvl_hvs[i-1])
          temp[change_list[(i-1)*cnt_toChange : i*cnt_toChange]] = -temp[change_list[(i-1)*cnt_toChange : i*cnt_toChange]]
          lvl_hvs.append(list(temp))
        lvl_hvs = torch.tensor(lvl_hvs).type(torch.float)
        self.lvl_hvs = nn.Parameter(lvl_hvs, requires_grad = False)
        self.flat = nn.Flatten()
    
    def forward(self, x):
        x = self.flat(x)
        x = x.clamp(self.minval, self.maxval)
        
        if self.pact:
            x = self.activn(x, self.alpha, self.k)

        #idx = torch.floor(x / self.bin_len).type(torch.long)
        idx = torch.searchsorted(self.intervals.detach(), x)
        encoded = (self.lvl_hvs.detach()[idx] * self.id_hvs.detach()).sum(dim=1)
        if self.quant:
            val = torch.tensor(2 ** self.k)
            encoded = torch.clamp(encoded, -val, val-1)
        else:
            encoded = torch.clamp(encoded, -1, 1)
            ones = torch.ones_like(encoded) * self.sparsity
            ones = 2 * torch.bernoulli(ones) - 1
            encoded[encoded == 0] = ones[encoded == 0]
        
        return encoded


class hd_id_lvl_decoder(nn.Module):
    def __init__(self, id_hvs, lvl_hvs, bin_len, min_val, max_val):
        super().__init__()
        self.id_hvs = id_hvs
        self.lvl_hvs = lvl_hvs
        self.bin_len = bin_len
        self.minval = min_val
        self.maxval = max_val
      
    def forward(self, x):
        decoded = x.repeat(1, self.id_hvs.shape[0]).view(x.shape[0], self.id_hvs.shape[0], x.shape[1]) * self.id_hvs.detach()
        decoded = self.minval + torch.matmul(decoded, self.lvl_hvs.detach().transpose(0,1)).max(dim=2)[1] * self.bin_len
            
        return decoded

class hdcodec(nn.Module):
    def __init__(self, nfeats, D, pact=True, k=3, qbins=8, max_val = None, min_val = None, quant=False):
        super().__init__()
        self.encoder = hd_id_lvl_encoder(nfeats, D, qbins, pact, k, max_val, min_val, quant = quant)
        self.decoder = hd_id_lvl_decoder(
            self.encoder.id_hvs, self.encoder.lvl_hvs, self.encoder.bin_len,
            self.encoder.minval, self.encoder.maxval
        )
    
    def forward(self, x):
        out = self.encoder(x)
        out = self.decoder(out)

        return out


class hd_classifier(nn.Module):
    def __init__(self, nclasses, D, alpha = 1.0, clip = False, cdt = False, k = 10, p=0.5):
        super().__init__()
        self.class_hvs = nn.Parameter(torch.zeros(size=(nclasses, D)), requires_grad = False)
        self.nclasses = nclasses
        self.alpha = alpha
        self.oneshot = False
        self.clip = clip
        self.cdt = cdt
        self.D = D
        self.cdt_k = k
        self.p = p
    
    def forward(self, encoded, targets = None):
        scores = torch.matmul(encoded, self.class_hvs.transpose(0, 1))

        with torch.no_grad():
            if not self.oneshot:
                self.oneshot = True
                for label in range(self.nclasses):
                    if label in targets:
                        self.class_hvs[label] += torch.sum(encoded[targets == label], dim = 0, keepdim = True).squeeze()

                return scores

            if targets is None:
                return scores

            if self.training:
                _, preds = scores.max(dim=1)

                for label in range(self.nclasses):
                    incorrect = encoded[torch.bitwise_and(targets != preds, targets == label)]
                    incorrect = incorrect.sum(dim = 0, keepdim = True).squeeze() * self.alpha

                    if self.clip:
                        incorrect = incorrect.clip(-1, 1)

                    self.class_hvs[label] += incorrect * self.alpha #.clip(-1, 1)

                    incorrect = encoded[torch.bitwise_and(targets != preds, preds == label)]
                    incorrect = incorrect.sum(dim = 0, keepdim = True).squeeze()

                    if self.clip:
                        incorrect = incorrect.clip(-1, 1)

                    self.class_hvs[label] -= incorrect * self.alpha #.clip(-1, 1) * self.alpha


                sparsity = torch.sum(self.class_hvs.detach()) / (self.class_hvs[0] * self.class_hvs[1])
                if self.cdt and b_sparsity > self.p:
                    while(sparisty > self.p):
                        perm = torch.randperm(self.D)
                        permuted = incorrect[perm]
                        incorrect += permuted * orig 
                        sparsity = torch.sum(self.class_hvs.detach()) / (self.class_hvs[0] * self.class_hvs[1])

        return scores
    
    def normalize_class_hvs(self):
        for idx in range(self.class_hvs.shape[0]):
            self.class_hvs[idx] /= torch.linalg.norm(self.class_hvs[idx])


class hd_skc_layer(nn.Module):
    def __init__(self, nfeats, D, r, mean = 0.0, std = 1.0):
        super().__init__()
        
        self.nfeats = nfeats
        self.D = D
        self.r = nn.Parameter(torch.tensor(r), requires_grad = False)

        gauss_std = torch.ones(size=(D, nfeats)) * std
        self.prototypes = nn.Parameter(torch.normal(mean = mean, std = gauss_std), requires_grad = False)
        self.flat = nn.Flatten()
    
    def forward(self, x):
        x = self.flat(x)
        encoded = torch.cdist(x, self.prototypes.detach(), p = 2)
        encoded = torch.where(encoded > self.r, 1, -1).type(torch.float)

        return encoded

if __name__ == '__main__':
  testdata = torch.tensor([[0, 4, 1, 3, 0]]).cuda()
  model = hdcodec(nfeats=5, D=10000, qbins = 9)
  model.cuda()
  out = model(testdata)
  print(testdata, out)

  model = hdcodec(nfeats=5, D=10000, pact=False, qbins = 8, max_val = 8, min_val = 0)
  model.cuda()
  out = model(testdata)
  print(testdata, out)

  testdata = torch.rand(size = (100, 13, 81))
  model = hd_rp_channel_encoder(size_in = (13, 81))
  out = model(testdata)
  print(out.shape)
