import os
import pandas as pd
from backtester.logger import *

class InstrumentDataManager(object):
    '''
    '''
    def __init__(self, dataParser, features, instrumentIds, featureFolderName='features', numChunks=1):
        self.__cachedFolderName = dataParser._cachedFolderName
        self.__dataSetId = dataParser._dataSetId
        self.__instrumentIds = instrumentIds
        self.__featureFolderName = featureFolderName
        self.__numChunks = numChunks
        self.__instrumentDataByFeature = {feature : None for feature in features}
        self.__instrumentDataSize = None    # NOTE: This requires to have same timestamps in all instruments

    def getFilePath(self, fileName, newDir=''):
        return os.path.join(self.__cachedFolderName, self.__dataSetId, self.__featureFolderName, newDir, fileName + '.csv')

    def getTemporaryFileName(self, fname, *fnames):
        tempFileName = str(fname)
        for name in fnames:
            tempFileName = tempFileName + "_" + str(name)
        return tempFileName

    def getFeatureGenerator(self, featureKey, chunkSize):
        return self.getBookDataInChunks(featureKey, chunkSize)

    # returns a chunk from already completely loaded book data features
    def getBookDataInChunks(self, featureKey, chunkSize):
        if chunkSize <=0 :
            logError("chunkSize must be a positive integer")
        for chunkNumber, bookDataFeatureChunk in self.__instrumentDataByFeature[featureKey].groupby(np.arange(self.__instrumentDataSize) // chunkSize):
            yield (chunkNumber, bookDataFeatureChunk)

    def addBookDataFeatureValueForAllInstruments(self, featureKey, data):
        self.__instrumentDataByFeature[featureKey] = data
        if self.__instrumentDataSize is None:
            self.__instrumentDataSize = len(data)

    def addFeatureValueForAllInstruments(self, featureKey, data, chunkNumber, save=False):
        self.__instrumentDataByFeature[featureKey] = data
        if save:
            self.writeInstrumentData(chunkNumber)

    def writeInstrumentData(self, featureKey, chunkNumber):
        for instrumentId in self.__instrumentDataByFeature[featureKey].columns:
            tempFileName = getTemporaryFileName(instrumentId, featureKey, chunkNumber)
            # fileName = getFilePath(instrumentId, newDir=featureKey)
            if os.path.isfile(fileName):
                self.__instrumentDataByFeature[featureKey][instrumentId].to_csv(fileName, mode='a')
            else:
                self.__instrumentDataByFeature[featureKey][instrumentId].to_csv(fileName, mode='w')

    def dumpInstrumentData(self, featureKey):
        del self.__instrumentDataByFeature[featureKey]
        self.__instrumentDataByFeature[featureKey] = None
        # TODO: Use gc to free memory

    def getInstrumentData(self, instrumentId):
        pass

    def getBookDataFeatures(self):
        return list(self.__bookData.columns)
