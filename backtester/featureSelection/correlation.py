import pandas as pd
from backtester.featureSelection.feature_selection import FeatureSelection
from backtester.logger import *


class PearsonCorrelation(FeatureSelection):
    # Defaults
    THRESHOLD = 0.1
    END_PERIOD = 1
    START_PERIOD = 0
    STEPS = 1

    @classmethod
    def computeInteractionScore(cls, variableDf1, variableDf2):
        return variableDf1.corrwith(variableDf2)

    @classmethod
    def extractImportantFeatures(cls, targetVariableKey, featureKeys, params, dataManager):
        startPeriod = params.get('startPeriod', cls.START_PERIOD)
        endPeriod = params.get('endPeriod', cls.END_PERIOD)
        steps = params.get('steps', cls.STEPS)
        threshold = params.get('threshold', cls.THRESHOLD)
        topK = params.get('topK', None)

        targetVariableDf = dataManager.getTargetVariableDf(targetVariableKey)
        featureDf = dataManager.getFeatureDf(featureKeys)
        score = cls.computeInteractionScore(featureDf, targetVariableDf).abs()
        for period in range(startPeriod, endPeriod, steps):
            if period == 0:
                continue
            df1 = featureDf.diff(periods=period)
            df2 = targetVariableDf.diff(periods=period)
            score = pd.concat([score, cls.computeInteractionScore(df1, df2).abs()], axis=1).min(axis=1)
        # print(score)
        if topK is None:
            return score[score >= threshold].index.tolist()
        else:
            return score.nlargest(topK).index.tolist()
