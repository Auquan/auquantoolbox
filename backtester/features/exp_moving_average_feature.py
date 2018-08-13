from backtester.features.feature import *
import math


class ExpMovingAverageFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureKey)
        data1 = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        checkData(data1)
        checkPeriod(featureParams)
        if len(data.index) >= 1:
            prev_ema = data.iloc[-1]
        else:
            prev_ema = data1.iloc[-1]
        halflife = featureParams['period']
        alpha = 1 - math.exp(math.log(0.5) / halflife)
        avg = data1.iloc[-1] * alpha + prev_ema * (1 - alpha)
        return avg.fillna(0)

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureKey]
        data1 = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        checkData(data1)
        checkPeriod(featureParams)
        if len(data.index) >= 1:
            prev_ema = data.iloc[-1]
        else:
            prev_ema = data1.iloc[-1]
        halflife = featureParams['period']
        alpha = 1 - math.exp(math.log(0.5) / halflife)
        avg = data1.iloc[-1] * alpha + prev_ema * (1 - alpha)
        if(math.isnan(avg)):
            avg=0
        return avg

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        checkData(data)
        checkPeriod(featureParams)
        halflife = featureParams['period']
        expMovingAvg = data.ewm(halflife=halflife, adjust=False).mean()
        return expMovingAvg.fillna(0)
