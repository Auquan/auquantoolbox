from feature import Feature


class RatioMarketFeature(Feature):

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):
        raise NotImplementedError

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        feature = featureParams['feature']
        instrumentId1 = featureParams['inst_1']
        instrument1 = instrumentManager.getInstrument(instrumentId1)
        instrumentId2 = featureParams['inst_2']
        instrument2 = instrumentManager.getInstrument(instrumentId2)
        if (instrument1 is None) or (instrument2 is None):
            return 0
        else:
            instrument1Price = instrument1.getDataDf()[feature].iloc[-1]
            instrument2Price = instrument2.getDataDf()[feature].iloc[-1]
            if instrument2Price is not 0:
                return instrument1Price / instrument2Price
            else:
                return 0
