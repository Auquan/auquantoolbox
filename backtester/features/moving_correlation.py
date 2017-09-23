from backtester.features.feature import Feature


# Correlation between two instruments over some number of data points specified by user.

class MovingCorrelationFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        x = instrumentLookbackData.getFeatureDf(featureParams['series1'])
        y = instrumentLookbackData.getFeatureDf(featureParams['series2'])

        return (x.rolling(featureParams['period']).corr(y)).iloc[-1]

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackMarketFeaturesDf = instrumentManager.getDataDf()
        x = lookbackMarketFeaturesDf[featureParams['series1']]
        y = lookbackMarketFeaturesDf[featureParams['series2']]

        if (len(x) < 1) or (len(y) < 1):
            return 0
        return round((x.rolling(featureParams['period']).corr(y)).iloc[-1], 3)
