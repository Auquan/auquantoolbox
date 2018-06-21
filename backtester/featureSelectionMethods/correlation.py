import pandas as pd
from backtester.featureSelectionMethods.feature_interaction import FeatureInteraction
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
        startPeriod = params.get('startPeriod', PearsonCorrelation.START_PERIOD)
        endPeriod = params.get('endPeriod', PearsonCorrelation.END_PERIOD)
        steps = params.get('steps', PearsonCorrelation.STEPS)
        threshold = params.get('threshold', PearsonCorrelation.THRESHOLD)
        topK = params.get('top', None)

        targetVariableDf = dataManager.getTargetVariableDf(targetVariableKey)
        featureDf = dataManager.getFeatureDf(featureKeys)
        score = cls.computeInteractionScore(targetVariableDf, featureDf).abs()
        for period in range(startPeriod, endPeriod, steps):
            if period == 0:
                continue
            df1 = targetVariableDf.diff(periods=period)
            df2 = featureDf.diff(periods=period)
            score = pd.concat([score, cls.computeInteractionScore(df1, df2).abs()], axis=1).min(axis=1)
        if topK is None:
            return score[score >= threshold].index.tolist()
        else:
            return score.nlargest(topK).index.tolist()
