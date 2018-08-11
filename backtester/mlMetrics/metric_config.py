from backtester.configurator import Configurator
from backtester.mlMetrics.metric import Metric
from backtester.logger import *
from backtester.mlMetrics.classificationMetrics.accuracy_score_metric import AccuracyScoreMetric
from backtester.mlMetrics.regressionMetrics.explained_variance_score_metric import ExplainedVarianceScoreMetric


metricIdToClassDict = {'accuracy_score' : AccuracyScoreMetric,
                       'explained_variance_score': ExplainedVarianceScoreMetric}


class MetricConfig(Configurator):
    """
    Configures metric dicts
    """

    customIdToClassDict = {}

    def __init__(self, configDict):
        super(MetricConfig, self).__init__()

        if 'metricId' not in configDict:
            logError('metricId missing in config dictionary %s', configDict['metricKey'])
            # TODO:  Raise appropriate error
        self._identifier = configDict['metricId']

        self._key = configDict.get('metricKey', self._identifier)
        self._params = configDict.get('params', {})

    @classmethod
    def setupCustomMetricMethods(cls, customIdToClass):
        MetricConfig.customIdToClassDict.update(customIdToClass)

    @classmethod
    def getClassForMetricId(cls, metricId):
        if metricId in MetricConfig.customIdToClassDict:
            return MetricConfig.customIdToClassDict[metricId]
        return cls.getClassForId(metricId, metricIdToClassDict, Metric)
