class MarketFeature:

    @classmethod
    def getClassForMarketFeatureId(cls, instrumentFeatureId):
        # TODO:
        return None

    @classmethod
    def computeForFeature(cls, marketFeatureId, featureParams, currentMarketFeatures, instrumentManager):
        instrumentFeatureCls = MarketFeature.getClassForInstrumentFeatureId(marketFeatureId)
        instrumentFeatureCls.compute(currentMarketFeatures, instrumentManager)

    @classmethod
    def validateInputs(cls, currentMarketFeatures, instrument):
        return True

    '''
    override this method
    '''
    @classmethod
    def compute(cls, currentMarketFeatures, instrument):
        raise NotImplementedError
        return None, None
