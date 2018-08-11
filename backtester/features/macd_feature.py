from backtester.features.feature import Feature


class MACDFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        dataDf = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        avg1 = dataDf[-featureParams['period1']:].mean()
        avg2 = dataDf[-featureParams['period2']:].mean()
        return avg1 - avg2

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        avg1 = data[-featureParams['period1']:].mean()
        avg2 = data[-featureParams['period2']:].mean()
        return (avg1 - avg2)

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        if data is None:
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        movingAvg1 = data.rolling(window=featureParams['period1'], min_periods=1).mean()
        movingAvg2 = data.rolling(window=featureParams['period2'], min_periods=1).mean()
        macd = movingAvg1-movingAvg2
        return macd
