from backtester.features.feature import Feature
from backtester.logger import *
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
        predictionDf = predictionDf.replace([np.nan, np.inf, -np.inf], 0)
        featureDf = featureDf.replace([np.nan, np.inf, -np.inf], 0)
        targetDf = targetDf.replace([np.nan, np.inf, -np.inf], 0)
        try:
            currentPrediction = predictionDf.iloc[-1]
            prevFeatureData = featureDf.iloc[-1] if updateNum > 1 else zeroSeries
            prevCount = updateNum - 1
            temp = (prevCount) * prevFeatureData
            currentPrediction = currentPrediction.fillna(0.5)
            currentPrediction = currentPrediction.astype(float)
            y = targetDf.iloc[-1]
            y.replace('', np.nan, inplace=True)
            temp = temp - (np.log(currentPrediction).replace([np.inf,-np.inf,np.nan],0) * y.astype(float) + np.log(1 - currentPrediction).replace([np.inf,-np.inf,np.nan],0) * (1 - y.astype(float)))
            if updateNum==0:
                return zeroSeries
            return temp / float(updateNum)
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
        if len(scoreDict) < 1:
            return 0
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        try:
            score = instrumentLookbackData.getFeatureDf(scoreKey).iloc[-1].sum()
            allInstruments = instrumentManager.getAllInstrumentsByInstrumentId()
            if len(allInstruments)==0:
                return score
            return score / float(len(allInstruments))
        except IndexError:
            logError("The scoreKey DataFrame is Empty")
