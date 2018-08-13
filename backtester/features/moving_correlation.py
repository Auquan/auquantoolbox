from backtester.features.feature import Feature


# Correlation between two instruments over some number of data points specified by user.

class MovingCorrelationFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        x = instrumentLookbackData.getFeatureDf(featureParams['featureName1'])
        y = instrumentLookbackData.getFeatureDf(featureParams['featureName2'])

        if (len(x) < 1) or (len(y) < 1):
            return 0
        return (x.rolling(featureParams['period'],min_periods=1).corr(y)).iloc[-1]

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackMarketFeaturesDf = instrumentManager.getDataDf()
        x = lookbackMarketFeaturesDf[featureParams['featureName1']]
        y = lookbackMarketFeaturesDf[featureParams['featureName2']]

        if (len(x) < 1) or (len(y) < 1):
            return 0
        return round((x.rolling(featureParams['period'],min_periods=1).corr(y)).iloc[-1], 3)

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data1= featureManager.getFeatureDf(featureParams['featureName1'])
        data2= featureManager.getFeatureDf(featureParams['featureName2'])
        if (data1 is None) or (data2 is None):
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName1'], featureKey))
            return None
        movingCorrelation = data1.rolling(window=featureParams['period'], min_periods=1).corr(data2)
        movingCorrelation.fillna(0.0, inplace=True)
        return movingCorrelation
