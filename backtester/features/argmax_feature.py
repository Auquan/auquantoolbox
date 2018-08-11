from backtester.features.feature import Feature
import pandas as pd
import numpy as np


class ArgMaxFeature(Feature):

    '''
    Computing for Instrument.
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        featureDataDf = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        if len(featureDataDf) < 1:
            instrumentDict = instrumentManager.getAllInstrumentsByInstrumentId()
            zeroSeries = pd.Series([0] * len(instrumentDict), index=instrumentDict.keys())
            return zeroSeries
        return featureDataDf[-featureParams['period']:].idxmax().astype(object)

    '''
    Computing for Market.
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        if len(data) < 1:
            return 0
        return data[-featureParams['period']:].idxmax()


    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        if data is None:
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        argMax = data.rolling(window=featureParams['period'], min_periods=1).apply(np.argmax)
        return argMax
