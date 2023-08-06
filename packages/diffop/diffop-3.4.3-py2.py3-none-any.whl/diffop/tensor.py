"""A module for the common differential operators of vector calculus"""

import cupy as np
from .operators import FinDiff
from .diff import Diff


class TensorOperator(object):
    """Base class for all vector differential operators.
       Shall not be instantiated directly, but through the child classes.
    """
    def __init__(self, **kwargs):
        """Constructor for the VectorOperator base class.
        
            kwargs:
            -------
            
            h       list with the grid spacings of an N-dimensional uniform grid
            
            coords  list of 1D arrays with the coordinate values along the N axes.
                    This is used for non-uniform grids. 
                    
            nablaorder 1 or 2 .,,,scalar

            Either specify "h" or "coords", not both.
        
        """

        if "acc" in kwargs:
            self.acc = kwargs.pop("acc")
        else:
            self.acc = 2

        if "h" in kwargs: # necessary for backward compatibility 0.5.2 => 0.6
            self.judge=0
            self.h = kwargs.pop("h")
            self.ndims = len(self.h)
            self.component=[]
            for i in range(self.ndims):
                self.component.append(FinDiff(i, self.h[i], 1))
                for j in range(self.ndims):
                    self.component.append(FinDiff((i, self.h[i]),(j, self.h[j])))
        if "coords" in kwargs:
            self.judge=1
            self.coords = kwargs.pop("coords")
            self.ndims = len(self.coords)
            self.component=[]
            for i in range(self.ndims):
                self.component.append(FinDiff(i, self.coords[i], 1))
                for j in range(self.ndims):
                    self.component.append(FinDiff((i, self.coords[i]),(j, self.coords[j])))




class Nabla(TensorOperator):
    r"""
    The N-dimensional gradient.
    
    .. math::
        \nabla = \left(\frac{\partial}{\partial x_0}, \frac{\partial}{\partial x_1}, ... , \frac{\partial}{\partial x_{N-1}}\right)

    :param kwargs:  exactly one of *h* and *coords* must be specified
    
             *h* 
                     list with the grid spacings of an N-dimensional uniform grid     
             *coords*
                     list of 1D arrays with the coordinate values along the N axes.
                     This is used for non-uniform grids.
                     
             *acc*
                     accuracy order, must be positive integer, default is 2
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, f):
        """
        Applies the N-dimensional gradient to the array f.
        
        :param f:  ``numpy.ndarray``
        
                Array to apply the gradient to. It represents a scalar function,
                so it must have N axes for the N independent variables.        
           
        :returns: ``numpy.ndarray``
         
                The gradient of f, which has N+1 axes, i.e. it is 
                an array of N arrays of N axes each.
           
        """

        # if not isinstance(f, np.ndarray):
        #     raise TypeError("Function to differentiate must be numpy.ndarray")

        # if len(f.shape) != self.ndims:
        #     raise ValueError("Gradients can only be applied to scalar functions")

        result = []
        for k in range(self.ndims):
            result.append(self.component[k](f, acc=self.acc))

        return np.concatenate((f,np.array(result)),axis=-1)
