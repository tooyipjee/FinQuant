import pandas as pd
from datetime import datetime
import numpy as np 
import math
portfolio_name='ftse25sharpeRatio'
optPfBacktest= (pd.read_csv('../portfolio/backtest_'+portfolio_name+'.csv')).to_numpy()

initialHolding=optPfBacktest[:,1]*optPfBacktest[:,2]
finalHolding=optPfBacktest[:,1]*optPfBacktest[:,3]
totalProfit=optPfBacktest[:,4].sum()
profitRate = finalHolding.sum()/initialHolding.sum()
duration_list=[]
for i in range(0,len(optPfBacktest)):
    duration_list.append([ datetime.strptime(optPfBacktest[i,6], '%m/%d/%Y') - datetime.strptime(optPfBacktest[i,5], '%m/%d/%Y')])
    duration_list[i]=duration_list[i][0].days
avgDuration=sum(duration_list)/len(duration_list)
yearsPassed=avgDuration/365
annulRate=np.e**((1/yearsPassed)*np.log(profitRate))