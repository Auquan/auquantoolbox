# **Available Features**

Features can be called by specifying config dictionaries. Create one dictionary per feature and return them in a dictionary as market features or instrument features.

Feature config Dictionary has the following keys:
  > *featureId:* a string representing the type of feature you want to use  
  > *featureKey:* {optional} a string representing the key you will use to access the value of this feature  
  >            If not present, will just use featureId  
  > *params:* {optional} A dictionary with which contains other optional params if needed by the feature 


Feature ID  | Parameters | Description
:-------------: | ------------- | -------------  
*moving_average*  | 'featureName', 'period' | calculate moving average of *featureName* over *period* 
*moving_sdev*  | 'featureName', 'period' | calculate moving standard deviation of *featureName* over *period*
*exponential_moving_average*  | 'featureName', 'period' | calculate exp. weighted moving average of *featureName* with *period* as half life 
*momentum*  | 'featureName', 'period' | calculate momentum in *featureName* over *period* as featureValue(now) -  featureValue(now - period)
*bollinger_bands*  | 'featureName', 'period' | upper and lower bollinger bands as average(period) - sdev(period), average(period) + sdev(period)
*macd*  | 'featureName', 'period1', 'period2' | moving average convergence divergence as average(period1) - average(period2)
*ratio*  | 'featureName', 'instrumentId1', 'instrumentId2' | ratio of feature values of instrumentID1 / instrumentID2
*rsi*  | 'featureName', 'period' | Relative Strength Index - ratio of average profits / average losses over period
*vwap*  | - | calculated from book data as *bid price x ask volume + ask price x bid volume / (ask volume + bid volume)*
***fees***  | - |fees to trade, always calculated
***position***  | - | instrument position, always calculated
***pnl***  | - | Profit/Loss, always calculated
***capital***  | -| Spare capital not in use, always calculated
***portfolio_value***  | - | Total value of trading system, always calculated