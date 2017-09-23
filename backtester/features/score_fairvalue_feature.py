from backtester.features.feature import Feature
import numpy as np
import pandas as pd


class ScoreFairValueFeature(Feature):

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

        predictionDf = instrumentLookbackData.getFeatureDf(predictionKey)
        featureDf = instrumentLookbackData.getFeatureDf(featureKey)
        priceDf = instrumentLookbackData.getFeatureDf(price)

        currentPrediction = predictionDf.iloc[-1]  # will have this
        prevFeatureData = featureDf.iloc[-1] if updateNum > 1 else zeroSeries  # might not have it
        prevCount = updateNum - 1
        temp = (prevCount) * (prevFeatureData**2)
        sqError = (currentPrediction - priceDf.iloc[-1])**2
        temp = (temp + sqError)
        temp = temp / updateNum
        return np.sqrt(temp)

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        score = 0
        scoreDict = instrumentManager.getDataDf()[featureKey]
        scoreKey = 'score'
        if 'instrument_score_feature' in featureParams:
            scoreKey = featureParams['instrument_score_feature']
        if len(scoreDict) <= 1:
            return 0
        cumulativeScore = scoreDict.values[-2]
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        score = instrumentLookbackData.getFeatureDf(scoreKey).iloc[-1].sum()
        allInstruments = instrumentManager.getAllInstrumentsByInstrumentId()
        cumulativeScore += score / len(allInstruments)
        return score
