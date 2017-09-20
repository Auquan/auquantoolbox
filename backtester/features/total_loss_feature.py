from backtester.features.feature import Feature
import pandas as pd


class TotalLossFeature(Feature):

    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        pnlKey = 'pnl'
        if 'pnlKey' in featureParams:
            pnlKey = featureParams['pnlKey']
        prevData = instrumentLookbackData.getDataForFeatureForAllInstruments(featureKey)
        pnlData = instrumentLookbackData.getDataForFeatureForAllInstruments(pnlKey)

        if len(prevData) <= 1:
            totalLoss = pd.Series([0] * len(pnlData.columns), index=pnlData.columns)
            prevPnl = pd.Series([0] * len(pnlData.columns), index=pnlData.columns)
        else:
            totalLoss = prevData.iloc[-1]
            prevPnl = pnlData.iloc[-2]

        pnl = pnlData.iloc[-1] - prevPnl

        totalLoss[pnl < 0] = totalLoss + pnl

        return totalLoss

    @classmethod
    def computeForMarket(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()

        pnlKey = 'pnl'
        if 'pnlKey' in featureParams:
            pnlKey = featureParams['pnlKey']
        if len(lookbackDataDf) <= 1:
            prevData = 0
            prevPnl = 0
        else:
            prevData = lookbackDataDf[featureKey].iloc[-2]
            prevPnl = lookbackDataDf[pnlKey].iloc[-2]

        totalLoss = prevData
        pnl = lookbackDataDf[pnlKey].iloc[-1] - prevPnl

        if (pnl < 0):
            totalLoss += pnl

        return totalLoss
