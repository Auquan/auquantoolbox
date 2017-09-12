from backtester.features.feature import Feature


class ProfitLossRatioFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        pnlKey = 'pnl'
        countKey = 'count'
        if 'pnlKey' in featureParams:
            pnlKey = featureParams['pnlKey']
        if 'countKey' in featureParams:
            countKey = featureParams['countKey']

        prevData = lookbackDataDf[featureKey].iloc[-2]
        prevCount = lookbackDataDf[countKey].iloc[-2]
        profitCount = prevCount * prevData
        if (lookbackDataDf[pnlKey].iloc[-1] - lookbackDataDf[pnlKey].iloc[-2] > 0):
            profitCount += 1
        prevCount += 1
        lossCount = prevCount - profitCount
        return float(profitCount) / float(lossCount)
