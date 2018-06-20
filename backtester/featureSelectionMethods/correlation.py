import pandas as pd
from backtester.featureEngineering.feature_interaction import FeatureInteraction
from backtester.logger import *


class PearsonCorrelation(FeatureInteraction):
    # Defaults
    THRESHOLD = 0.1
    END_PERIOD = 1
    START_PERIOD = 0
    STEPS = 1

    @classmethod
    def computeInteractionScore(cls, variableDf1, variableDf2):
        return variableDf2.corrwith(variableDf1)

    @classmethod
    def extractImportantFeatures(cls, targetVariableKey, featureKeys, params, dataManager):
        startPeriod = params.get('startPeriod', START_PERIOD)
        endPeriod = params.get('endPeriod', END_PERIOD)
        steps = params.get('steps', STEPS)
        threshold = params.get('threshold', THRESHOLD)
        topK = params.get('top', None)

        variableDf1 = dataManager.getVariableDf(targetVariableKey)
        variableDf2 = dataManager.getVariableDf(featureKeys)
        score = cls.computeInteractionScore(variableDf1, variableDf2).abs()
        for period in range(startPeriod, endPeriod, steps):
            if period == 0:
                continue
            df1 = variableDf1.diff(periods=period)
            df2 = variableDf2.diff(periods=period)
            score = pd.concat([score, cls.computeInteractionScore(df1, df2).abs()], axis=1).min(axis=1)
        if topK is None:
            return score[score >= threshold].index.tolist()
        if else:
            return score.nlargest(topK).index.tolist()
