from backtester.features.feature import Feature


class ProfitLossRatioFeature(Feature):

    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):
        pnlKey = 'pnl'
        countKey = 'count'
        if 'pnlKey' in featureParams:
            pnlKey = featureParams['pnlKey']
        if 'countKey' in featureParams:
            countKey = featureParams['countKey']

        lookbackDataDf = instrument.getDataDf()
        lookbackMarketDataDf = instrumentManager.getDataDf()

        if len(lookbackDataDf) <= 1:
            prevData = 0
            prevCount = 0
            prevPnl = 0
        else:
            prevData = lookbackDataDf[featureKey].iloc[-2]
            prevCount = lookbackMarketDataDf[countKey].iloc[-1]
            prevPnl = lookbackDataDf[pnlKey].iloc[-2]

        lossCount = prevCount /(1+ prevData)
        profitCount = prevCount - lossCount
        if (lookbackDataDf[pnlKey].iloc[-1] - prevPnl > 0):
            profitCount += 1
        else:
            lossCount += 1
        prevCount += 1
        return float(profitCount) / float(lossCount)

    @classmethod
    def computeForMarket(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        pnlKey = 'pnl'
        countKey = 'count'
        if 'pnlKey' in featureParams:
            pnlKey = featureParams['pnlKey']
        if 'countKey' in featureParams:
            countKey = featureParams['countKey']

        lookbackMarketDataDf = instrumentManager.getDataDf()

        if len(lookbackMarketDataDf) <= 1:
            prevData = 0
            prevCount = 0
            prevPnl = 0
        else:
            prevData = lookbackMarketDataDf[featureKey].iloc[-2]
            prevCount = lookbackMarketDataDf[countKey].iloc[-2]
            prevPnl = lookbackMarketDataDf[pnlKey].iloc[-2]

        profitCount = prevCount * prevData
        if (lookbackMarketDataDf[pnlKey].iloc[-1] - prevPnl > 0):
            profitCount += 1
        prevCount += 1
        lossCount = prevCount - profitCount
        return float(profitCount) / float(lossCount)
