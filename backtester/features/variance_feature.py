from backtester.features.feature import Feature


class VarianceFeature(Feature):
    # Computing for Instrument. By default defers to computeForLookbackData
    # MAKE SURE PNL is calculated BEFORE this feature
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):
        lookbackDataDf = instrument.getDataDf()
        pnlKey = 'pnl'
        countKey = 'count'
        if len(lookbackDataDf) <= 1 or instrumentManager is None:
            return 0
        lookbackMarketDataDf = instrumentManager.getDataDf()
        if 'pnlKey' in featureParams:
            pnlKey = featureParams['pnlKey']
        if 'countKey' in featureParams:
            countKey = featureParams['countKey']
        if len(lookbackMarketDataDf) <= 1:
            # first iteration
            return 0
        prevCount = lookbackMarketDataDf[countKey].iloc[-1]

        pnlDict = lookbackDataDf[pnlKey]
        varDict = lookbackDataDf[featureKey]
        if len(varDict) <= 1:
            return 0

        sqSum = 0 if (len(varDict) <= 1) else float(prevCount) * varDict.iloc[-2]

        prevAvgPnl = pnlDict.iloc[-2] / float(prevCount)
        newAvgPnl = pnlDict.iloc[-1] / float(prevCount + 1)
        newSqSum = sqSum + prevCount * (prevAvgPnl**2 - newAvgPnl**2) \
            + (pnlDict.iloc[-2] - pnlDict.iloc[-1] - newAvgPnl)**2

        return newSqSum / float(prevCount + 1)

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        pnlKey = 'pnl'
        countKey = 'count'
        lookbackMarketDataDf = instrumentManager.getDataDf()
        if len(lookbackMarketDataDf) <= 2 or instrumentManager is None:
            # First Iteration
            return 0
        if 'pnlKey' in featureParams:
            pnlKey = featureParams['pnlKey']
        if 'countKey' in featureParams:
            countKey = featureParams['countKey']

        prevCount = lookbackMarketDataDf[countKey].iloc[-2]

        pnlDict = lookbackMarketDataDf[pnlKey]
        varDict = lookbackMarketDataDf[featureKey]
        if len(varDict) <= 1:
            return 0

        sqSum = 0 if (len(varDict) <= 1) else float(prevCount) * varDict.iloc[-2]

        prevAvgPnl = pnlDict.iloc[-2] / float(prevCount)
        newAvgPnl = pnlDict.iloc[-1] / float(prevCount + 1)
        newSqSum = sqSum + prevCount * (prevAvgPnl**2 - newAvgPnl**2)\
            + (pnlDict.iloc[-2] - pnlDict.iloc[-1] - newAvgPnl)**2

        return newSqSum / float(prevCount + 1)
