import pandas as pd
from backtester.constants import *
from backtester.logger import *


class TargetVariableManager(object):
    """
    """
    def __init__(self, systemParams, targetVariablesFileName='', chunkSize=None):
        self.systemParams = systemParams
        self.__instrumentData = None
        self.__chunkSize = chunkSize
        targetVariableConfigs = systemParams.getTargetVariableConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        targetVariableKeys = map(lambda x: x.getFeatureKey(), targetVariableConfigs)
        # self.__keyToConfigMap = {key : config for key, config in zip(targetVariableKeys, targetVariableConfigs)}
        if targetVariablesFileName is not '':
            self.readTargetVariables(targetVariablesFileName, targetVariableKeys)
        else:
            self.__targetVariables = {key : None for key in targetVariableKeys}

    def getFeatureDf(self, featureKey):
        if self.__instrumentData is None:
            return None
        return self.__instrumentData[featureKey]

    def getTargetVariableByKey(self, targetVariableKey):
        return self.__targetVariables[targetVariableKey]

    def getAllTargetVariables(self):
        return self.__targetVariables

    def readTargetVariables(self, fileName, columns=None):
        columns = None if columns == [] else columns
        self.__targetVariables = pd.read_csv(fileName, index_col=0, parse_dates=True,
                                             dtype=float, usecols=columns, chunksize=self.__chunkSize)

    def computeTargetVariables(self, updateNum, instrumentData, targetVariableConfigs=None, writeVariables=False):
        self.__instrumentData = instrumentData
        timeFrequency = instrumentData.getTimeFrequency()
        if targetVariableConfigs is None:
            targetVariableConfigs = self.systemParams.getTargetVariableConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        for targetVariableConfig in targetVariableConfigs:
            targetVariableKey = targetVariableConfig.getFeatureKey()
            targetVariableParams = targetVariableConfig.getFeatureParams()
            period = targetVariableParams.get('period', None)
            if period is not None and timeFrequency is not None:
                targetVariableParams['period'] = '%d%s' % (int(period), timeFrequency)
            featureId = targetVariableConfig.getFeatureId()
            featureCls = targetVariableConfig.getClassForFeatureId(featureId)
            self.__targetVariables[targetVariableKey]  = featureCls.computeForInstrumentData(updateNum=updateNum,
                                                                                        featureParams=targetVariableParams,
                                                                                        featureKey=targetVariableKey,
                                                                                        featureManager=self)
            shift = targetVariableParams.get('shift', None)
            if shift is not None and shift > 0:
                self.shiftTargetVariable(targetVariableKey, shift, timeFrequency)

    def shiftTargetVariable(self, key, shift, timeFrequency):
        tempDf = self.__targetVariables[key].shift(-shift, freq=timeFrequency)
        if isinstance(tempdf, pd.Series):
            self.__targetVariables[key] = pd.Series(index=self.__targetVariables[key].index)
        elif isinstance(tempDf, pd.DataFrame):
            self.__targetVariables[key] = pd.DataFrame(index=self.__targetVariables[key].index,
                                                              columns=self.__targetVariables[key].columns)
        else:
            raise ValueError
        self.__targetVariables[key].update(tempDf)
        self.__targetVariables[key].fillna(method='ffill', inplace=True)

    def shiftTargetVariableV2(self, key, shift, timeFrequency):
        self.__targetVariables[key].update(self.__targetVariables[key].shift(-shift, freq=timeFrequency))
        if isinstance(self.__targetVariables[key], pd.Series):
            self.__targetVariables[key][-shift:] = self.__targetVariables[key][-(shift+1)]
        elif isinstance(self.__targetVariables[key], pd.DataFrame):
            self.__targetVariables[key].iloc[-shift:] = self.__targetVariables[key].iloc[-(shift+1)].values
