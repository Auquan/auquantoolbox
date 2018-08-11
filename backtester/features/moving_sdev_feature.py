from backtester.features.feature import Feature


class MovingSDevFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        sdev = data[-featureParams['period']:].std().fillna(0)
        return sdev

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        sdev = data[-featureParams['period']:].std()
        if len(data) < 1:
            return 0
        return sdev

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        if data is None:
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        movingStd = data.rolling(window=featureParams['period'], min_periods=1).std().fillna(0.00)
        return movingStd
