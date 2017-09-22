from backtester.features.feature import Feature
import numpy as np
import pandas as pd


class ScoreLogLossFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        instrumentDict = instrumentManager.getAllInstrumentsByInstrumentId()
        zeroSeries = pd.Series([0] * len(instrumentDict), index=instrumentDict.keys())
        predictionKey = 'prediction'
        target = 'Y'
        if 'predictionKey' in featureParams:
            predictionKey = featureParams['predictionKey']
        if 'target' in featureParams:
            target = featureParams['target']

        predictionDf = instrumentLookbackData.getDataForFeatureForAllInstruments(predictionKey)
        featureDf = instrumentLookbackData.getDataForFeatureForAllInstruments(featureKey)
        targetDf = instrumentLookbackData.getDataForFeatureForAllInstruments(target)

        currentPrediction = predictionDf.iloc[-1]  # will have this
        prevFeatureData = featureDf.iloc[-1] if updateNum > 1 else zeroSeries  # might not have it
        prevCount = updateNum - 1

        temp = (prevCount) * prevFeatureData

        currentPrediction.fillna(0.5)

        y = targetDf.iloc[-1]
        temp = temp - (np.log(currentPrediction) * float(y) + np.log(1 - currentPrediction) * float(1 - y))

        return float(temp) / float(updateNum)

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
        if len(scoreDict) < 1:
            return 0
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        score = instrumentLookbackData.getDataForFeatureForAllInstruments(scoreKey).iloc[-1].sum()
        allInstruments = instrumentManager.getAllInstrumentsByInstrumentId()
        return score / float(len(allInstruments))
