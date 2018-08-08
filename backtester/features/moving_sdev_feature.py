from backtester.features.feature import Feature
import numpy as np
import math

class MovingSDevFeature(Feature):

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
        data.replace(np.Inf,np.nan, inplace=True)
        data.replace(-np.Inf,np.nan,inplace=True)
        data.fillna(0,inplace=True)
        sdev = data[-featureParams['period']:].std()
        sdev.replace(np.Inf,np.nan, inplace=True)
        sdev.replace(-np.Inf,np.nan,inplace=True)
        sdev.fillna(0,inplace=True)
        return sdev

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
        data.replace(np.Inf,np.nan, inplace=True)
        data.replace(-np.Inf,np.nan,inplace=True)
        data.fillna(0,inplace=True)
        sdev = data[-featureParams['period']:].std()
        if(math.isinf(sdev)):
            sdev = 0
        sdev = np.nan_to_num(sdev)
        if len(data) < 1:
            return 0
        return sdev

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
        data.replace(np.Inf,np.nan, inplace=True)
        data.replace(-np.Inf,np.nan,inplace=True)
        data.fillna(0,inplace=True)
        movingStd = data.rolling(window=featureParams['period'], min_periods=1).std()
        movingStd.replace(np.Inf,np.nan, inplace=True)
        movingStd.replace(-np.Inf,np.nan,inplace=True)
        movingStd.fillna(0,inplace=True)
        return movingStd
