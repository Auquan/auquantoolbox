class MarketFeature:

    @classmethod
    def getClassForMarketFeatureId(cls, marketFeatureId):
        # TODO:
        return MarketFeature

    '''
    override this method
    '''
    @classmethod
    def compute(cls):
        raise NotImplementedError
        return

    @classmethod
    def computeForFeature(cls, marketFeatureId, currentBookData):
        marketFeatureCls = MarketFeature.getClassForMarketFeatureId(marketFeatureId)
        marketFeatureCls.compute()
