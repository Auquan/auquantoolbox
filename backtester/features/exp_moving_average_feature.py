from backtester.features.feature import Feature
import math


class ExpMovingAverageFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureKey)
        if data is None or data.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
        if featureParams['period']==0:
            raise ValueError('period cannot be 0')
            return None
        if len(data.index) >= 1:
            prev_ema = data.iloc[-1]
        else:
            prev_ema = instrumentLookbackData.getFeatureDf(featureParams['featureName']).iloc[-1]
        halflife = featureParams['period']
        alpha = 1 - math.exp(math.log(0.5) / halflife)
        avg = instrumentLookbackData.getFeatureDf(featureParams['featureName']).iloc[-1] * alpha + prev_ema * (1 - alpha)
        return avg.fillna(0)

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureKey]
        if data is None or data.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
        if featureParams['period']==0:
            raise ValueError('period cannot be 0')
            return None
        if len(data.index) >= 1:
            prev_ema = data.iloc[-1]
        else:
            prev_ema = instrumentLookbackData.getFeatureDf(featureParams['featureName']).iloc[-1]
        halflife = featureParams['period']
        alpha = 1 - math.exp(math.log(0.5) / halflife)
        avg = instrumentLookbackData.getFeatureDf(featureParams['featureName']).iloc[-1] * alpha + prev_ema * (1 - alpha)
        if(math.isnan(avg)):
            avg=0
        return avg

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        if data is None or data.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
        if featureParams['period']==0:
            raise ValueError('period cannot be 0')
            return None
        halflife = featureParams['period']
        expMovingAvg = data.ewm(halflife=halflife, adjust=False).mean()
        return expMovingAvg.fillna(0)
