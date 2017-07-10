from feature import Feature
import numpy as np

class ProfitLossFeature(Feature):

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):

        priceDict = instrument.getDataDf()[featureParams['price']]
        if len(priceDict) <1:
            return 0
        fees = currentFeatures[featureParams['fees']]
        currentPosition = instrument.getCurrentPosition()
        previousPosition = instrument.getDataDf()['position'][-1]
        previousPrice = priceDict[-1]
        currentPrice = currentFeatures[featureParams['price']]       
        pnl = previousPosition * (currentPrice - previousPrice) - fees
        return pnl


    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        pnl = 0
        pnlDict = instrumentManager.getDataDf()[featureKey]
        if len(pnlDict) < 1:
            return 0
        cumulativePnl = pnlDict.values[-1]
        allInstruments = instrumentManager.getAllInstrumentsByInstrumentId()
        for instrumentId in allInstruments:
            instrument = allInstruments[instrumentId]
            pnl += instrument.getDataDf()[featureParams['instrument_pnl_feature']][-1]
        cumulativePnl += pnl
        return cumulativePnl
