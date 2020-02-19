# # Building a portfolio with data from `quandl`/`yfinance`
# ## Building a portfolio with `build_portfolio()` by downloading relevant data through `quandl`/`yfinance` with stock names, start and end date and column labels
# This example only focuses on how to use `build_portfolio()` to get an instance of `Portfolio` by providing minimal information that is passed on to `quandl`/`yfinance`. For a more exhaustive description of this package and example, please try `Example-Analysis` and `Example-Optimisation`.

import pandas as pd
import datetime
# importing some custom functions/objects
from finquant.portfolio import build_portfolio
import numpy as np 
import math
years=3
yearsAgo=1
no_of_stocks=10
portfolio_name='ftse25sharpeRatioPlus'
pf_allocation = pd.read_csv('../portfolio/'+portfolio_name+'.csv')
names = pf_allocation["Name"].values.tolist()
today = datetime.datetime.now()
start_date = today - datetime.timedelta(days=int(years*365))
end_date = today - datetime.timedelta(days=int(yearsAgo*365))
pf = build_portfolio(
    names=names, pf_allocation=pf_allocation, start_date=start_date, end_date=end_date, data_api="yfinance")

# Monte Carlo optimisation
opt_w, opt_res = pf.mc_optimisation(num_trials=500)

opt_w_T=(opt_w.T)
opt_w_T=pd.DataFrame.sort_values(opt_w_T, 'Max Sharpe Ratio',ascending=False)

opt_pf_allocation=pd.DataFrame(np.zeros((no_of_stocks, 2))).astype(str)
for i in range(0,no_of_stocks):
    opt_pf_allocation.iat[i, 0]=opt_w_T.index[i]
    opt_pf_allocation.iat[i, 1]=opt_w_T.iloc[i,1]

opt_pf_allocation.columns = ['Name','Allocation']
opt_alloc=opt_pf_allocation["Allocation"].values.tolist()
opt_alloc=opt_alloc/sum(opt_alloc)
for i in range(0,no_of_stocks):
    opt_pf_allocation.iat[i, 0]=opt_w_T.index[i]
    opt_pf_allocation.iat[i, 1]=opt_alloc[i]
opt_names = opt_pf_allocation["Name"].values.tolist()

opt_pf = build_portfolio(
    names=opt_names, pf_allocation=opt_pf_allocation, start_date=end_date, data_api="yfinance")
opt_pf_allocation.to_csv('../portfolio/optimal/optimal_'+portfolio_name+'.csv',index=False)

backtestPortfolio=np.zeros((no_of_stocks,7)).astype(str)
opt_stockList = np.zeros((len(opt_pf_allocation),1)).astype(str)
opt_allocList = np.zeros((len(opt_pf_allocation),1)).astype(str)
for i in range(0,len(opt_pf_allocation)):
    opt_stockList[i]=opt_pf_allocation.iloc[i,0]
    opt_allocList[i]=opt_pf_allocation.iloc[i,1]


backtestPortfolio[:,0]=opt_stockList[:,0]
backtestPortfolio[:,1]=opt_allocList[:,0]
for j in range(0,len(opt_stockList)):
    first = 0
    end = -1
    backtestPortfolio[j,2]=opt_pf.get_stock(opt_stockList[j][0]).data.iloc[first][0]
    backtestPortfolio[j,3]=opt_pf.get_stock(opt_stockList[j][0]).data.iloc[end][0]
    while math.isnan(opt_pf.get_stock(opt_stockList[j][0]).data.iloc[first][0]) and opt_pf.get_stock(opt_stockList[j][0]).data.iloc[first][0] < 0:
        first=first+1
        backtestPortfolio[j,2]=opt_pf.get_stock(opt_stockList[j][0]).data.iloc[first][0]
    while (math.isnan(opt_pf.get_stock(opt_stockList[j][0]).data.iloc[end][0]) and (opt_pf.get_stock(opt_stockList[j][0]).data.iloc[first][0]) < 0):
        end=end-1
        backtestPortfolio[j,3]=opt_pf.get_stock(opt_stockList[j][0]).data.iloc[end][0]
    backtestPortfolio[j,5] = (end_date + datetime.timedelta(days=int(first))).strftime("%m/%d/%Y")
    backtestPortfolio[j,6] = (today - datetime.timedelta(days=int(end))).strftime("%m/%d/%Y")
backtestPortfolio[:,4]=(backtestPortfolio[:,3].astype(float)-backtestPortfolio[:,2].astype(float))*backtestPortfolio[:,1].astype(float)
backtestPortfolio=pd.DataFrame(backtestPortfolio)
backtestPortfolio.columns = ['Name','Allocation','Initial','Final','Nett','Initial Date','Final Date']
backtestPortfolio.to_csv('../portfolio/backtest/backtest_'+portfolio_name+'.csv',index=False)

optPfBacktest= (pd.read_csv('../portfolio/backtest/backtest_'+portfolio_name+'.csv')).to_numpy()

initialHolding=optPfBacktest[:,1]*optPfBacktest[:,2]
finalHolding=optPfBacktest[:,1]*optPfBacktest[:,3]
totalProfit=optPfBacktest[:,4].sum()
profitRate = finalHolding.sum()/initialHolding.sum()
duration_list=[]
for i in range(0,len(optPfBacktest)):
    duration_list.append([ datetime.datetime.strptime(optPfBacktest[i,6], '%m/%d/%Y') - datetime.datetime.strptime(optPfBacktest[i,5], '%m/%d/%Y')])
    duration_list[i]=duration_list[i][0].days
avgDuration=sum(duration_list)/len(duration_list)
yearsPassed=avgDuration/365
annulRate=np.e**((1/yearsPassed)*np.log(profitRate))

print("Choosing " + str(no_of_stocks) + " stocks, maximising for SR an optimal pf was computed using MC sim over the period, " + start_date.strftime("%m/%d/%Y") + " till " + end_date.strftime("%m/%d/%Y") + ".")
print("The optimal portfolio, produced an annualised profit rate of " + str(annulRate) + ".")