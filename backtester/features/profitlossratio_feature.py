from backtester.features.feature import Feature


class ProfitLossRatioFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):

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
