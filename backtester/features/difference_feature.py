from backtester.features.feature import Feature
import pandas as pd
import numpy as np
import math

class DifferenceFeature(Feature):

    '''
    Computing for Instrument.
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        if data is None or data.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        if featureParams['period']==0:
            raise ValueError('period cannot be 0')
            return None
        if len(data.index) < featureParams['period']-1:
            instrumentDict = instrumentManager.getAllInstrumentsByInstrumentId()
            zeroSeries = pd.Series([0] * len(instrumentDict), index=instrumentDict.keys())
            difference =  data.iloc[-1]
            difference.replace(np.Inf,np.nan, inplace=True)
            difference.replace(-np.Inf,np.nan,inplace=True)
            difference.fillna(0,inplace=True)
            return difference
        difference = data.iloc[-1] - (data.iloc[-featureParams['period']-1]).fillna(0)
        difference.replace(np.Inf,np.nan, inplace=True)
        difference.replace(-np.Inf,np.nan,inplace=True)
        difference.fillna(0,inplace=True)
        return difference

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        if data is None or data.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        if featureParams['period']==0:
            raise ValueError('period cannot be 0')
            return None
        if len(data.index) < featureParams['period']-1:
            difference = data.iloc[-1]
            if(math.isinf(difference)):
                difference = 0
            return np.nan_to_num(difference)
        difference = data.iloc[-1] - np.nan_to_num(data.iloc[-featureParams['period']-1])
        if(math.isinf(difference)):
            difference = 0
        return np.nan_to_num(difference)

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        if data is None or data.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        if featureParams['period']==0:
            raise ValueError('period cannot be 0')
            return None
        mid = data.shift(featureParams['period']).fillna(0.0)
        difference=data-mid
        difference.replace(np.Inf,np.nan, inplace=True)
        difference.replace(-np.Inf,np.nan,inplace=True)
        difference.fillna(0,inplace=True)
        return difference
