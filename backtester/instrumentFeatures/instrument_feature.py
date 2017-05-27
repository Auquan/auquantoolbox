class InstrumentFeature:

    @classmethod
    def getClassForInstrumentFeatureId(cls, instrumentFeatureId):
        # TODO:
        return InstrumentFeature

    '''
    override this method
    '''
    @classmethod
    def compute(cls, currentBookData):
        raise NotImplementedError
        return

    @classmethod
    def computeForFeature(cls, instrumentFeatureId, currentBookData, currentFeatures, ):
        instrumentFeatureCls = InstrumentFeature.getClassForInstrumentFeatureId(instrumentFeatureId)
        instrumentFeatureCls.compute(currentBookData)
