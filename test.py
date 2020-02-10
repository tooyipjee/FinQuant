

from finquant.portfolio import build_portfolio
names = ['WIKI/GOOG', 'WIKI/AMZN']
pf = build_portfolio(names=names)
pf.properties()

from finquant.moving_average import compute_ma, ema
# get stock data for Disney
dis = pf.get_stock("GOOG").data.copy(deep=True)
spans = [10, 50, 100, 150, 200]
# computing and visualising a band of moving averages
ma = compute_ma(dis, ema, spans, plot=True)
print(ma.tail())