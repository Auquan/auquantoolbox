from backtester.features.feature import Feature
import pandas as pd
import numpy as np
import math

class ScaleFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        dataDf = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        if dataDf is None or dataDf.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        if featureParams['period']==0:
            raise ValueError('period cannot be 0')
            return None
        if featureParams['scale']==0:
            raise ValueError('scale cannot be 0')
            return None
        dataDf.replace(np.Inf,np.nan, inplace=True)
        dataDf.replace(-np.Inf,np.nan,inplace=True)
        dataDf.fillna(0,inplace=True)
        data = dataDf[-featureParams['period']:]
        scale = np.abs(data).mul(featureParams['scale']).div(np.abs(data).sum())
        scale.replace(np.Inf,np.nan, inplace=True)
        scale.replace(-np.Inf,np.nan,inplace=True)
        scale.fillna(0,inplace=True)
        return scale.iloc[-1]

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']][-featureParams['period']:]
        if data is None or data.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        if featureParams['period']==0:
            raise ValueError('period cannot be 0')
            return None
        if featureParams['scale']==0:
            raise ValueError('scale cannot be 0')
            return None
        data.replace(np.Inf,np.nan, inplace=True)
        data.replace(-np.Inf,np.nan,inplace=True)
        data.fillna(0,inplace=True)
        scale = np.abs(data).mul(featureParams['scale']).div(np.abs(data).sum()).iloc[-1]
        if(math.isinf(scale)):
            scale = 0
        return np.nan_to_num(scale)

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
        if featureParams['scale']==0:
            raise ValueError('scale cannot be 0')
            return None
        data.replace(np.Inf,np.nan, inplace=True)
        data.replace(-np.Inf,np.nan,inplace=True)
        data.fillna(0,inplace=True)
        data1 = data.abs()
        scale = data1.rolling(window = featureParams['period'], min_periods = 1).sum()
        scale = (data1.div(scale)).mul(featureParams['scale'])
        scale.replace(np.Inf,np.nan, inplace=True)
        scale.replace(-np.Inf,np.nan,inplace=True)
        scale.fillna(0,inplace=True)
        return scale
