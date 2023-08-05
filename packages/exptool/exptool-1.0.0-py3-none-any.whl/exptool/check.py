import torch
from torch import nn
import numpy as np
from typing import Union,List,Tuple
from functools import reduce
from collections import OrderedDict

class TensorChecker:
    """
    检查每层网络的输入和输出的梯度是否正常
    """

    def __init__(self,prefix="",check=True):
        self.check=check
        self.prefix=prefix

    def __call__(self, module:nn.Module, tensor_in, tensor_out):
        if(self.check):
            self.check=False
        else:
            return

        print("################")
        print(module.name)
        print(f"{self.prefix}_in:")
        for e in tensor_in:
            print(e.shape)
        print("----------------")
        print(f"{self.prefix}_out:")
        for e in tensor_in:
            print(e.shape)
        # print("----------------")
        # print(f"{module.__class__}_param:")
        # for a,e in module.named_parameters():
        #     print(a,e.shape)
        print("################")

    def set_state(self,check):
        self.check=check
        return self

    def get_state(self):
        return self.check


T=Tuple[nn.Module,str]
class ModuleWrapper(nn.Module):
    def __init__(self,model, grad_check: Union[T,List[T]] = None,
                 output_check: Union[T,List[T]] = None,params_check=Union[T,List[T]]):

        super(ModuleWrapper,self).__init__()
        self.model=model
        self._grad=[]
        self._output=[]
        self._params_module=OrderedDict()

        if(grad_check is not None):
            if (isinstance(grad_check, tuple)):
                grad_check=[grad_check]
            for e,name in grad_check:
                t=TensorChecker(f"grad_{name}")
                self._grad.append(t)
                e.register_full_backward_hook(t)

        if(output_check is not None):
            if(isinstance(output_check,tuple)):
                output_check=[output_check]
            for e,name in output_check:
                t=TensorChecker(f"output_{name}")
                self._output.append(t)
                e.register_forward_hook(t)

        if(params_check is not None):
            if(isinstance(params_check,tuple)):
                params_check=[params_check]
            for e,name in params_check:
                self._params_module[name]=e

    def forward(self,*args,**kwargs):
        return self.model(*args,**kwargs)

    def grad_check(self):
        for e in self._grad:
            e.set_state(True)

    def output_check(self):
        for e in self._output:
            e.set_state(True)

    def param_check(self):
        print("params check:")
        for name,e in self._params_module.items():
            print("check", name)
            res=dict()
            for param in e.parameters():
                n=param.ndim
                if(n not in res):
                    res[n]=dict(weights=[],stats=[])
                res[n]["weights"].append(reduce(lambda x,y:x*y,param.shape))
                res[n]["stats"].append(self.stat(param.detach().numpy()))

            for n,ans in res.items():
                a = np.stack(ans["stats"])
                w = ans["weights"]
                print(n,"dim: ",np.average(a, axis=0, weights=w))

    def stat(self,param:np.ndarray):
        return np.mean(param), np.median(param), np.max(param), np.min(param),np.std(param)

