from backtester.features.feature import Feature


class PositionInstrumentFeature(Feature):

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentsDict = instrumentManager.getAllInstrumentsByInstrumentId()
        positionDict = {}
        for instrumentId in instrumentsDict:
            positionDict[instrumentId] = instrumentManager.getInstrument(instrumentId).getCurrentPosition()
        return positionDict

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        raise NotImplementedError
