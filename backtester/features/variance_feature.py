from backtester.features.feature import Feature
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

        if updateNum == 1:
            return zeroSeries
        prevCount = updateNum - 1

        pnlDataDf = instrumentLookbackData.getFeatureDf(pnlKey)
        varDataDf = instrumentLookbackData.getFeatureDf(featureKey)
        pnlDataDf = pnlDataDf.replace([np.nan, np.inf, -np.inf], 0)
        varDataDf = varDataDf.replace([np.nan, np.inf, -np.inf], 0)	
        if pnlDataDf.empty or varDataDf.empty or len(pnlDataDf)<2 or len(varDataDf)<2:
        		return zeroSeries

        sqSum = float(prevCount) * varDataDf.iloc[-1]

        prevAvgPnl = pnlDataDf.iloc[-2] / float(prevCount)
        newAvgPnl = pnlDataDf.iloc[-1] / float(updateNum)
        newSqSum = sqSum + prevCount * (prevAvgPnl**2 - newAvgPnl**2) \
            + (pnlDataDf.iloc[-2] - pnlDataDf.iloc[-1] - newAvgPnl)**2

        return newSqSum / float(updateNum)


    '''
    Computing for Market. 
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        pnlKey = 'pnl'
        lookbackMarketDataDf = instrumentManager.getDataDf()
        if len(lookbackMarketDataDf) <= 2 or instrumentManager is None:
            # First Iteration
            return np.float64(0.0)
        if 'pnlKey' in featureParams:
            pnlKey = featureParams['pnlKey']

        prevCount = updateNum - 1
        
        pnlDict = lookbackMarketDataDf[pnlKey]
        varDict = lookbackMarketDataDf[featureKey]
        pnlDict = pnlDict.replace([np.nan, np.inf, -np.inf], 0)
        varDict = varDict.replace([np.nan, np.inf, -np.inf], 0)
        if len(varDict) <= 1:
            return np.float64(0.0)
        

        sqSum = 0 if (len(varDict) <= 1) else float(prevCount) * varDict.iloc[-2]

        prevAvgPnl = pnlDict.iloc[-2] / float(prevCount)
        newAvgPnl = pnlDict.iloc[-1] / float(prevCount + 1)
        newSqSum = sqSum + prevCount * (prevAvgPnl**2 - newAvgPnl**2)\
            + (pnlDict.iloc[-2] - pnlDict.iloc[-1] - newAvgPnl)**2

        return newSqSum / float(prevCount + 1)
