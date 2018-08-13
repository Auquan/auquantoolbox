from backtester.features.feature import Feature
import pandas as pd
import numpy as np

class ProfitLossFeature(Feature):

    '''
    Computing for Instrument.
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        priceDict = instrumentLookbackData.getFeatureDf(featureParams['price'])
        priceDict = priceDict.replace([np.nan, np.inf, -np.inf], 0)
        try:
            zeroSeries = priceDict.iloc[-1] * 0
            pnlDict = instrumentLookbackData.getFeatureDf(featureKey)
            pnlDict = pnlDict.replace([np.nan, np.inf, -np.inf], 0)
            cumulativePnl = zeroSeries if (len(pnlDict.index) < 1) else pnlDict.iloc[-1]
            fees = instrumentLookbackData.getFeatureDf(featureParams['fees']).iloc[-1]
            fees = fees.replace([np.nan, np.inf, -np.inf], 0)
            positionDict = instrumentLookbackData.getFeatureDf('position')
            positionDict = positionDict.replace([np.nan, np.inf, -np.inf], 0)
            currentPosition = positionDict.iloc[-1]
            previousPosition = positionDict.iloc[-2] if (len(positionDict.index) > 1) else zeroSeries
            previousPrice = priceDict.iloc[-2] if (len(priceDict.index) > 1) else zeroSeries
            currentPrice = priceDict.iloc[-1]
            changeInPosition = currentPosition - previousPosition
            tradePrice = pd.Series([instrumentManager.getInstrument(x).getLastTradePrice() for x in priceDict.columns], index=priceDict.columns)
            tradeLoss = pd.Series([instrumentManager.getInstrument(x).getLastTradeLoss() for x in priceDict.columns], index=priceDict.columns)
            pnl = (previousPosition * (currentPrice - previousPrice)) + (changeInPosition * (currentPrice - tradePrice)) - fees - tradeLoss
            cumulativePnl += pnl
            return cumulativePnl
        except IndexError:
        		raise IndexError("Dataframe is empty")
    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        pnlDict = instrumentManager.getDataDf()[featureKey]
        pnlKey = 'pnl'
        if 'instrument_pnl_feature' in featureParams:
            pnlKey = featureParams['instrument_pnl_feature']
        if len(pnlDict) < 1:
            return 0
        return instrumentManager.getLookbackInstrumentFeatures().getFeatureDf(pnlKey).iloc[-1].sum()
