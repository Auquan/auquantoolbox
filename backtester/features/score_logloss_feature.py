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

        predictionDf = instrumentLookbackData.getFeatureDf(predictionKey)
        featureDf = instrumentLookbackData.getFeatureDf(featureKey)
        targetDf = instrumentLookbackData.getFeatureDf(target)

        currentPrediction = predictionDf.iloc[-1]  # will have this
        prevFeatureData = featureDf.iloc[-1] if updateNum > 1 else zeroSeries  # might not have it
        prevCount = updateNum - 1

        temp = (prevCount) * prevFeatureData

        currentPrediction = currentPrediction.fillna(0.5)
        currentPrediction = currentPrediction.astype(float)

        y = targetDf.iloc[-1]
        y.replace('', np.nan, inplace=True)
        temp = temp - (np.log(currentPrediction) * y.astype(float) + np.log(1 - currentPrediction) * (1 - y.astype(float)))
        return temp / float(updateNum)

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
        score = instrumentLookbackData.getFeatureDf(scoreKey).iloc[-1].sum()
        allInstruments = instrumentManager.getAllInstrumentsByInstrumentId()
        return score / float(len(allInstruments))
