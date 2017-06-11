from market_feature import MarketFeature
from backtester.financial_fn import msdev

class MovingSdevInstrumentFeature(MarketFeature):

    @classmethod
    def validateInputs(cls, featureParams, currentMarketFeatures, instrumentManager):
        return True

    @classmethod
    def compute(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        data = instrumentManager.getLookbackMarketFeatures().getData()[featureParams['featureName']]
        avg = msdev(data, featureParams['period'])
        if len(avg.index) > 0 :
        	return avg[-1]
        else:
        	return currentMarketFeatures[featureParams['featureName']]
        