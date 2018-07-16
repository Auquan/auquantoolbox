from backtester.constants import *
from backtester.logger import *
import numpy as np
import pandas as pd

class MetricManager(object):

    def __init__(self, systemParams):
        self.systemParams = systemParams
        self.metricData = {}

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

    def calculateMetrics(self, targetVariablesData, predictedVariablesData, modelConfigs, metricConfigs = None):
        if metricConfigs is None:
            metricConfigs = self.systemParams.getMetricConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)

        for modelConfig in modelConfigs:
            key = modelConfig.getKey()
            timestamps = self.computeWorkingTimestamps(targetVariablesData)
            if timestamps is not None and (isinstance(predictedVariablesData[key], pd.DataFrame) or isinstance(predictedVariablesData[key], pd.Series)):
                predictedVariablesData[key] = predictedVariablesData[key].loc[timestamps]
            for metricConfig in metricConfigs:
                metricKey = metricConfig.getKey()
                metricId = metricConfig.getId()
                metricParams = metricConfig.getParams()
                metricCls = metricConfig.getClassForMetricId(metricId)

                self.metricData = metricCls.computeMetrics(metricParams, targetVariablesData, predictedVariablesData[key])
            print(self.metricData)
