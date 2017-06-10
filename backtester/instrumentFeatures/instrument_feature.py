class InstrumentFeature(object):

    @classmethod
    def validateInputs(cls, featureKey, featureParams, currentFeatures, instrument):
        return True

    '''
    override this method
    '''
    @classmethod
    def compute(cls, featureParams, featureKey, currentFeatures, instrument):
        raise NotImplementedError
        return None, None
