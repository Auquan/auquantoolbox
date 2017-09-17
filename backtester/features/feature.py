class Feature(object):

    '''
    Computing for Instrument.
    '''
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, instrumentManager):
        raise NotImplementedError
        return None

    '''
    Computing for Market.
    '''
    @classmethod
    def computeForMarket(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        raise NotImplementedError
        return None
