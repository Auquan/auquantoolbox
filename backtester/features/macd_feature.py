from backtester.features.feature import *
import numpy as np

class MACDFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        checkData(data)
        checkPeriod(featureParams)
        avg1 = data[-featureParams['period1']:].mean()
        avg2 = data[-featureParams['period2']:].mean()
        pClean(avg1)
        pClean(avg2)
        return (avg1 - avg2).fillna(0)

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        checkData(data)
        checkPeriod(featureParams)
        avg1 = data[-featureParams['period1']:].mean()
        avg2 = data[-featureParams['period2']:].mean()
        return np.nan_to_num(np.nan_to_num(avg1) - np.nan_to_num(avg2))

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        checkData(data)
        checkPeriod(featureParams)
        movingAvg1 = data.rolling(window=featureParams['period1'], min_periods=1).mean()
        movingAvg2 = data.rolling(window=featureParams['period2'], min_periods=1).mean()
        pClean(movingAvg1)
        pClean(movingAvg2)
        macd = movingAvg1-movingAvg2
        return macd.fillna(0)
