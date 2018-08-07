from backtester.features.feature import Feature
import pandas as pd
import numpy as np
import math

class MomentumFeature(Feature):

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
        mid = data.shift(featureParams['period']).fillna(method='pad')
        if len(data.index) > featureParams['period']:
            momentum = ((data.iloc[-1] / mid.iloc[-1]) - 1) * 100
            momentum.replace(np.Inf,np.nan, inplace=True)
            momentum.replace(-np.Inf,np.nan,inplace=True)
            momentum.fillna(0,inplace=True)
            return momentum
        else:
            instrumentDict = instrumentManager.getAllInstrumentsByInstrumentId()
            zeroSeries = pd.Series([0] * len(instrumentDict), index=instrumentDict.keys())
            return zeroSeries

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
        mid = data.shift(featureParams['period']).fillna(method='pad')
        if len(data.index) > featureParams['period']:
            m = ((data.iloc[-1] /mid.iloc[-1]) -1)
        else:
            m = 0
        if(math.isinf(m)):
            m=0
        m=np.nan_to_num(m)
        return m*100

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
        mid = data.shift(featureParams['period']).fillna(method='pad')
        momentum = ((data/mid)-1)*100
        momentum.replace(np.Inf,np.nan, inplace=True)
        momentum.replace(-np.Inf,np.nan,inplace=True)
        momentum.fillna(0,inplace=True)
        return momentum
