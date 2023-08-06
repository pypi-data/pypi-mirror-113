# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 10:22:59 2020

@author: yuanq
"""

import dd8
import dd8.utility.utils as utils
import dd8.finance.quant as quant

logger = utils.get_basic_logger(__name__, dd8.LOG_PRINT_LEVEL, dd8.LOG_WRITE_LEVEL)

class Dividend(quant.Schedule):
    """
    Each instance represents one dividend schdule with ex-div dates, payment
    dates, currency and amount.
    
    Attributes
    ----------
    npa_ex_dates : np.ndarray
        ex-dividend dates in chronological order
    npa_amount : np.ndarray
        dividend amount of the corresponding ex-dividend dates
    """
    def __init__(self, npa_ex_dates, npa_amount):
        super().__init__(npa_ex_dates, npa_amount)
        
    def is_ex_date(self, dte_to_check):
        return dte_to_check in self.dates
    
    def get_div_yield(self, dte_as_at = None):
        pass
    
    def get_div_pv(self, dte_as_at = None):
        pass
    
class Equity(quant.Underlying):
    """
    Each instance represents one equity secruity.
    
    Parameters
    ----------
    str_bloomberg_symbol : str
        bloomberg ticker (e.g. AAPL UQ) 
    """
    def __init__(self, str_bloomberg_symbol):
        super().__init__(str_bloomberg_symbol)
    
    def from_csv(self, str_file_path):
        pass
    
    @property
    def currency(self):
        return self.__str_currency
    
    @currency.setter
    def currency(self, str_currency):
        self.__str_currency = str_currency
        
    @property
    def isin(self):
       return self.__str_isin
   
    @isin.setter
    def isin(self, str_isin):
        self.__str_isin = str_isin
        
    @property
    def name(self):
        return self.__str_name
    
    @name.setter
    def name(self, str_name):
        self.__str_name = str_name
        
    @property
    def description(self):
        return self.__str_description
    
    @description.setter
    def description(self, str_description):
        self.__str_description = str_description
        
    @property
    def round_lot_size(self):
        return self.__int_round_lot_size
    
    @round_lot_size.setter
    def round_lot_size(self, int_round_lot_size):
        self.__int_round_lot_size = int_round_lot_size
        
    @property
    def market_status(self):
        return self.__str_market_status
    
    @market_status.setter
    def market_status(self, str_market_status):
        self.__str_market_status = str_market_status
        
    @property
    def dividend_ex_date(self):
        return self.__dte_dividend_ex_date
    
    @dividend_ex_date.setter
    def dividend_ex_date(self, dte_dividend_ex_date):
        self.__dte_dividend_ex_date = dte_dividend_ex_date
        
    @property
    def expected_report_datetime(self):
        return self.__dte_expected_report_datetime
    
    @expected_report_datetime.setter
    def expected_report_datetime(self, dte_expected_report_datetime):
        self.__dte_expected_report_datetime = dte_expected_report_datetime
        
    @property
    def reference_tick_size(self):
        return self.__dbl_reference_tick_size
        
    @reference_tick_size.setter
    def reference_tick_size(self, dbl_reference_tick_size):
        self.__dbl_reference_tick_size = dbl_reference_tick_size