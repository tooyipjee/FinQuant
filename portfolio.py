# # Building a portfolio with data from `quandl`/`yfinance`
# ## Building a portfolio with `build_portfolio()` by downloading relevant data through `quandl`/`yfinance` with stock names, start and end date and column labels
# This example only focuses on how to use `build_portfolio()` to get an instance of `Portfolio` by providing minimal information that is passed on to `quandl`/`yfinance`. For a more exhaustive description of this package and example, please try `Example-Analysis` and `Example-Optimisation`.

import pandas as pd
import datetime
# importing some custom functions/objects
from finquant.portfolio import build_portfolio
years=5

pf_allocation = pd.read_csv('portfolio.csv')
names = pf_allocation["Name"].values.tolist()
start_date = datetime.datetime.now() - datetime.timedelta(days=years*365)
pf = build_portfolio(
    names=names, pf_allocation=pf_allocation, start_date=start_date, data_api="yfinance")

# ## Portfolio is successfully built
# print(pf.portfolio)
# print(pf.data.head(3))
# print(pf)
pf.properties()
stockList = list()
for i in pf.stocks.keys():
    stockList.append(i)
    
from finquant.moving_average import compute_ma, ema
for j in range(0,len(stockList)):
    dis = pf.get_stock(stockList[j]).data.copy(deep=True)
    spans = [7, 30, 180]
    # computing and visualising a band of moving averages
    ma = compute_ma(dis, ema, spans, plot=True)
    pf.get_stock(stockList[j]).properties()
    #print(ma.tail())
    
# Monte Carlo optimisation
opt_w, opt_res = pf.mc_optimisation(num_trials=500)
#Uncomment the code below to visualise EF (ER vs Volatility)
"""
pf.mc_plot_results()
# minimisation to compute efficient frontier and optimal portfolios along it
pf.ef_plot_efrontier()
pf.ef.plot_optimal_portfolios()
# plotting individual stocks
pf.plot_stocks()
pf.mc_properties()

"""
