from backtester.constants import *
from backtester.logger import *
import numpy as np
import pandas as pd

class MetricManager(object):

    def __init__(self, systemParams):
        self.systemParams = systemParams

    def getMetrics(self):
        return self.metricData

    def getKeysFromData(self, data):
        if isinstance(data, dict):
            return data.keys()
        elif isinstance(data, pd.DataFrame):
            return data.columns.tolist()
        else:
            raise ValueError

    def computeWorkingTimestamps(self, data):
        timestamps = None
        if isinstance(data, dict):
            for key in data:
                if timestamps is None:
                    timestamps = data[key].index
                else:
                    timestamps = data[key].index.intersection(timestamps)
        elif isinstance(data, pd.DataFrame) or isinstance(data, pd.Series):
            timestamps = data.index
        else:
            print("hello")
            return None
        return timestamps

    def calculateMetrics(self, targetVariablesData, predictedVariablesData, metricConfigs):
        score = {}
        for metricConfig in metricConfigs:
            metricKey = metricConfig.getKey()
            metricId = metricConfig.getId()
            metricParams = metricConfig.getParams()
            metricCls = metricConfig.getClassForMetricId(metricId)
            score[metricKey] = metricCls.computeMetrics(metricParams, targetVariablesData, predictedVariablesData)
        return score
