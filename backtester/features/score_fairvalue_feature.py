from backtester.features.feature import Feature
import numpy as np
import pandas as pd


class ScoreFairValueFeature(Feature):

    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        numInstruments = len(instrumentManager.getAllInstrumentsByInstrumentId())
        predictionKey = 'prediction'
        price = 'close'
        countKey = 'count'
        lookbackMarketDataDf = instrumentManager.getDataDf()
        if 'predictionKey' in featureParams:
            predictionKey = featureParams['predictionKey']
        if 'price' in featureParams:
            price = featureParams['price']
        if 'countKey' in featureParams:
            countKey = featureParams['countKey']
        if len(lookbackMarketDataDf) < 1:
            # first iteration
            return [0] * numInstruments
        predictionDict = lookbackMarketDataDf[predictionKey].iloc[-1]
        # lookback market data is not updated yet since we are in instrument updates
        # therefore the count is previous count.
        prevCount = lookbackMarketDataDf[countKey].iloc[-1]
        if len(predictionDict) == 0:
            return [0] * numInstruments
        prevData = instrumentLookbackData.getDataForFeatureForAllInstruments(featureKey).iloc[-1]
        temp = (prevCount) * (prevData**2)
        sqError = (pd.Series(predictionDict) - instrumentLookbackData.getDataForFeatureForAllInstruments(price).iloc[-2])**2
        temp = (temp + sqError)
        # print(currentFeatures[price], lookbackDataDf[price].iloc[-1])
        temp = temp/(prevCount + 1)
        return temp
        # TODO KANAV
        return np.sqrt(temp)
        #return np.sqrt(temp / (prevCount + 1))


    '''
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):
        lookbackDataDf = instrument.getDataDf()
        predictionKey = 'prediction'
        price = 'close'
        countKey = 'count'
        if len(lookbackDataDf) < 1 or instrumentManager is None:
            return 0
        lookbackMarketDataDf = instrumentManager.getDataDf()
        if 'predictionKey' in featureParams:
            predictionKey = featureParams['predictionKey']
        if 'price' in featureParams:
            price = featureParams['price']
        if 'countKey' in featureParams:
            countKey = featureParams['countKey']
        if len(lookbackMarketDataDf) < 1:
            # first iteration
            return 0
        predictionDict = lookbackMarketDataDf[predictionKey].iloc[-1]
        # lookback market data is not updated yet since we are in instrument updates
        # therefore the count is previous count.
        prevCount = lookbackMarketDataDf[countKey].iloc[-1]
        if len(predictionDict) == 0:
            return 0
        prevData = lookbackDataDf[featureKey].iloc[-2]

        temp = (prevCount) * (prevData**2)

        sqError = (predictionDict[instrument.getInstrumentId()] - lookbackDataDf[price].iloc[-2])**2
        temp = (temp + sqError)
        # print(currentFeatures[price], lookbackDataDf[price].iloc[-1])
        return np.sqrt(float(temp) / float(prevCount+1))
    '''

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
        if len(scoreDict) <= 1:
            return 0
        cumulativeScore = scoreDict.values[-2]
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        score = instrumentLookbackData.getDataForFeatureForAllInstruments(scoreKey).iloc[-1].sum()
        allInstruments = instrumentManager.getAllInstrumentsByInstrumentId()
        cumulativeScore += score / len(allInstruments)
        return score
