from backtester.features.feature import Feature
from backtester.financial_fn import ma
from backtester.financial_fn import msdev


class BollingerBandsFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        raise NotImplementedError
        return 'Please use bollinger_bands_lower and bollinger_bands_upper'

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        raise NotImplementedError
        return 'Please use bollinger_bands_lower and bollinger_bands_upper'
