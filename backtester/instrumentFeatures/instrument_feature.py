from vwap_price_feature import VwapPriceInstrumentFeature
from position_feature import PositionFeature


class InstrumentFeature(object):

    @classmethod
    def getClassForInstrumentFeatureId(cls, instrumentFeatureId):
        # TODO:
        if instrumentFeatureId == 'vwap':
            return VwapPriceInstrumentFeature
        if instrumentFeatureId == 'position':
            return PositionFeature
        return InstrumentFeature

    @classmethod
    def computeForFeature(cls, instrumentFeatureId, featureParams, currentFeatures, instrument):
        instrumentFeatureCls = InstrumentFeature.getClassForInstrumentFeatureId(instrumentFeatureId)
        return instrumentFeatureCls.compute(featureParams, currentFeatures, instrument)

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
