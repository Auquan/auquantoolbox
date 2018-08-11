from sklearn.metrics import *
from backtester.mlMetrics.metric import Metric
from backtester.logger import *

class ExplainedVarianceScoreMetric(Metric):


    @classmethod
    def computeMetrics(cls, params, trueValues, predictedValues):
        return explained_variance_score(trueValues, predictedValues, multioutput = 'uniform_average')
