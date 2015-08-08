from collections import Callable
from itertools import product
class Function:
    def __init__(self, function):
        self.function = function
        if isinstance(function, Function):
            self.function_name = function.function_name
        else :
            self.function_name = getattr(getattr(function,'__code__',None),'co_name','function')

        
    def __repr__(self):
        try :
            return "{0}:\n\t{0}(0)={1}\n\t{0}(1)={2}".format(self.function_name,
                                                      self.function(0), self.function(1))
        except:
            return repr(self.function)
        
    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)
    
    def __add__(self, other):
        if isinstance(other, Callable):
            return Function(lambda *args, **kwargs: \
                            self(*args , **kwargs) + other(*args, **kwargs))
        else :
            return Function(lambda *args, **kwargs: self(*args, **kwargs) + other)

    def __mul__(self, other):
        if isinstance(other, Callable):
            return Function(lambda *args, **kwargs: self(other(*args, **kwargs)))
        else :
            return Function(lambda *args, **kwargs: self(*args, **kwargs) * other)
        
    def __rmul__(self, other):
        if isinstance(other, Callable):
            return Function(lambda *args, **kwargs: other(self(*args, **kwargs)))
        else :
            return Function(lambda *args, **kwargs: self(*args, **kwargs) * other)

    def __pow__(self, power):
        res = Function(self.function)
        for _ in range(power - 1):
            res = res * Function(self.function)
        return res

@Function
def identity(*args):
    arg, *_ = args
    return arg 

@Function
def combine(*functions):
    def combined_function(*args):
        return sum(function(arg) for function, arg in zip(functions, args))
    return combined_function

class Range:
    def __init__(self, rng, *functions):
        self.range = rng
        self.functions = functions
    
    def _repr_html_(self):
        from pandas import DataFrame
        data = [[func(i) for func in self.functions] for i in self.range]
        columns = [Function(func).function_name for func in self.functions]
        return DataFrame(data, index = self.range, columns=columns)._repr_html_()

class Matrix:
    def __init__(self, ranges = [], functions = []):
        self.ranges = ranges
        self.functions = functions
        
    def _repr_html_(self):
        from pandas import DataFrame
        data = [[func(*items) for func in self.functions]
                               for items in product(*self.ranges)]
        columns = [Function(func).function_name for func in self.functions]
        return DataFrame(data, columns=columns,index=product(*self.ranges))._repr_html_()
