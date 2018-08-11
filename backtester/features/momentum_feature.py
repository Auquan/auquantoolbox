from backtester.features.feature import Feature
import pandas as pd
import numpy as np


class MomentumFeature(Feature):

    '''
    Computing for Instrument.
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        dataDf = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        if len(dataDf.index) > featureParams['period']:
            m = ((dataDf.iloc[-1] / dataDf.iloc[-featureParams['period']]) - 1) * 100
            return m
        else:
            instrumentDict = instrumentManager.getAllInstrumentsByInstrumentId()
            zeroSeries = pd.Series([0] * len(instrumentDict), index=instrumentDict.keys())
            return zeroSeries

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        if len(data.index) > featureParams['period']:
            m = (data[-1] / data[-featureParams['period']] - 1) * 100
        else:
            m = 0
        return m

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        if data is None:
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        mid = data.shift(featureParams['period']).fillna(0.00)
        momentum = ((data/mid)-1)*100
        momentum[momentum == np.Inf] = 0.00
        return momentum
