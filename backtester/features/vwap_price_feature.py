from backtester.features.feature import Feature


class VwapPriceInstrumentFeature(Feature):

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):
        bookData = instrument.getCurrentBookData()
        totalVolume = (bookData['askVolume'] + bookData['bidVolume'])
        if totalVolume > 0:
            vwap = ((bookData['askPrice'] * bookData['askVolume']) + (bookData['bidPrice'] *
                                                                      bookData['bidVolume'])) / totalVolume
            return vwap
        else:
            return 0

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        raise NotImplementedError
