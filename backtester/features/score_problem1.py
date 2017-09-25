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
        return np.sqrt(pd.to_numeric(temp))

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
        score = instrumentLookbackData.getFeatureDf(scoreKey).iloc[-1]
        normalization = instrumentLookbackData.getFeatureDf(normalizationKey).iloc[-1]
        normalized_score = score * 0
        normalized_score[normalization == 0] = 1
        normalized_score[normalization != 0] = score / (normalization / 1000)
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
