from vwap_price_feature import VwapPriceInstrumentFeature


class InstrumentFeature:

    @classmethod
    def getClassForInstrumentFeatureId(cls, instrumentFeatureId):
        # TODO:
        if instrumentFeatureId == 'vwap':
            return VwapPriceInstrumentFeature
        return InstrumentFeature

    @classmethod
    def computeForFeature(cls, instrumentFeatureId, featureParams, currentFeatures, instrument):
        instrumentFeatureCls = InstrumentFeature.getClassForInstrumentFeatureId(instrumentFeatureId)
        instrumentFeatureCls.compute(currentFeatures, instrument)

    @classmethod
    def validateInputs(cls, currentFeatures, instrument):
        return True

    '''
    override this method
    '''
    @classmethod
    def compute(cls, currentFeatures, instrument):
        raise NotImplementedError
        return None, None
