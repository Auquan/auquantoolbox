import os
import pandas as pd
from backtester.constants import *
from backtester.logger import *


class TargetVariableManager(object):
    """
    """
    def __init__(self, systemParams, instrumentIds=None, targetVariableFileName=None, targetVariablePath=None, chunkSize=None):
        self.systemParams = systemParams
        self.__targetVariablePath = targetVariablePath
        self.__chunkSize = chunkSize
        self.__firstChunk = True
        self.__instrumentData = None
        self.__lookBackInstrumentData = None
        targetVariableConfigs = systemParams.getTargetVariableConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        targetVariableKeys = map(lambda x: x.getFeatureKey(), targetVariableConfigs)
        self.readTargetVariables(targetVariableFileName, targetVariableKeys, instrumentIds)

    def getFeatureDf(self, featureKey):
        if self.__instrumentData is None:
            return None
        return self.__instrumentData[featureKey]

    def getTargetVariableByKey(self, targetVariableKey):
        return self.__targetVariables[targetVariableKey]

    def getAllTargetVariables(self):
        return self.__targetVariables

    def getMaxShiftFromConfigList(configList):
        maxShift = 0
        for config in configList:
            featureParams = config.getFeatureParams()
            maxShift = max(maxShift, featureParams.get('shift', 0))
        if maxShift == 0:
            return None
        return maxShift

    def readTargetVariables(self, fileNames, targetVariableKeys=None, instrumentIds=None):
        if isinstance(fileNames, list):
            for fileName in fileNames:
                key = os.path.basename(os.splitext(fileName))
                if key not in targetVariableKeys:
                    continue
                # NOTE: This kind of Target Variable must be: (timestamps x instrumentIds) for a targetVariableKey
                self.__targetVariables[key] = pd.read_csv(fileName, index_col=0, parse_dates=True, dtype=float,
                                                          usecols=instrumentIds, chunksize=self.__chunkSize)
        elif isinstance(fileNames, str):
            # NOTE: This kind of Target Variable must be: (timestamps x targetVariableKey) for a instrument
            self.__targetVariables = pd.read_csv(fileNames, index_col=0, parse_dates=True, dtype=float,
                                                 usecols=targetVariableKeys, chunksize=self.__chunkSize)
        else:
            self.__targetVariables = {key : None for key in targetVariableKeys}

    def writeTargetVariables(self, instrumentId=None):
        self.__targetVariablePath = '.' if self.__targetVariablePath is None else self.__targetVariablePath
        if isinstance(self.__targetVariables, dict):
            for key in self.__targetVariables:
                fileName = os.path.join(self.__targetVariablePath, key + '.csv')
                if self.__targetVariables[key] is None:
                    continue
                if self.__firstChunk:
                    self.__targetVariables[key].to_csv(fileName, mode='w')
                else:
                    self.__targetVariables[key].to_csv(fileName, mode='a', header=False)
        else:
            fileName = os.path.join(self.__targetVariablePath, instrumentId + '.csv')
            if self.__firstChunk:
                self.__targetVariables.to_csv(fileName, mode='w')
            else:
                self.__targetVariables.to_csv(fileName, mode='a', header=False)

    def updateInstrumentData(self, instrumentData):
        if self.__chunkSize is None:
            self.__instrumentData = instrumentData
            return None
        else:
            maxShift = self.getMaxShiftFromConfigList(targetVariableConfigs)
            if self.__lookBackInstrumentData is not None:
                self.__instrumentData = pd.concat([self.__lookBackInstrumentData, instrumentData])
            return maxShift

    def computeTargetVariables(self, updateNum, instrumentData, instrumentId=None, targetVariableConfigs=None, writeVariables=False):
        if targetVariableConfigs is None:
            targetVariableConfigs = self.systemParams.getTargetVariableConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)

        maxShift = self.updateInstrumentData(instrumentData)
        timeFrequency = instrumentData.getTimeFrequency()
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
            if maxShift is not None:
                self.__lookBackInstrumentData = instrumentData[-2*maxShift:]
                if self.__firstChunk:
                    self.__targetVariables[targetVariableKey] = self.__targetVariables[targetVariableKey][:(-maxShift)]
                else:
                    self.__targetVariables[targetVariableKey] = self.__targetVariables[targetVariableKey][maxShift:(-maxShift)]
        if writeVariables:
            self.writeTargetVariables(instrumentId)
        if self.__firstChunk:
            self.__firstChunk = False

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
