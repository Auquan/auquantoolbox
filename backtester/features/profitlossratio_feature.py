from backtester.features.feature import Feature


def computeForOneInstrument(instrumentId, featureKey, pnlKey, instrumentLookbackData):
    featureData = instrumentLookbackData.getDataForFeatureForAllInstruments(featureKey)
    pnlData = instrumentLookbackData.getDataForFeatureForAllInstruments(pnlKey)

    if len(featureData) < 1:
        prevData = {'totalLoss': 0, 'totalProfit': 0,
                    'countLoss': 0, 'countProfit': 0}
        prevPnl = 0
    else:
        prevData = featureData.iloc[-1][instrumentId]
        prevPnl = pnlData.iloc[-2][instrumentId]

    totalLoss = prevData['totalLoss']
    totalProfit = prevData['totalProfit']
    countLoss = prevData['countLoss']
    countProfit = prevData['countProfit']

    pnl = pnlData.iloc[-1][instrumentId] - prevPnl

    if (pnl > 0):
        totalProfit += pnl
        countProfit += 1
    elif (pnl < 0):
        totalLoss += -pnl
        countLoss += 1

    return {'totalLoss': totalLoss, 'totalProfit': totalProfit,
            'countLoss': countLoss, 'countProfit': countProfit}

class ProfitLossRatioFeature(Feature):

    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        pnlKey = 'pnl'
        if 'pnlKey' in featureParams:
            pnlKey = featureParams['pnlKey']
        toRtn = {}
        for instrumentId in instrumentManager.getAllInstrumentsByInstrumentId():
            toRtn[instrumentId] = computeForOneInstrument(instrumentId, featureKey, pnlKey, instrumentLookbackData)
        return toRtn

    @classmethod
    def computeForMarket(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()

        pnlKey = 'pnl'
        if 'pnlKey' in featureParams:
            pnlKey = featureParams['pnlKey']
        if len(lookbackDataDf) <= 1:
            prevData = {'totalLoss': 0, 'totalProfit': 0,
                        'countLoss': 0, 'countProfit': 0}
            prevPnl = 0
        else:
            prevData = lookbackDataDf[featureKey].iloc[-2]
            prevPnl = lookbackDataDf[pnlKey].iloc[-2]

        totalLoss = prevData['totalLoss']
        totalProfit = prevData['totalProfit']
        countLoss = prevData['countLoss']
        countProfit = prevData['countProfit']

        pnl = lookbackDataDf[pnlKey].iloc[-1] - prevPnl

        if (pnl > 0):
            totalProfit += pnl
            countProfit += 1
        elif (pnl < 0):
            totalLoss += -pnl
            countLoss += 1

        return {'totalLoss': totalLoss, 'totalProfit': totalProfit,
                'countLoss': countLoss, 'countProfit': countProfit}
