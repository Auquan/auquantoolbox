from backtester.features.feature import Feature
import numpy as np

class MovingMaximumFeature(Feature):

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
        movingMax = data[-featureParams['period']:].max()
        return movingMax

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
        movingMax = data[-featureParams['period']:].max()
        return movingMax

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
        movingMax = data.rolling(window=featureParams['period'], min_periods=1).max()
        movingMax.replace(np.Inf,np.nan, inplace=True)
        movingMax.replace(-np.Inf,np.nan,inplace=True)
        movingMax.fillna(0,inplace=True)
        return movingMax
