from backtester.features.feature import Feature
import numpy as np
class ScoreRankFeature(Feature):

    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):      
        raise NotImplementedError
        return None

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        score = 0
        scoreDict = instrumentManager.getDataDf()[featureKey]
        predictionKey = 'prediction'
        priceKey = 'close'
        if 'predictionKey' in featureParams:
            predictionKey = featureParams['predictionKey']
        if 'price' in featureParams:
           priceKey = featureParams['price']
        if len(scoreDict) < 1:
            return 0
        cumulativeScore = scoreDict.values[-1]
        allInstruments = instrumentManager.getAllInstrumentsByInstrumentId()
        returns = pd.Series(0, index = allInstruments.keys())
        for instrumentId in allInstruments:
            instrument = allInstruments[instrumentId]
            lookbackDataDf = instrument.getDataDf()
            returns[instrumentId] = lookbackDataDf[priceKey].iloc[-1]/lookbackDataDf[priceKey].iloc[-2]

        returns.dropna(inplace=True)
        rank = returns.rank(ascending=False)
        p = instrumentManager.getDataDf()[prediction].iloc[-1]
        score = ((rank - p ) * (rank - rank.mean())).abs().sum() 
        cumulativeScore -= score/len(allInstruments)
        return score

