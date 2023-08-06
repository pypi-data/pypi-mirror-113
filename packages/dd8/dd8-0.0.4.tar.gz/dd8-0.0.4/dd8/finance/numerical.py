# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 18:37:40 2020

@author: yuanq
"""

import numpy as np

import dd8
import dd8.utility.utils as utils
import dd8.finance.enums as enums

logger = utils.get_basic_logger(__name__, 
                                dd8.LOG_PRINT_LEVEL, 
                                dd8.LOG_WRITE_LEVEL)

class Differentiate(object):
    """
    Compute the derivative of f
    
    Parameters
    ----------
    f : object
        function of one variable
    x : double
        point at which to compute derivative
    step : double
        step size in difference formula
    method : ENUM_DERIVATIVE_METHOD
        enum to determine difference formula: CENTRAL, FORWARD, BACKWARD
        
    Returns
    -------
    float
        Difference formula:
            ENUM_DERIVATIVE_METHOD.CENTRAL:  [f(x+step)-f(x-step)]/(2*step)
            ENUM_DERIVATIVE_METHOD.FORWARD:  [f(x+step)-f(x)]/(step)
            ENUM_DERIVATIVE_METHOD.BACKWARD: [f(x)-f(x-step)]/(step)
            
    Raises
    ------
    ValueError
        when an invalid method enum is passed to function
        
    Source(s)
    ---------
    [1] http://www.math.ubc.ca/~pwalls/math-python/differentiation/    
    """
    def __init__(self, method):
        self.method = method
        
    @property
    def method(self):
        return self.__enum_derivative_method
    
    @property
    def method(self, enum_derivative_method):
        self.__enum_derivative_method = enum_derivative_method
    
    def fit(self, func, x, step):
        if self.method == enums.ENUM_DERIVATIVE_METHOD.CENTRAL:
            return (func(x+step) - func(x-step)) / (2*step)
        elif self.method == enums.ENUM_DERIVATIVE_METHOD.FORWARD:
            return (func(x+step) - func(x)) / (step)
        elif self.method == enums.ENUM_DERIVATIVE_METHOD.BACKWARD:
            return (func(x) - func(x-step)) / (step)
            

# def incremental_search(obj_func, dbl_start, dbl_end, dbl_dx):
#     initial_x = dbl_start
#     initial_y  = obj_func(initial_x)
#     next_x = initial + dbl_dx
#     next_y = obj_func(next_x)
#     counter = 1
#     while np.sign(initial_y) == np.sign(next_y):
#         if initial_x >= dbl_end:
#             return initial_x - dbl_dx, counter
        
#         initial_x = next_x
#         initial_y = next_y
#         next_x = nex