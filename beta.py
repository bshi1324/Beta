# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 16:09:26 2017

@author: bshi1_000
"""
from datetime import date
from dateutil.relativedelta import relativedelta
from pandas_datareader.data import DataReader
from pandas_datareader._utils import RemoteDataError
import numpy as np
import pandas as pd
import pickle


def get_beta(stock):
    today = date.today()
    start = today - relativedelta(years=3)
    dfb = DataReader('^GSPC','yahoo',start,today)
    rbts = dfb.resample('M').last()
    
    try:
        df = DataReader(stock,'yahoo',start,today)
        
        
        # create a time-series of monthly data points
        rts = df.resample('M').last()
    
        dfsm = pd.DataFrame({'s_adjclose' : rts['Adj Close'],
                                  'b_adjclose' : rbts['Adj Close']},
                                  index=rts.index)
            
        # compute return
        dfsm[['s_returns','b_returns']] = dfsm[['s_adjclose','b_adjclose']]/\
                dfsm[['s_adjclose','b_adjclose']].shift(1) -1
        dfsm = dfsm.dropna()
        covmat = np.cov(dfsm["s_returns"],dfsm["b_returns"])
            
        # calculate measures now
        beta = covmat[0,1]/covmat[1,1]
        
        return beta
            
    except RemoteDataError:
        beta = np.NaN
        return beta
    
def dct_beta(stocks):
    beta_dct = {stock:get_beta(stock) for stock in stocks}
    
    return beta_dct

def main_beta(stocks):
    beta_dct = dct_beta(stocks)
    beta_lst = ['CASH']
    for key, value in beta_dct.items():
        if value < 1.75 and value >=1.1:
            beta_lst.append(key)
        else:
            pass
    return beta_lst

stocks_consider = ['AAPL','ABBV','ABT','ACN','AEP','AIG','ALL',
    'AMGN','AMZN','APA','APC','AXP','BA','BAC','BAX','BK','BMY','BRKB','C',
    'CAT','CL','CMCSA','COF','COP','COST','CSCO','CVS','CVX','DD','DIS','DOW',
    'DVN','EBAY','EMC','EMR','EXC','F','FB','FCX','FDX','FOXA','GD','GE',
    'GILD','GM','GOOGL','GS','HAL','HD','HON','HPQ','IBM','INTC','JNJ','JPM',
    'KO','LLY','LMT','LOW','MA','MCD','MDLZ','MDT','MET','MMM','MO','MON',
    'MRK','MS','MSFT','NKE','NOV','NSC','ORCL','OXY','PEP','PFE','PG','PM',
    'QCOM','RTN','SBUX','SLB','SO','SPG','T','TGT','TWX','TXN','UNH','UNP',
    'UPS','USB','UTX','V','VZ','WAG','WFC','WMT','XOM']

inter_lst = main_beta(stocks_consider)
with open('beta_lst.pickle', 'wb') as fpw:
    pickle.dump(inter_lst, fpw)
    

    

    