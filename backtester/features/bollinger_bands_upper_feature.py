from backtester.features.feature import Feature
from backtester.financial_fn import ma
from backtester.financial_fn import msdev


class BollingerBandsUpperFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        avg = data[-featureParams['period']:].mean()
        sdev = data[-featureParams['period']:].std().fillna(0)
        return avg + sdev

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        avg = data[-featureParams['period']:].mean()
        sdev = data[-featureParams['period']:].std().fillna(0)
        if len(data) < 1:
            return 0
        return avg + sdev
