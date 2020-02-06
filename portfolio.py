# # Building a portfolio with data from `quandl`/`yfinance`
# ## Building a portfolio with `build_portfolio()` by downloading relevant data through `quandl`/`yfinance` with stock names, start and end date and column labels
# This example only focuses on how to use `build_portfolio()` to get an instance of `Portfolio` by providing minimal information that is passed on to `quandl`/`yfinance`. For a more exhaustive description of this package and example, please try `Example-Analysis` and `Example-Optimisation`.

import pandas as pd
import datetime

# importing some custom functions/objects
from finquant.portfolio import build_portfolio


d = {
    0: {"Name": "GOOG", "Allocation": 20},
    1: {"Name": "AMZN", "Allocation": 10},
    2: {"Name": "MCD", "Allocation": 15},
    3: {"Name": "DIS", "Allocation": 18},
}
pf_allocation = pd.DataFrame.from_dict(d, orient="index")

# ### User friendly interface to quandl/yfinance
# As mentioned above, in this example `build_portfolio()` is used to build a portfolio by performing a query to `quandl`/`yfinance`.
#
# To download Google's stock data, `quandl` requires the string `"WIKI/GOOG"`. For simplicity, `FinQuant` facilitates a set of functions under the hood to sort out lots of specific commands/required input for `quandl`/`yfinance`. When using `FinQuant`, the user simply needs to provide a list of stock names/tickers. Moreover, the leading `"WIKI/"` in `quandl`'s request can be set by the user or not.
#
# For example, if using `quandl` as a data source (default), all three lists of tickers/names as shown below are valid input for
# `FinQuant`'s function `build_portfolio(names=names)`:
#  * `names = ['WIKI/GOOG', 'WIKI/AMZN']`
#  * `names = ['GOOG', 'AMZN']`
#  * `names = ['WIKI/GOOG', 'AMZN']`
#
# If using `yfinance` as a data source, `FinQuant`'s function `build_portfolio(names=names)` expects the stock names to be without any leading/trailing string:
#  * `names = ['GOOG', 'AMZN']`
#
# By default, `FinQuant` uses `quandl` to obtain stock price data. The function `build_portfolio()` can be called with the optional argument `data_api` to use `yfinance` instead:
#  * `build_portfolio(names=names, data_api="yfinance")`
#
# In the below example we are using the default option, `quandl`.

# here we set the list of names based on the names in
# the DataFrame pf_allocation
names = pf_allocation["Name"].values.tolist()

# dates can be set as datetime or string, as shown below:
start_date = datetime.datetime(2015, 1, 1)

# While quandl/yfinance will download lots of different prices for each stock,
# e.g. high, low, close, etc, FinQuant will extract the column "Adj. Close" ("Adj Close" if using yfinance).

pf = build_portfolio(
    names=names, pf_allocation=pf_allocation, start_date=start_date, data_api="yfinance")

# ## Portfolio is successfully built
# Getting data from the portfolio

# the portfolio information DataFrame
print(pf.portfolio)

# the portfolio stock data, prices DataFrame
print(pf.data.head(3))

# print out information and quantities of given portfolio
print(pf)
pf.properties()

# ## Please continue with `Example-Build-Portfolio-from-file.py`.
# As mentioned above, this example only shows how to use `build_portfolio()` to get an instance of `Portfolio` by downloading data thro