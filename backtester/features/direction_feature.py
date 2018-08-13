from backtester.features.feature import *
import pandas as pd
import numpy as np


class DirectionFeature(Feature):

    '''
    Computing for Instrument.
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        checkData(data)
        checkPeriod(featureParams)
        if len(data.index) < featureParams['period']-1:
            instrumentDict = instrumentManager.getAllInstrumentsByInstrumentId()
            zeroSeries = pd.Series([0] * len(instrumentDict), index=instrumentDict.keys())
            return np.sign(data.iloc[-1])
        pClean(data)
        return np.sign(data.iloc[-1] - data.iloc[-featureParams['period']-1])

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        checkData(data)
        checkPeriod(featureParams)
        if len(data.index) < featureParams['period']-1:
            return np.sign(np.nan_to_num(data.iloc[-1]))
        return np.sign(np.nan_to_num(data.iloc[-1]) - np.nan_to_num(data.iloc[-featureParams['period']-1]))

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        checkData(data)
        checkPeriod(featureParams)
        mid = data.shift(featureParams['period']).fillna(0.00)
        pClean(data)
        direction = np.sign(data-mid)
        return direction
