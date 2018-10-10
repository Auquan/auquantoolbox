from backtester.features.feature import Feature
from backtester.logger import *
import pandas as pd
import numpy as np


class VarianceFeature(Feature):
    # Computing for Instrument.
    # MAKE SURE PNL is calculated BEFORE this feature
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        instrumentDict = instrumentManager.getAllInstrumentsByInstrumentId()
        zeroSeries = pd.Series([0] * len(instrumentDict), index=instrumentDict.keys())
        pnlKey = 'pnl'
        if 'pnlKey' in featureParams:
            pnlKey = featureParams['pnlKey']

        if updateNum==0 or updateNum == 1:
            return zeroSeries
        prevCount = updateNum - 1

        pnlDataDf = instrumentLookbackData.getFeatureDf(pnlKey)
        varDataDf = instrumentLookbackData.getFeatureDf(featureKey)
        pnlDataDf = pnlDataDf.replace([np.nan, np.inf, -np.inf], 0)
        varDataDf = varDataDf.replace([np.nan, np.inf, -np.inf], 0)

        try:
            sqSum = float(prevCount) * varDataDf.iloc[-1]
            prevAvgPnl = pnlDataDf.iloc[-2] / float(prevCount)
            newAvgPnl = pnlDataDf.iloc[-1] / float(updateNum)
            newSqSum = sqSum + prevCount * (prevAvgPnl**2 - newAvgPnl**2) \
                + (pnlDataDf.iloc[-2] - pnlDataDf.iloc[-1] - newAvgPnl)**2
            return newSqSum / float(updateNum)
        except IndexError:
            logError("DataFrames have less than two elements")
            return zeroSeries


    '''
    Computing for Market.
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        pnlKey = 'pnl'
        lookbackMarketDataDf = instrumentManager.getDataDf()
        if len(lookbackMarketDataDf) <= 2 or instrumentManager is None:
            # First Iteration
            return 0
        if 'pnlKey' in featureParams:
            pnlKey = featureParams['pnlKey']

        prevCount = updateNum - 1

        pnlDict = lookbackMarketDataDf[pnlKey]
        varDict = lookbackMarketDataDf[featureKey]
        pnlDict = pnlDict.replace([np.nan, np.inf, -np.inf], 0)
        varDict = varDict.replace([np.nan, np.inf, -np.inf], 0)
        if len(varDict) <= 1 or (updateNum==0 or updateNum==1):
            return 0

        sqSum = 0 if (len(varDict) <= 1) else float(prevCount) * varDict.iloc[-2]

        try:
            prevAvgPnl = pnlDict.iloc[-2] / float(prevCount)
            newAvgPnl = pnlDict.iloc[-1] / float(prevCount + 1)
            newSqSum = sqSum + prevCount * (prevAvgPnl**2 - newAvgPnl**2)\
                + (pnlDict.iloc[-2] - pnlDict.iloc[-1] - newAvgPnl)**2

            return newSqSum / float(prevCount + 1)
        except IndexError:
            logError("DataFrames have less than two elements")
            return 0
