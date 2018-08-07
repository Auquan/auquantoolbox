from backtester.features.feature import Feature
import numpy as np

class MACDFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        if data is None or data.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        if featureParams['period1']==0 or featureParams['period2']==0:
            raise ValueError('period cannot be 0')
            return None
        avg1 = data[-featureParams['period1']:].mean()
        avg2 = data[-featureParams['period2']:].mean()
        avg1.fillna(0,inplace=True)
        avg2.fillna(0,inplace=True)
        return (avg1 - avg2).fillna(0)

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        if data is None or data.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        if featureParams['period1']==0 or featureParams['period2']==0:
            raise ValueError('period cannot be 0')
            return None
        avg1 = data[-featureParams['period1']:].mean()
        avg2 = data[-featureParams['period2']:].mean()
        return np.nan_to_num(np.nan_to_num(avg1) - np.nan_to_num(avg2))

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        if data is None or data.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        if featureParams['period1']==0 or featureParams['period2']==0:
            raise ValueError('period cannot be 0')
            return None
        movingAvg1 = data.rolling(window=featureParams['period1'], min_periods=1).mean()
        movingAvg2 = data.rolling(window=featureParams['period2'], min_periods=1).mean()
        movingAvg1.fillna(0,inplace=True)
        movingAvg2.fillna(0,inplace=True)
        macd = movingAvg1-movingAvg2
        return macd.fillna(0)
