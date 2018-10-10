from backtester.features.feature import Feature
from backtester.logger import *
import pandas as pd
import numpy as np

class CountProfitFeature(Feature):

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
        try:
            if len(prevData) <= 1:
                countProfit = pd.Series([0] * len(pnlData.columns), index=pnlData.columns)
                prevPnl = pd.Series([0] * len(pnlData.columns), index=pnlData.columns)
            else:
                countProfit = prevData.iloc[-1]
                prevPnl = pnlData.iloc[-2]
            pnl = pnlData.iloc[-1] - prevPnl
            countProfit[pnl > 0] = countProfit + 1
            return countProfit
        except AttributeError:
            logError("The pnl DataFrame is empty")
        except IndexError:
            logError("The DataFrames are empty")

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        lookbackDataDf = lookbackDataDf.replace([np.nan, np.inf, -np.inf], 0)
        pnlKey = 'pnl'
        if 'pnlKey' in featureParams:
            pnlKey = featureParams['pnlKey']
        if len(lookbackDataDf) <= 1:
            prevData = 0
            prevPnl = 0
        else:
            prevData = lookbackDataDf[featureKey].iloc[-2]
            prevPnl = lookbackDataDf[pnlKey].iloc[-2]
        countProfit = prevData
        try:
            pnl = lookbackDataDf[pnlKey].iloc[-1] - prevPnl
            if (pnl > 0):
                countProfit += 1
            return countProfit
        except IndexError:
            logError("The pnl DataFrame is empty")
