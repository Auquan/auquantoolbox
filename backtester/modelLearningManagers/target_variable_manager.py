import os
import pandas as pd
from backtester.constants import *
from backtester.logger import *


class TargetVariableManager(object):
    """
    Calculates or reads target variables
    * Data (instrumentData) can be fed to computeTargetVariables in two formats:
        1. For a instrument, a dataframe of shape: timeStamps x features
        2. A dictionary with keys as features and values as dataframe of shape: timeStamps x instrumentIds
        ** 2nd format is useful for calculating target variables efficiently when several models are being trained simulataneoulsy
    * Size of calculated target variables can be less than or equal to the size of instrumentData
    """
    def __init__(self, systemParams, instrumentIds=None, targetVariableFileName=None, targetVariablePath=None, chunkSize=None, dateRange=None):
        self.systemParams = systemParams
        self.__targetVariablePath = targetVariablePath
        self.__chunkSize = chunkSize
        self.__firstChunk = True
        self.__instrumentData = None
        self.__lookBackInstrumentData = None
        targetVariableConfigs = systemParams.getTargetVariableConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        targetVariableKeys = map(lambda x: x.getFeatureKey(), targetVariableConfigs)
        self.readTargetVariables(targetVariableFileName, targetVariableKeys, instrumentIds, dateRange)
        self.__leftoverChunk = {key : None for key in targetVariableKeys}

    def getFeatureDf(self, featureKey):
        if self.__instrumentData is None:
            return None
        return self.__instrumentData[featureKey]

    def getTargetVariableByKey(self, targetVariableKey):
        return self.__targetVariables[targetVariableKey]

    def getAllTargetVariables(self):
        return self.__targetVariables

    def getLeftoverTargetVariableChunk(self):
        return self.__leftoverChunk

    def getMaxPeriodAndShiftFromConfigList(self, configList):
        maxShift = 0
        maxPeriod = 0
        for config in configList:
            featureParams = config.getFeatureParams()
            maxShift = max(maxShift, featureParams.get('shift', 0))
            maxPeriod = max(maxPeriod, featureParams.get('period', 0))
        if maxShift == 0 and maxPeriod == 0:
            return None, None
        maxPeriod = max(2*maxShift, maxPeriod)
        maxShift = None if maxShift == 0 else maxShift
        return maxShift, maxPeriod

    def getIndexColumnName(self, fileName):
        return pd.read_csv(fileName, nrows=1).columns.tolist()[0]

    def readTargetVariables(self, fileNames, targetVariableKeys=None, instrumentIds=None, dateRange=None):
        if isinstance(fileNames, list):
            for fileName in fileNames:
                key = os.path.basename(os.splitext(fileName))
                if key not in targetVariableKeys:
                    continue
                indexColumn = self.getIndexColumnName(fileName)
                usecols = instrumentIds if instrumentIds is None else [indexColumn] + instrumentIds
                # NOTE: This kind of Target Variable must be: [timestamps x instrumentIds] for a targetVariableKey
                self.__targetVariables[key] = pd.read_csv(fileName, index_col=0, parse_dates=True, dtype=float,
                                                          usecols=usecols, chunksize=self.__chunkSize)
                self.__targetVariables[key] = self.filterTargetVariablesByDates(self.__targetVariables[key], dateRange)
        elif isinstance(fileNames, str):
            indexColumn = self.getIndexColumnName(fileNames)
            usecols = targetVariableKeys if targetVariableKeys is None else [indexColumn] + targetVariableKeys
            # NOTE: This kind of Target Variable must be: [timestamps x targetVariableKey(s)] for a instrument
            self.__targetVariables = pd.read_csv(fileNames, index_col=0, parse_dates=True, dtype=float,
                                                 usecols=usecols, chunksize=self.__chunkSize)
            self.__targetVariables = self.filterTargetVariablesByDates(self.__targetVariables, dateRange)
        else:
            self.__targetVariables = {key : None for key in targetVariableKeys}

    def filterTargetVariablesByDates(self, data, dateRange):
        if dateRange is None:
            return data
        elif type(dateRange) is list and type(dateRange[0]) is tuple:
            frames = []
            for dr in dateRange:
                frames.append(data[dr[0]:dr[1]])
            return pd.concat(frames)
        else:
            return data[dateRange[0]:dateRange[1]]

    def writeTargetVariables(self, instrumentId=None):
        self.__targetVariablePath = '.' if self.__targetVariablePath is None else self.__targetVariablePath
        if isinstance(self.__targetVariables, dict):
            if instrumentId is None:
                # save targetVariables with filename as targetVariableKey and data in format (timeStamps x instrumentIds)
                for key in self.__targetVariables:
                    fileName = os.path.join(self.__targetVariablePath, key + '.csv')
                    if self.__targetVariables[key] is None:
                        continue
                    if self.__firstChunk:
                        self.__targetVariables[key].to_csv(fileName, mode='w', float_format=FLOAT_FORMAT)
                    else:
                        self.__targetVariables[key].to_csv(fileName, mode='a', header=False, float_format=FLOAT_FORMAT)
            else:
                # save targetVariables with filename as instrumentId and data in format (timeStamps x targetVariableKeys)
                # BUG: This part of code may not work when there is only one instrumentId in self.__targetVariables dataframes
                # TODO: Check and fix it
                targetVariableDf = pd.concat([self.__targetVariables[key][instrumentId] for key in self.__targetVariables], axis=1)
                targetVariableDf.columns = self.__targetVariables.keys()
                fileName = os.path.join(self.__targetVariablePath, instrumentId + '.csv')
                if self.__firstChunk:
                    self.__targetVariables.to_csv(fileName, mode='w', float_format=FLOAT_FORMAT)
                else:
                    self.__targetVariables.to_csv(fileName, mode='a', header=False, float_format=FLOAT_FORMAT)
        else:
            fileName = os.path.join(self.__targetVariablePath, instrumentId + '.csv')
            if self.__firstChunk:
                self.__targetVariables.to_csv(fileName, mode='w', float_format=FLOAT_FORMAT)
            else:
                self.__targetVariables.to_csv(fileName, mode='a', header=False, float_format=FLOAT_FORMAT)

    def updateInstrumentData(self, instrumentData, targetVariableConfigs):
        if self.__chunkSize is None:
            self.__instrumentData = instrumentData
            return None, None
        else:
            maxShift, maxPeriod = self.getMaxPeriodAndShiftFromConfigList(targetVariableConfigs)
            if self.__lookBackInstrumentData is None:
                self.__instrumentData = instrumentData
            else:
                self.__instrumentData = pd.concat([self.__lookBackInstrumentData, instrumentData])
            return maxShift, maxPeriod

    def computeTargetVariables(self, updateNum, instrumentData, instrumentId=None, targetVariableConfigs=None, timeFrequency=None, writeVariables=False):
        if targetVariableConfigs is None:
            targetVariableConfigs = self.systemParams.getTargetVariableConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)

        maxShift, maxPeriod = self.updateInstrumentData(instrumentData, targetVariableConfigs)
        for targetVariableConfig in targetVariableConfigs:
            targetVariableKey = targetVariableConfig.getFeatureKey()
            targetVariableParams = targetVariableConfig.getFeatureParams()
            period = targetVariableParams.get('period', None)
            # TODO: Use the below code to calculate features using time frequency also
            # if period is not None and timeFrequency is not None:
                # try:
                    # targetVariableParams['period'] = '%d%s' % (int(period), timeFrequency)
                # except:
                    # pass
            featureId = targetVariableConfig.getFeatureId()
            featureCls = targetVariableConfig.getClassForFeatureId(featureId)
            self.__targetVariables[targetVariableKey]  = featureCls.computeForInstrumentData(updateNum=updateNum,
                                                                                        featureParams=targetVariableParams,
                                                                                        featureKey=targetVariableKey,
                                                                                        featureManager=self)
            shift = targetVariableParams.get('shift', 0)
            if shift > 0:
                self.shiftTargetVariable(targetVariableKey, shift, timeFrequency)
            if maxPeriod is not None or maxShift is not None:
                self.__lookBackInstrumentData = instrumentData[-maxPeriod:]
                if maxShift is not None:
                    self.__leftoverChunk[targetVariableKey] = self.__targetVariables[targetVariableKey][(-maxShift):]
                    if self.__firstChunk:
                        self.__targetVariables[targetVariableKey] = self.__targetVariables[targetVariableKey][:(-maxShift)]
                    else:
                        self.__targetVariables[targetVariableKey] = self.__targetVariables[targetVariableKey][(maxPeriod-maxShift):(-maxShift)]
            self.__targetVariables[targetVariableKey].dropna(inplace=True)
        if writeVariables:
            self.writeTargetVariables(instrumentId)
        if self.__firstChunk:
            self.__firstChunk = False

    def shiftTargetVariable(self, key, shift, timeFrequency):
        tempDf = self.__targetVariables[key].shift(-shift, freq=timeFrequency)
        if isinstance(tempDf, pd.Series):
            self.__targetVariables[key] = pd.Series(index=self.__targetVariables[key].index)
        elif isinstance(tempDf, pd.DataFrame):
            self.__targetVariables[key] = pd.DataFrame(index=self.__targetVariables[key].index,
                                                       columns=self.__targetVariables[key].columns)
        else:
            raise ValueError
        self.__targetVariables[key].update(tempDf)
        self.__targetVariables[key].fillna(method='ffill', inplace=True)

    def flushTargetVariables(self):
        keys = list(self.__targetVariables.keys())
        for key in keys:
            del self.__targetVariables[key]
        del self.__targetVariables
        self.__targetVariables = {}
