from backtester.features.feature import Feature


class CapitalFeature(Feature):

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):

        currentPosition = instrument.getCurrentPosition()
        if len(instrument.getDataDf()['position']) < 1:
            previousPosition = 0
        else:
            previousPosition = instrument.getDataDf()['position'][-1]
        currentPrice = currentFeatures[featureParams['price']]
        changeInCapital = (currentPosition - previousPosition) * currentPrice + currentFeatures[featureParams['fees']]
        return changeInCapital

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        changeInCapital = 0
        capitalDict = instrumentManager.getDataDf()[featureKey]
        if len(capitalDict) < 1:
            return featureParams['initial_capital']
        capital = capitalDict.values[-1]
        allInstruments = instrumentManager.getAllInstrumentsByInstrumentId()
        for instrumentId in allInstruments:
            instrument = allInstruments[instrumentId]
            changeInCapital -= instrument.getDataDf()[featureKey][-1]
        return capital + changeInCapital
