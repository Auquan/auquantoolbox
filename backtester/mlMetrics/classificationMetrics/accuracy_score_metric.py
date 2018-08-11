from sklearn.metrics import *
from backtester.mlMetrics.metric import Metric
from backtester.logger import *

class AccuracyScoreMetric(Metric):

    NORMALISE = True

    @classmethod
    def computeMetrics(cls, params, trueValues, predictedValues):
        normalise = params.get('normalise', cls.NORMALISE)
        return accuracy_score(trueValues, predictedValues, normalise)
