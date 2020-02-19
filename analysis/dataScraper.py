import yfinance as yf
import pandas as pd
import datetime
import numpy as np
today = datetime.datetime.now()
today = today.strftime("%Y-%m-%d")
portfolio_name='snp500_10-2'
pf_allocation = pd.read_csv('../portfolio/'+portfolio_name+'.csv')
names = pf_allocation["Name"].values.tolist()
data = yf.download(names, start="2015-01-01", end=today)

pfData = data['Adj Close']
pfData.to_csv('../portfolio/stockData/stockData_' + portfolio_name + '.csv')
  