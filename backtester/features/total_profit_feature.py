from backtester.features.feature import Feature
import pandas as pd
import numpy as np

class TotalProfitFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        pnlKey = 'pnl'
        if 'pnlKey' in featureParams:
            pnlKey = featureParams['pnlKey']
        prevData = instrumentLookbackData.getFeatureDf(featureKey)
        pnlData = instrumentLookbackData.getFeatureDf(pnlKey)
        prevData = prevData.replace([np.nan, np.inf, -np.inf], 0)
        pnlData = pnlData.replace([np.nan, np.inf, -np.inf], 0)
        
        if len(prevData) <= 1:
            totalProfit = pd.Series([0] * len(pnlData.columns), index=pnlData.columns)
            prevPnl = pd.Series([0] * len(pnlData.columns), index=pnlData.columns)
        else:
            totalProfit = prevData.iloc[-1]
            prevPnl = pnlData.iloc[-2]
        
        if prevData.empty or pnlData.empty:
        		return totalProfit
        
        pnl = pnlData.iloc[-1] - prevPnl
        totalProfit[pnl > 0] = totalProfit + pnl
        return totalProfit
        
              
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        lookbackDataDf = lookbackDataDf.replace([np.nan, np.inf, -np.inf], 0)
        if lookbackDataDf.empty:
        		return np.float64(0.0)
        pnlKey = 'pnl'
        if 'pnlKey' in featureParams:
            pnlKey = featureParams['pnlKey']
        if len(lookbackDataDf) <= 1:
            prevData = 0
            prevPnl = 0
        else:
            prevData = lookbackDataDf[featureKey].iloc[-2]
            prevPnl = lookbackDataDf[pnlKey].iloc[-2]
        
        totalProfit = prevData
        pnl = lookbackDataDf[pnlKey].iloc[-1] - prevPnl

        if (pnl > 0):
            totalProfit += pnl
        return totalProfit

