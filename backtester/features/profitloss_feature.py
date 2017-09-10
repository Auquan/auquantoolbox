from backtester.features.feature import Feature


class ProfitLossFeature(Feature):

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):

        priceDict = instrument.getDataDf()[featureParams['price']]
        if len(priceDict) < 1:
            return 0
        fees = currentFeatures[featureParams['fees']]
        currentPosition = instrument.getCurrentPosition()
        previousPosition = instrument.getDataDf()['position'][-2] if (len(instrument.getDataDf()['position']) > 1) else 0
        previousPrice = priceDict[-2] if (len(priceDict) > 1) else 0
        currentPrice = currentFeatures[featureParams['price']]
        changeInPosition = currentPosition - previousPosition
        tradePrice = instrument.getLastTradePrice()
        pnl = (previousPosition * (currentPrice - previousPrice)) + (changeInPosition * (currentPrice - tradePrice)) - fees
        return pnl

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        pnl = 0
        pnlDict = instrumentManager.getDataDf()[featureKey]
        pnlKey = 'pnl'
        if 'instrument_pnl_feature' in featureParams:
            pnlKey = featureParams['instrument_pnl_feature']
        if len(pnlDict) < 1:
            return 0
        cumulativePnl = 0 if (len(pnlDict) == 1) else pnlDict.values[-2]
        allInstruments = instrumentManager.getAllInstrumentsByInstrumentId()
        for instrumentId in allInstruments:
            instrument = allInstruments[instrumentId]
            pnl += instrument.getDataDf()[pnlKey][-1]
        cumulativePnl += pnl
        return cumulativePnl
