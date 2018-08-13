from backtester.features.feature import *


# Correlation between two instruments over some number of data points specified by user.

class MovingCorrelationFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data1 = instrumentLookbackData.getFeatureDf(featureParams['featureName1'])
        data2 = instrumentLookbackData.getFeatureDf(featureParams['featureName2'])
        checkDataMultiple(data1, data2)
        checkPeriod(featureParams)
        if (len(data1) < 1) or (len(data2) < 1):
            return 0
        movingCorrelation = data1[featureParams['featureName1']].rolling(window=featureParams['period'], min_periods=1).corr(data2[featureParams['featureName2']])
        pClean(movingCorrelation)
        return movingCorrelation.iloc[-1]

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackMarketFeaturesDf = instrumentManager.getDataDf()
        data1 = lookbackMarketFeaturesDf[featureParams['featureName1']]
        data2 = lookbackMarketFeaturesDf[featureParams['featureName2']]
        checkDataMultiple(data1, data2)
        checkPeriod(featureParams)
        if (len(data1) < 1) or (len(data2) < 1):
            return 0
        movingCorrelation = data1.rolling(window=featureParams['period'], min_periods=1).corr(data2)
        pClean(movingCorrelation)
        return movingCorrelation.iloc[-1]

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data1= featureManager.getFeatureDf(featureParams['featureName1'])
        data2= featureManager.getFeatureDf(featureParams['featureName2'])
        checkDataMultiple(data1, data2)
        checkPeriod(featureParams)
        movingCorrelation = data1[featureParams['featureName1']].rolling(window=featureParams['period'], min_periods=1).corr(data2[featureParams['featureName2']])
        pClean(movingCorrelation)
        return movingCorrelation
