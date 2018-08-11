from backtester.features.feature import Feature


class MovingMaximumFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        dataDf = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        return dataDf[-featureParams['period']:].max()

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        return data[-featureParams['period']:].max()

@classmethod
def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
    data = featureManager.getFeatureDf(featureParams['featureName'])
    if data is None:
        logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
        return None
    movingMax = data.rolling(window=featureParams['period'], min_periods=1).max()
    return movingMax
