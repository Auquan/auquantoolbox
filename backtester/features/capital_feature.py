from backtester.features.feature import Feature


class CapitalFeature(Feature):

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        positionData = instrumentLookbackData.getDataForFeatureForAllInstruments('position')
        currentPosition = positionData.iloc[-1]
        zeroSeries = currentPosition * 0
        if (updateNum == 1):
            previousPosition = zeroSeries
        else:
            previousPosition = positionData.iloc[-2]
        currentPrice = instrumentLookbackData.getDataForFeatureForAllInstruments(featureParams['price']).iloc[-1]
        currentFees = instrumentLookbackData.getDataForFeatureForAllInstruments(featureParams['fees']).iloc[-1]
        changeInCapital = (currentPosition - previousPosition) * currentPrice + currentFees
        return changeInCapital

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        changeInCapital = 0
        capitalDict = instrumentManager.getDataDf()[featureKey]
        if len(capitalDict) <= 1:
            return featureParams['initial_capital']
        capital = capitalDict.values[-2]
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        changeInCapital = instrumentLookbackData.getDataForFeatureForAllInstruments(featureKey).iloc[-1].sum()
        return capital + changeInCapital
