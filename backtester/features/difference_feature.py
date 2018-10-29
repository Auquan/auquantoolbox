from backtester.features.feature import *
import pandas as pd
import numpy as np

class DifferenceFeature(Feature):

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
            difference =  data.iloc[-1]
            cClean(difference)
            return difference
        difference = data.iloc[-1] - (data.iloc[-featureParams['period']-1]).fillna(0)
        cClean(difference)
        return difference

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        checkData(data)
        checkPeriod(featureParams)
        if len(data.index) < featureParams['period']-1:
            difference = data.iloc[-1]
            fClean(difference)
            return difference
        difference = data.iloc[-1] - np.nan_to_num(data.iloc[-featureParams['period']-1])
        fClean(difference)
        return difference
