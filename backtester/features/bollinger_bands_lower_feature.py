from backtester.features.feature import Feature
from backtester.financial_fn import ma
from backtester.financial_fn import msdev


class BollingerBandsLowerFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        avg = data[-featureParams['period']:].mean()
        sdev = data[-featureParams['period']:].std().fillna(0)
        return avg - sdev

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        avg = data[-featureParams['period']:].mean()
        sdev = data[-featureParams['period']:].std().fillna(0)
        if len(data) < 1:
            return 0
        return avg - sdev

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        if data is None:
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        movingAvg = data.rolling(window=featureParams['period'], min_periods=1).mean()
        movingStd = data.rolling(window=featureParams['period'], min_periods=1).std().fillna(0.00)
        return movingAvg-movingStd
