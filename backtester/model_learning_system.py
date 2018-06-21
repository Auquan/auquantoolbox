import sys, os
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from backtester.model_learning_system_parameters import ModelLearningSystemParamters
from backtester.target_variable_manager import TargetVariableManager
from backtester.feature_selection_manager import FeatureSelectionManager
from backtester.constants import *

class ModelLearningSystem:
    def __init__(self, mlsParams, chunkSize=None):
        self.mlsParams = mlsParams
        self.__trainingDataSource = mlsParams.getTrainingDataSource()
        self.__chunkSize = chunkSize
        self.__targetVariableManager = TargetVariableManager(mlsParams, instrumentIds=mlsParams.instrumentIds, chunkSize=self.__chunkSize)
        self.__featureSelectionManager = FeatureSelectionManager(mlsParams)

    def getTrainingInstrurmentData(self, instrumentId):
        return self.__trainingDataSource.getInstrumentUpdates(instrumentId, self.__chunkSize)

    def getTargetVariables(self, targetVariableConfigs):
        targetVariableConfigs = targetVariableConfigs if isinstance(targetVariableConfigs, list) else [targetVariableConfigs]
        targetVariableKeys = map(lambda x: x.getFeatureKey(), targetVariableConfigs)
        targetVariable = {}
        for key in targetVariableKeys:
            targetVariable[key] = self.__targetVariableManager.getTargetVariableByKey(key)
        return targetVariable

    def computeTargetVariables(self, instrumentData, instrumentId, targetVariableConfigs, useTimeFrequency=True):
        timeFrequency = instrumentData.getTimeFrequency() if useTimeFrequency else None
        if self.__chunkSize is None:
            self.__targetVariableManager.computeTargetVariables(0, instrumentData.getBookData(), instrumentId,
                                                                targetVariableConfigs, timeFrequency)
            targetVariable = self.getTargetVariables(targetVariableConfigs)
            print(targetVariable)
            return
        for chunkNumber, instrumentDataChunk in instrumentData.getBookDataChunk():
            self.__targetVariableManager.computeTargetVariables(chunkNumber, instrumentDataChunk, instrumentId,
                                                                targetVariableConfigs, timeFrequency)
            targetVariable = self.getTargetVariables(targetVariableConfigs)
            print(chunkNumber, targetVariable)
        targetVariable = self.__targetVariableManager.getLeftoverTargetVariableChunk()
        print(chunkNumber+1, targetVariable)

    def getFeatureSet(self):
        return self.mlsParams.features

    def findBestModel(self, instrumentId, useTimeFrequency=True):
        instrumentData = self.getTrainingInstrurmentData(instrumentId)[instrumentId]
        targetVariableConfigs = self.mlsParams.getTargetVariableConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        self.computeTargetVariables(instrumentData, instrumentId, targetVariableConfigs, useTimeFrequency)
        self.__featureSelectionManager.pruneFeatures(instrumentData.getBookData(), self.getTargetVariables(targetVariableConfigs))
        selectedFeatures = self.__featureSelectionManager.getAllSelectedFeatures()
        print(selectedFeatures)

    def getFinalMetrics(self):
        pass

if __name__ == '__main__':
    instrumentIds = ['IBM', 'AAPL']
    startDateStr = '2014/07/10'
    endDateStr = '2017/10/07'
    chunkSize = 100
    mlsParams = ModelLearningSystemParamters(instrumentIds, 'XYZ', chunkSize=chunkSize)
    params = dict(cachedFolderName='yahooData/',
                 dataSetId='testTrading',
                 instrumentIds=instrumentIds,
                 startDateStr=startDateStr,
                 endDateStr=endDateStr,
                 liveUpdates=False)
    mlsParams.initializeDataSource('YahooStockDataSource', **params)

    system1 = ModelLearningSystem(mlsParams, chunkSize=None)
    print(system1.getTrainingInstrurmentData('IBM')['IBM'].getBookData())
    system1.findBestModel('IBM')
