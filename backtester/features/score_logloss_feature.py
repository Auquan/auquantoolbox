from backtester.features.feature import Feature
import numpy as np
import pandas as pd


class ScoreLogLossFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures() #mock
        instrumentDict = instrumentManager.getAllInstrumentsByInstrumentId() #dict
        zeroSeries = pd.Series([0] * len(instrumentDict), index=instrumentDict.keys()) #series
        predictionKey = 'prediction' #done
        target = 'Y' #done
        if 'predictionKey' in featureParams:
            predictionKey = featureParams['predictionKey']
        if 'target' in featureParams:
            target = featureParams['target']

        predictionDf = instrumentLookbackData.getFeatureDf(predictionKey) #df
        featureDf = instrumentLookbackData.getFeatureDf(featureKey) #df
        targetDf = instrumentLookbackData.getFeatureDf(target) #df
        predictionDf = predictionDf.replace([np.nan, np.inf, -np.inf], 0) #???
        featureDf = featureDf.replace([np.nan, np.inf, -np.inf], 0)
        targetDf = targetDf.replace([np.nan, np.inf, -np.inf], 0)
        try:
            currentPrediction = predictionDf.iloc[-1]  # will have this #series 9.06
            prevFeatureData = featureDf.iloc[-1] if updateNum > 1 else zeroSeries  # might not have it #series 8.0
            prevCount = updateNum - 1 #1
            temp = (prevCount) * prevFeatureData #8.0 float
            currentPrediction = currentPrediction.fillna(0.5) #9.06
            currentPrediction = currentPrediction.astype(float) #9.06
            y = targetDf.iloc[-1] #2.46 series
            y.replace('', np.nan, inplace=True) #2.46
            temp = temp - (np.log(currentPrediction) * y.astype(float) + np.log(1 - currentPrediction) * (1 - y.astype(float)))
            return temp / float(updateNum)
        except IndexError:
            raise IndexError('Empty DataFrame')

            #8-(    )
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
        score = instrumentLookbackData.getFeatureDf(scoreKey).iloc[-1].sum()
        allInstruments = instrumentManager.getAllInstrumentsByInstrumentId()
        return score / float(len(allInstruments))
