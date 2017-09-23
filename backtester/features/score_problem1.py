from backtester.features.feature import Feature
import numpy as np
import pandas as pd


class ProblemOneScore(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        instrumentDict = instrumentManager.getAllInstrumentsByInstrumentId()
        zeroSeries = pd.Series([0] * len(instrumentDict), index=instrumentDict.keys())
        predictionKey = 'prediction'
        price = 'close'
        if 'predictionKey' in featureParams:
            predictionKey = featureParams['predictionKey']
        if 'price' in featureParams:
            price = featureParams['price']

        predictionDf = instrumentLookbackData.getDataForFeatureForAllInstruments(predictionKey)
        featureDf = instrumentLookbackData.getDataForFeatureForAllInstruments(featureKey)
        priceDf = instrumentLookbackData.getDataForFeatureForAllInstruments(price)

        currentPrediction = predictionDf.iloc[-1]  # will have this
        prevFeatureData = featureDf.iloc[-1] if updateNum > 1 else zeroSeries  # might not have it
        prevCount = updateNum - 1
        temp = (prevCount) * (prevFeatureData**2)
        sqError = (currentPrediction - priceDf.iloc[-1])**2
        temp = (temp + sqError)
        temp = temp / updateNum
        return np.sqrt(temp)



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
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        score = 0
        scoreDict = instrumentManager.getDataDf()[featureKey]
        scoreKey = 'score'
        normalizationKey = 'benchmark_score'
        if 'instrument_score_feature' in featureParams:
            scoreKey = featureParams['instrument_score_feature']
        if 'benchmark_score_feature' in featureParams:
            normalizationKey = featureParams['benchmark_score_feature']
        if len(scoreDict) <= 1:
            return 0
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        score = instrumentLookbackData.getDataForFeatureForAllInstruments(scoreKey).iloc[-1]
        normalized_score = score / (instrumentLookbackData.getDataForFeatureForAllInstruments(normalizationKey).iloc[-1] / 1000)
        allInstruments = instrumentManager.getAllInstrumentsByInstrumentId()
        '''
        for instrumentId in allInstruments:
            instrument = allInstruments[instrumentId]
            lookbackDataDf = instrument.getDataDf()
            if lookbackDataDf[normalizationKey].iloc[-1] == 0:
                score += 1
            else:
                score += lookbackDataDf[scoreKey].iloc[-1] / (lookbackDataDf[normalizationKey].iloc[-1] / 1000)
         '''
        return normalized_score.sum() / float(len(allInstruments))
