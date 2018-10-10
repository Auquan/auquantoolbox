from backtester.features.feature import Feature
import pandas as pd
import numpy as np

class TotalLossFeature(Feature):

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
            totalLoss = pd.Series([0] * len(pnlData.columns), index=pnlData.columns)
            prevPnl = pd.Series([0] * len(pnlData.columns), index=pnlData.columns)
        else:
            totalLoss = prevData.iloc[-1]
            prevPnl = pnlData.iloc[-2]
        if len(pnlData)>=1:
            pnl = pnlData.iloc[-1] - prevPnl
            totalLoss[pnl < 0] = totalLoss + np.abs(pnl)
        return totalLoss

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

        totalLoss = prevData
        if len(lookbackDataDf[pnlKey])>=1:
            pnl = lookbackDataDf[pnlKey].iloc[-1] - prevPnl
            if (pnl < 0):
                totalLoss += np.abs(pnl)
        return totalLoss
