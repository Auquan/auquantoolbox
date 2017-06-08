class InstrumentFeature(object):

    @classmethod
    def validateInputs(cls, featureKey, featureParams, currentFeatures, instrument):
        return True

    '''
    override this method
    '''
    @classmethod
    def compute(cls, featureKey, featureParams, currentFeatures, instrument):
        raise NotImplementedError
        return None, None
