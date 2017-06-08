class InstrumentFeature(object):

    @classmethod
    def validateInputs(cls, featureParams, currentFeatures, instrument):
        return True

    '''
    override this method
    '''
    @classmethod
    def compute(cls, featureParams, featureKey, currentFeatures, instrument):
        raise NotImplementedError
        return None, None
