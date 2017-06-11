from market_feature import MarketFeature
class RatioFeature(MarketFeature):

    @classmethod
    def validateInputs(cls, featureParams, currentMarketFeatures, instrumentManager):
        return True

    '''
    override this method
    '''
    @classmethod
    def compute(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        feature = featureParams['feature']
        instrumentId1 = featureParams['inst_1']
        instrument1 = instrumentManager.getInstrument(instrumentId1)
        instrumentId2 = featureParams['inst_2']
        instrument2 = instrumentManager.getInstrument(instrumentId2)
        if (instrument1 is None) or (instrument2 is None):
            return 0
        else:
            instrument1Price = instrument1.getCurrentBookData()[feature]
            instrument2Price = instrument2.getCurrentBookData()[feature]
            r = instrument1Price/instrument2Price
            return r
