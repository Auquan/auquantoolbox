import os, gc
import pandas as pd
import numpy as np
from backtester.logger import *
from backtester.instrumentUpdates.instrument_data import InstrumentData


class InstrumentDataManager(object):
    '''
    '''
    def __init__(self, dataParser, features, instrumentIds, featureFolderName='features'):
        self.__cachedFolderName = dataParser._cachedFolderName
        self.__dataSetId = dataParser._dataSetId
        self.__timeStamps = dataParser._allTimes
        self.__instrumentIds = instrumentIds
        self.__featureFolderName = featureFolderName
        self.__features = features
        self.__instrumentDataByFeature = {feature : None for feature in features}
        self.__instrumentDataChunkByFeature = {feature : None for feature in features}
        # self.__instrumentDataChunkCounter = {feature : None for feature in features}
        self.__instrumentDataGenerator = {feature : None for feature in features}
        self.__instrumentDataByInstrument = {instrumentId : None for instrumentId in instrumentIds}
        # self.__instrumentDataByInstrument = {instrumentId : pd.DataFrame(columns=features) for instrumentId in instrumentIds}


    def getFilePath(self, fileName, newDir=''):
        return os.path.join(self.__cachedFolderName, self.__dataSetId, self.__featureFolderName, newDir, fileName + '.csv')

    def getTemporaryFileName(self, fname, *fnames):
        tempFileName = str(fname)
        for name in fnames:
            tempFileName = tempFileName + "_" + str(name)
        return tempFileName

    # returns simulator (generator) to simulate feature calculations in chunks
    # NOTE: This assumes all instruments have same set of timeStamps (index)
    def getSimulator(self, chunkSize):
        for feature in self.__features:
            self.__instrumentDataGenerator[feature] = self.getInstrumentDataGenerator(feature, chunkSize)
        return self.getInstrumentDataInChunks(pd.Series(self.__timeStamps), chunkSize)

    # returns a chunk of all instruments data with feature as featureKey
    def getInstrumentDataChunkByFeature(self, featureKey):
        if self.__instrumentDataChunkByFeature[featureKey] is None:
            self.updateInstrumentDataChunk(featureKey)
        return self.__instrumentDataChunkByFeature[featureKey]

    # updates the instrumentBookDataChunk using its feature generator
    def updateInstrumentDataChunk(self, featureKey):
        if self.__instrumentDataGenerator[featureKey] is None:
            self.__instrumentDataChunkByFeature[featureKey] = None
            return
        try :
            self.__instrumentDataChunkByFeature[featureKey] = next(self.__instrumentDataGenerator[featureKey])
            # self.__instrumentDataChunkCounter[featureKey] = chunkNumber
        except StopIteration:
            self.__instrumentDataChunkByFeature[featureKey] = None

    # dumps the chunk of all instrument data and releases the memory
    def dumpInstrumentDataChunk(self):
        for featureKey in self.__features:
            del self.__instrumentDataChunkByFeature[featureKey]
            self.__instrumentDataChunkByFeature[featureKey] = None
        gc.collect()

    # helper method to create and return generator if its data exists
    def getInstrumentDataGenerator(self, featureKey, chunkSize):
        if self.__instrumentDataByFeature[featureKey] is None:
            return None
        return self.getInstrumentDataInChunks(self.__instrumentDataByFeature[featureKey], chunkSize)

    # a generator to return a chunk from already completely loaded book data features
    def getInstrumentDataInChunks(self, instrumentData, chunkSize):
        if (chunkSize < 0) or (chunkSize is None):
            logError("[InstrumentDataManager] chunkSize must be a non-negative integer")
        if instrumentData is None:
            logError("[InstrumentDataManager] instrument data is not available")
        if chunkSize = 0:
            yield (chunkSize, instrumentData)
        groups = np.arange(len(instrumentData)) // chunkSize
        for chunkNumber, instrumentDataChunk in instrumentData.groupby(groups):
            yield (chunkNumber, instrumentDataChunk)

    def addFeatureValueForAllInstruments(self, featureKey, data):
        self.__instrumentDataByFeature[featureKey] = data

    def addAllFeaturesForInstrument(self, instrumentId, data):
        self.__instrumentDataByInstrument[instrumentId] = data

    def transformInstrumentData(self):
        for instrumentId in self.__instrumentIds:
            frames = []
            columns = []
            for feature in self.__features:
                if self.__instrumentDataChunkByFeature[feature] is not None:
                    frames.append(self.__instrumentDataChunkByFeature[feature][instrumentId])
                    columns.append(feature)
            self.__instrumentDataByInstrument[instrumentId] =  pd.concat(frames, axis=1)
            self.__instrumentDataByInstrument[instrumentId].columns = columns
        # for feature in self.__features:
            # if self.__instrumentDataChunkByFeature[feature] is not None:
                # for instrumentId in self.__instrumentDataChunkByFeature[feature].columns:
                    # self.__instrumentDataByInstrument[instrumentId][feature] = self.__instrumentDataChunkByFeature[feature][instrumentId]

    def writeInstrumentData(self):
        for instrumentId in self.__instrumentIds:
            # tempFileName = getTemporaryFileName(instrumentId, featureKey, chunkNumber)
            fileName = self.getFilePath(instrumentId)
            if os.path.isfile(fileName):
                self.__instrumentDataByInstrument[instrumentId].to_csv(fileName, mode='a', header=False)
            else:
                self.__instrumentDataByInstrument[instrumentId].to_csv(fileName, mode='w')

    def readInstrumentData(self, useFile=True, chunkSize=None):
        if useFile:
            for instrumentId in self.__instrumentIds:
                fileName = self.getFilePath(instrumentId)
                if os.path.isfile(fileName):
                    self.__instrumentDataByInstrument[instrumentId] = InstrumentData(instrumentId, instrumentId,
                                                                                     fileName, chunkSize)
        else:
            for instrumentId in self.__instrumentIds:
                instrumentData = InstrumentData(instrumentId, instrumentId)
                instrumentData.setBookData(self.__instrumentDataByInstrument[instrumentId])
                self.__instrumentDataByInstrument[instrumentId] = instrumentData

    def getInstrumentDataByInstrument(self, instrumentId):
        return self.__instrumentDataByInstrument[instrumentId]

    def getInstrumentDataByFeature(self, featureKey):
        return self.__instrumentDataByFeature[featureKey]

    def cleanUp(self):
        for feature in self.__features:
            del self.__instrumentDataByFeature[feature], self.__instrumentDataGenerator[feature]
            del self.__instrumentDataChunkByFeature[feature]
        gc.collect()
