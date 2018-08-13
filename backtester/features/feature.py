class Feature(object):

    '''
    Computing for Instrument Update
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        raise NotImplementedError
        return None

    '''
    Computing for Market.
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        raise NotImplementedError
        return None


    '''
    Computing for Instrument Data.
    '''
    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        raise NotImplementedError
        return None
