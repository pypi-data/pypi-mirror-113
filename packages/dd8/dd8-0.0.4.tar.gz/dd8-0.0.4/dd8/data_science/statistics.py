# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 18:39:27 2021

@author: LIM YUAN QING
"""

class Statistics(object):
    def __init__(self):
        pass
    
    def fit(self, X):
        pass
    
class StandardDeviation(Statistics):
    def __init__(self):
        self.value = None
    
    def fit(self, X):
        self.value = X.std()
        return self.value
    
    @property
    def value(self):
        return self.__dbl_value
    
    @value.setter
    def value(self, dbl_value):
        self.__dbl_value = dbl_value
        

        
        
if __name__ == '__main__':
    import sys
    sys.path.append(r'E:\Program Files\Dropbox\Yuan Qing\Work\Projects\Libraries\3. Python\1. Modules\dd8')

    import dd8.finance.data as data
    
    dataset = data.YahooData('ES=F', '01 Jan 2020', '02 Oct 2020')
    df_data = dataset.df_data
    
    returns = df_data['Adj Close'].diff().values[1:] / df_data['Adj Close'].values[:-1]
    std = StandardDeviation()
    print(std.fit(returns))