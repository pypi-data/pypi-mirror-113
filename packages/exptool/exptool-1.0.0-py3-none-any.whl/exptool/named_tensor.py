import numpy as np
import pandas as pd

class NamedTensor:
    """
    A NamedTensor class, based on numpy.ndarray. In a NamedTensor object, each dim was named, and each value of each
     dim was aslo named. the object support the fundamental calculating, including mean,sum,max,min along an given axis,
     and +,-,*,/ with another NamedTensor or number, the definition of the operator was the same as them in numpy.adarray.
     We also provided apply() function, for flexible summary along a given axis.
    """
    def __init__(self,data:np.ndarray=None,index_name:list=None,index:dict=None):
        """
        data: ndarray
        index_name: list of str
        index: dict from index_name to list of index_values.
        """

        if(index is not None and index_name is None):
            index_name=list(index.keys())

        if(index_name is not None and
                data is not None and
                index is None):
            index=dict([(name,list(range(sp))) for sp,name in zip(data.shape,index_name)])

        if(data is None and index_name is not None and index is not None):
            shape=[len(index[e]) for e in index_name]
            data=np.zeros(shape,dtype=np.float)

        for e,en in zip([data, index_name, index],["data", "index_name", "index"]):
            if(e is None):
                raise RuntimeError(f"The parameter {en} was None, but we can not deduce it.")

        self.data=data
        self.set_index(index_name,index)
        self.shape=data.shape

    def set_index(self,index_name:list,index:dict):
        for i,dim_name in enumerate(index_name):
            if(len(index[dim_name])!=self.data.shape[i]):
                raise RuntimeError(f"the length of {dim_name} dim is not equal to its named index, if the index_name was passed into the init function,"
                                   f"you may need to check the order defined by index_name, if the index_name was not pased into the init function, the shape of"
                                   f"your ndarray data and the index may be mismatach, please check it.")
        self.index=index
        self.index_name=list(index_name)
        self.rindex=dict()
        for dim_name,dim_value in index.items():
            self.rindex[dim_name]=dict([(e,i) for i,e in enumerate(dim_value)])

    def __add__(self, other):
        if(isinstance(other,NamedTensor)):
            resdata=self.data+other.data
        else:
            resdata = self.data + other
        return NamedTensor(resdata,self.index_name,self.index)

    def __sub__(self, other):
        if (isinstance(other, NamedTensor)):
            resdata = self.data - other.data
        else:
            resdata = self.data - other
        return NamedTensor(resdata, self.index_name, self.index)

    def __truediv__(self, other):
        if (isinstance(other, NamedTensor)):
            resdata = self.data / other.data
        else:
            resdata = self.data / other
        return NamedTensor(resdata, self.index_name, self.index)

    def __mul__(self, other):
        if (isinstance(other, NamedTensor)):
            resdata = self.data * other.data
        else:
            resdata = self.data * other
        return NamedTensor(resdata, self.index_name, self.index)

    def _apply(self, func, axis=None):
        if (axis is None):
            axis = self.index_name[-1]

        axis = self.index_name.index(axis)
        resindex = self.index_name[:axis] + self.index_name[axis + 1:]
        resdata=func(ax=axis)
        return NamedTensor(
            resdata, index_name=resindex,
            index=dict([(e, self.index[e]) for e in resindex])
        )

    def min(self,axis=None):
        fun = lambda ax: np.min(a=self.data,axis=ax)
        return self._apply(fun, axis=axis)

    def max(self,axis=None):
        fun = lambda ax: np.max(a=self.data,axis=ax)
        return self._apply(fun, axis=axis)

    def mean(self,axis=None):
        fun = lambda ax: np.mean(a=self.data,axis=ax)
        return self._apply(fun, axis=axis)

    def sum(self,axis=None):
        fun = lambda ax: np.sum(a=self.data,axis=ax)
        return self._apply(fun, axis=axis)

    def apply(self,func,axis=None):
        fun=lambda ax:np.apply_along_axis(func,axis=ax,arr=self.data)
        return self._apply(fun,axis=axis)

    def __repr__(self):
        s=f"index name: {self.index_name}\n"
        for k in self.index_name:
            s+=f"{k}: {self.index[k]}\n"
        s+="----------------------------------"
        s+=self.data.shape.__repr__()
        return s

    def to_numpy(self):
        return self.data

    def to_dataframe(self):
        length=len(self.index_name)
        if(length==0 or length>2):
            raise RuntimeError("the ndim of index_name required was not satisfied, please check.")

        if(length==1):
            return pd.Series(self.data,index=self.index[self.index_name[0]],name=self.index_name[0])

        res=pd.DataFrame(self.data, index=self.index[self.index_name[0]],
                            columns=self.index[self.index_name[1]])
        res.index.name=self.index_name[0]
        res.columns.name=self.index_name[1]
        return pd.DataFrame(self.data, index=self.index[self.index_name[0]],
                            columns=self.index[self.index_name[1]])

    def __getitem__(self, item):
        if(not isinstance(item,tuple)):
            item=(item,)

        if(len(self.index_name)!=len(item)):
            raise RuntimeError(f"the length of item is {len(item)}, but the length of index_name is {len(self.index_name)}."
                               f" they were mismatch")
        index_name=[]
        newitem=[]
        for name,e in zip(self.index,item):
            #the dim match all value
            if(isinstance(e,slice) and e.start is None):
                index_name.append(name)
                newitem.append(e)

            #the dim match a subset
            elif(isinstance(e,list) or isinstance(e,tuple)):
                index_name.append(name)
                newitem.append([self.rindex[name][ee] for ee in e])

            #the dim match single value
            else:
                newitem.append(self.rindex[name][e])

        return NamedTensor( self.data.__getitem__(tuple(newitem)),
                            index_name,
                            dict([(e,self.index[e]) for e in index_name])
                           )
