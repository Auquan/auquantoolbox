from backtester.features.feature import *

class MovingSDevFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        checkData(data)
        checkPeriod(featureParams)
        cClean(data)
        sdev = data[-featureParams['period']:].std()
        cClean(sdev)
        return sdev

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        checkData(data)
        checkPeriod(featureParams)
        cClean(data)
        sdev = data[-featureParams['period']:].std()
        fClean(sdev)
        if len(data) < 1:
            return 0
        return sdev

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        checkData(data)
        checkPeriod(featureParams)
        cClean(data)
        movingStd = data.rolling(window=featureParams['period'], min_periods=1).std()
        cClean(movingStd)
        return movingStd
