# # Building a portfolio with data from `quandl`/`yfinance`
# ## Building a portfolio with `build_portfolio()` by downloading relevant data through `quandl`/`yfinance` with stock names, start and end date and column labels
# This example only focuses on how to use `build_portfolio()` to get an instance of `Portfolio` by providing minimal information that is passed on to `quandl`/`yfinance`. For a more exhaustive description of this package and example, please try `Example-Analysis` and `Example-Optimisation`.

import pandas as pd
import datetime
# importing some custom functions/objects
from finquant.portfolio import build_portfolio
import numpy as np
years=3
yearsAgo=1
no_of_stocks=4
portfolio_name='malaysia'
pf_allocation = pd.read_csv('../portfolio/'+portfolio_name+'.csv')
names = pf_allocation["Name"].values.tolist()
today = datetime.datetime.now()
start_date = today - datetime.timedelta(days=int(years*365))
end_date = today - datetime.timedelta(days=int(yearsAgo*365))
pf = build_portfolio(
    names=names, pf_allocation=pf_allocation, start_date=start_date, end_date=end_date, data_api="yfinance")

# Monte Carlo optimisation
opt_w, opt_res = pf.mc_optimisation(num_trials=100)

opt_w_T=(opt_w.T)
opt_w_T=pd.DataFrame.sort_values(opt_w_T, 'Max Sharpe Ratio',ascending=False)

opt_pf_allocation=pd.DataFrame(np.zeros((no_of_stocks, 2))).astype(str)
for i in range(0,no_of_stocks):
    opt_pf_allocation.set_value(i, 0,opt_w_T.index[i])
    opt_pf_allocation.set_value(i, 1,opt_w_T.iloc[i,1])
opt_pf_allocation.columns = ['Name','Allocation']
opt_names = pf_allocation["Name"].values.tolist()
opt_pf = build_portfolio(
    names=opt_names, pf_allocation=opt_pf_allocation, start_date=end_date, data_api="yfinance")
opt_pf_allocation.to_csv('../portfolio/optimal_'+portfolio_name+'.csv',index=False)

backtestPortfolio=np.zeros((no_of_stocks,5)).astype(str)
opt_stockList = np.zeros((len(opt_pf_allocation),1)).astype(str)
opt_allocList = np.zeros((len(opt_pf_allocation),1)).astype(str)
for i in range(0,len(opt_pf_allocation)):
    opt_stockList[i]=opt_pf_allocation.iloc[i,0]
    opt_allocList[i]=opt_pf_allocation.iloc[i,1]

for j in range(0,len(opt_stockList)):
    backtestPortfolio[j,0]=opt_stockList[j][0]
    backtestPortfolio[j,1]=opt_allocList[j][0]
    backtestPortfolio[j,2]=opt_pf.get_stock(opt_stockList[j][0]).data.iloc[0][0]
    backtestPortfolio[j,3]=opt_pf.get_stock(opt_stockList[j][0]).data.iloc[-1][0]
    backtestPortfolio[j,4]=(float(backtestPortfolio[j,3])-float(backtestPortfolio[j,2]))*float(backtestPortfolio[j,1])


# Uncomment the code below to visualise EF (ER vs Volatility)
"""
pf.mc_plot_results()
# minimisation to compute efficient frontier and optimal portfolios along it
pf.ef_plot_efrontier()
pf.ef.plot_optimal_portfolios()
# plotting individual stocks
pf.plot_stocks()
pf.mc_properties()

"""
