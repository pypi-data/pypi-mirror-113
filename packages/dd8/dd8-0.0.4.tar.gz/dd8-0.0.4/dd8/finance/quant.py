# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 22:42:06 2019

@author: LIM YUAN QING
@email: yuanqing87@gmail.com

Classes
-------
Underlying


"""

import numpy as np

import dd8
import dd8.utility.utils as utils

logger = utils.get_basic_logger(__name__, 
                                dd8.LOG_PRINT_LEVEL, 
                                dd8.LOG_WRITE_LEVEL)

class Underlying(object):
    """
    Abstract Base Class to represent an underlying object.
    
    Attributes
    ----------
    uid
    
    """
    
    def __init__(self, str_uid):
        """
        Instantiate an `Underlying` object.
        
        Parameters
        ----------
        str_uid : str
            unique identifier
            
        """
        self.uid = str_uid
        
    @property    
    def uid(self):
        return self.__str_uid
    
    @uid.setter
    def uid(self, str_uid):
        self.__str_uid = str(str_uid)
        
class Schedule(object):
    """
    Abstract Base Class to represent a schedule, where a numerical value, 
    such as interest rate or cashflow, is associated with a particular date. 
    
    Attributes
    ----------
    dates
    values
    uid 
    
    """
    def __init__(self, npa_dates, npa_values, str_uid):   
        """
        Instantiate an `Underlying` object.
        
        Parameters
        ----------
        npa_dates : numpy.ndarray
            dates that correspond to `npa_values`
        npa_values : numpy.ndarray
            numeric values that correspond to `npa_dates`
        str_uid : str
            unique identifier
            
        """
        self.dates = npa_dates
        self.values = npa_values
        self.uid = str_uid
        
    @property
    def dates(self):
        return self.__npa_dates
    
    @dates.setter
    def dates(self, npa_dates):
        self.__npa_dates = np.array(npa_dates)
        
    @property
    def values(self):
        return self.__npa_values
    
    @values.setter
    def values(self, npa_values):
        self.__npa_values = np.array(npa_values)
    
    @property
    def uid(self):
        return self.__str_uid       
    
    @uid.setter
    def uid(self, str_uid):
        self.__str_uid = str(str_uid)