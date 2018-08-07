from backtester.features.feature import Feature
from backtester.financial_fn import ma
from backtester.financial_fn import msdev
import numpy as np


class BollingerBandsLowerFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        if data is None or data.empty :
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        if featureParams['period']==0:
            raise ValueError('period cannot be 0')
            return None
        data.replace(np.Inf, np.nan, inplace = True)
        data.replace(-np.Inf, np.nan, inplace = True)
        avg = data[-featureParams['period']:].mean().fillna(0)
        sdev = data[-featureParams['period']:].std().fillna(0)
        return avg - sdev

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        if data is None or data.empty :
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        if featureParams['period']==0:
            raise ValueError('period cannot be 0')
            return None
        data.replace(np.Inf, np.nan, inplace = True)
        data.replace(-np.Inf, np.nan, inplace = True)
        avg = data[-featureParams['period']:].mean()
        sdev = data[-featureParams['period']:].std()
        if len(data) < 1:
            return 0
        return np.nan_to_num(avg) - np.nan_to_num(sdev)

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        if data is None or data.empty :
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        if featureParams['period']==0:
            raise ValueError('period cannot be 0')
            return None
        movingAvg = data.rolling(window=featureParams['period'], min_periods=1).mean().fillna(0.00)
        movingStd = data.rolling(window=featureParams['period'], min_periods=1).std().fillna(0.00)
        return movingAvg-movingStd
