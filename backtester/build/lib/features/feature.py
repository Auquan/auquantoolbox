class Feature(object):

    '''
    Computing for Lookback data. Generic for instrument and market.
    '''
    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        raise NotImplementedError
        return None

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):
        lookbackDataDf = instrument.getDataDf()
        return cls.computeForLookbackData(featureParams, featureKey, currentFeatures, lookbackDataDf)

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        return cls.computeForLookbackData(featureParams, featureKey, currentMarketFeatures, lookbackDataDf)
