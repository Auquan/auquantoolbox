from feature import Feature
import numpy as np
class ScoreLogLossFeature(Feature):

    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):      
        lookbackDataDf = instrument.getDataDf()
        predictionKey = 'prediction'
        price = 'close'
        if 'predictionKey' in featureParams:
            predictionKey = featureParams['predictionKey']
        if 'price' in featureParams:
            price = featureParams['price']
        prevData = lookbackDataDf[featureKey].iloc[-1]
        prevCount = lookbackDataDf[countKey].iloc[-1]
        temp = prevCount*prevData
        prevCount+=1
        p = lookbackDataDf[prediction].iloc[-1]
        y = 1 if lookbackDataDf[price].iloc[-1] < currentFeatures[price] else 0
        temp = temp + (np.log(p)*y + log(1-p)*(1-y))
        return float(temp)/float(prevCount)

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        score = 0
        scoreDict = instrumentManager.getDataDf()[featureKey]
        scoreKey = 'score'
        if 'instrument_score_feature' in featureParams:
           scoreKey = featureParams['instrument_score_feature']
        if len(scoreDict) < 1:
            return 0
        cumulativeScore = scoreDict.values[-1]
        allInstruments = instrumentManager.getAllInstrumentsByInstrumentId()
        for instrumentId in allInstruments:
            instrument = allInstruments[instrumentId]
            lookbackDataDf = instrument.getDataDf()
            score += instrument.getDataDf()[scoreKey][-1]
        cumulativeScore += score/len(allInstruments)
        return score

