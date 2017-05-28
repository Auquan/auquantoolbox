
class InstrumentFeatureConfig:

    def __init__(self, configDict):
        # TODO: validate
        self.__featureKey = configDict['featureKey']
        self.__featureIdentifier = configDict['featureId']
        self.__featureParams = configDict['params']

    def getFeatureKey(self):
        return self.__featureKey

    def getFeatureId(self):
        return self.__featureIdentifier

    def getFeatureParams(self):
        return self.__featureParams


class InstrumentFeature:

    @classmethod
    def getClassForInstrumentFeatureId(cls, instrumentFeatureId):
        # TODO:
        if instrumentFeatureId == 'vwap_price':
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

    
