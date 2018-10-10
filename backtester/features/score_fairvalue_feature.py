from backtester.features.feature import Feature
from backtester.logger import *
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
        predictionDf = predictionDf.replace([np.nan, np.inf, -np.inf], 0)
        featureDf = featureDf.replace([np.nan, np.inf, -np.inf], 0)
        priceDf = priceDf.replace([np.nan, np.inf, -np.inf], 0)
        try:
            currentPrediction = predictionDf.iloc[-1]  # will have this
            prevFeatureData = featureDf.iloc[-1] if updateNum > 1 else zeroSeries  # might not have it
            prevCount = updateNum - 1
            temp = (prevCount) * (prevFeatureData**2)
            sqError = (currentPrediction - priceDf.iloc[-1])**2
            temp = (temp + sqError)
            if updateNum==0:
                return prevFeatureData
            temp = temp / updateNum
            return np.sqrt(temp)
        except IndexError:
            logError('Empty DataFrame')

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        score = 0
        scoreDict = instrumentManager.getDataDf()[featureKey]
        scoreDict = scoreDict.replace([np.nan, np.inf, -np.inf], 0)
        scoreKey = 'score'
        if 'instrument_score_feature' in featureParams:
            scoreKey = featureParams['instrument_score_feature']
        if len(scoreDict) <= 1:
            return 0
        cumulativeScore = scoreDict.values[-2]
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        try:
            score = instrumentLookbackData.getFeatureDf(scoreKey).iloc[-1].sum()
            allInstruments = instrumentManager.getAllInstrumentsByInstrumentId()
            if len(allInstruments)>0:
                cumulativeScore += score / len(allInstruments)
            else:
                cumulativeScore += score
            return score
        except IndexError:
            logError("scoreKey DataFrame is empty")
