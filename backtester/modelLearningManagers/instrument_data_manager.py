import os, gc
import pandas as pd
import numpy as np
import json
from dateutil import parser
from datetime import timedelta
from backtester.logger import *
from backtester.constants import FLOAT_FORMAT
from backtester.instrumentUpdates.instrument_data import InstrumentData

class InstrumentDataManager(object):
    '''
    '''
    def __init__(self, dataParser, features, instrumentIds, featureFolderName='features', lookbackSize=None):
        self.__cachedFolderName = dataParser._cachedFolderName
        self.__dataSetId = dataParser._dataSetId
        self.__timestamps = dataParser._allTimes
        self.__startDateStr = dataParser.getStartDate()
        self.__endDateStr = dataParser.getEndDate()
        self.__features = features
        self.__instrumentIds = instrumentIds
        self.__featureFolderName = featureFolderName
        self.__lookbackSize = None if (lookbackSize is None) or (lookbackSize == 0) else lookbackSize     # MaxPeriod -1
        self.__firstChunk = True
        self.__currentChunkNumber = -1
        self.__periodStartDateStr = None
        self.__periodEndDateStr = None
        self.__instrumentDataByFeature = {feature : None for feature in features}
        self.__instrumentLookbackDataByFeature = {feature : None for feature in features}
        self.__instrumentDataChunkByFeature = {feature : None for feature in features}
        self.__instrumentDataChunkCounter = {feature : None for feature in features}        # Useful for Proof of Concept
        self.__instrumentDataGenerator = {feature : None for feature in features}
        self.__instrumentDataByInstrument = {instrumentId : None for instrumentId in instrumentIds}
        # self.__instrumentDataByInstrument = {instrumentId : pd.DataFrame(columns=features) for instrumentId in instrumentIds}

        self.ensureDirectoryExists(self.__cachedFolderName, self.__dataSetId, featureFolderName)

    # returns simulator (generator) to simulate feature calculations in chunks
    # NOTE: This assumes all instruments have same set of timeStamps (index)
    def getSimulator(self, chunkSize):
        for feature in self.__features:
            self.__instrumentDataGenerator[feature] = self.getInstrumentDataGenerator(feature, chunkSize)
        return self.getInstrumentDataInChunks(pd.Series(self.__timestamps), chunkSize)

    # returns a chunk of all instruments data with feature as featureKey
    def getInstrumentDataChunkByFeature(self, featureKey):
        if self.__instrumentDataChunkByFeature[featureKey] is None:
            self.updateInstrumentDataChunk(featureKey)
        if self.__instrumentLookbackDataByFeature[featureKey] is None:
            return self.__instrumentDataChunkByFeature[featureKey]
        else:
            # OPTIMIZE: Concat it only once. Put it in updateInstrumentDataChunk
            return pd.concat([self.__instrumentLookbackDataByFeature[featureKey],
                              self.__instrumentDataChunkByFeature[featureKey]])

    # updates the instrumentBookDataChunk using its feature generator
    def updateInstrumentDataChunk(self, featureKey):
        if self.__instrumentDataGenerator[featureKey] is None:
            self.__instrumentDataChunkByFeature[featureKey] = None
            return
        try :
            chunkNumber, self.__instrumentDataChunkByFeature[featureKey] = next(self.__instrumentDataGenerator[featureKey])
            self.__instrumentDataChunkCounter[featureKey] = chunkNumber
            self.setPeriodDates(featureKey, chunkNumber)
        except StopIteration:
            print("Data Integrity is broken! Check instrument data chunk counter")
            self.__instrumentDataChunkByFeature[featureKey] = None

    # set period start and end dates which is used for fingerprinting
    def setPeriodDates(self, featureKey, chunkNumber):
        if self.__lookbackSize is not None:
            if self.__periodStartDateStr is None:
                # NOTE: Hardcoded date format string
                try:
                    # Take twice of maxPeriod from the top of chunk
                    self.__periodStartDateStr = self.__instrumentDataChunkByFeature[featureKey].index[2*self.__lookbackSize].date().strftime('%Y/%m/%d')
                except IndexError:
                    # Take last timestamp
                    self.__periodStartDateStr = self.__instrumentDataChunkByFeature[featureKey].index[-1].date().strftime('%Y/%m/%d')
            if self.__currentChunkNumber != chunkNumber:
                self.__currentChunkNumber = chunkNumber
                try:
                    # Take the maxPeriod from the bottom of chunk
                    self.__periodEndDateStr = self.__instrumentDataChunkByFeature[featureKey].index[-self.__lookbackSize].date().strftime('%Y/%m/%d')
                except IndexError:
                    # Take first timestamp
                    self.__periodEndDateStr = self.__instrumentDataChunkByFeature[featureKey].index[0].date().strftime('%Y/%m/%d')

    # adds last lookbackSize rows from instrument data chunk to instrument lookbackData
    def updateInstrumentLookbackData(self, featureKey):
        if (self.__instrumentDataChunkByFeature[featureKey] is not None) and (self.__lookbackSize is not None):
            self.__instrumentLookbackDataByFeature[featureKey] = self.__instrumentDataChunkByFeature[featureKey][-self.__lookbackSize:]

    # dumps the chunks of all instrument data and releases the memory
    def dumpInstrumentDataChunk(self):
        for featureKey in self.__features:
            self.updateInstrumentLookbackData(featureKey)
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
        if self.__lookbackSize is not None:
            chunkSize = chunkSize if chunkSize is None else (chunkSize - self.__lookbackSize)
        if chunkSize is None:
            yield (0, instrumentData)
        else:
            if chunkSize <= 0:
                logError("[InstrumentDataManager] chunkSize must be a positive integer and greater than lookbackSize")
                raise ValueError
            if instrumentData is None:
                logError("[InstrumentDataManager] instrument data is not available")
                raise ValueError
            groups = np.arange(len(instrumentData)) // chunkSize
            # OPTIMIZE: check if groupby returns copy or view
            for chunkNumber, instrumentDataChunk in instrumentData.groupby(groups):
                yield (chunkNumber, instrumentDataChunk)

    def addFeatureValueChunkForAllInstruments(self, featureKey, data):
        if (self.__instrumentLookbackDataByFeature[featureKey] is None) or (self.__lookbackSize is None) or (data is None):
            self.__instrumentDataChunkByFeature[featureKey] = data
        else:
            chunkSize = len(data) - self.__lookbackSize
            self.__instrumentDataChunkByFeature[featureKey] = data[-chunkSize:]

    def transformInstrumentData(self):
        for instrumentId in self.__instrumentIds:
            frames = []
            columns = []
            for feature in self.__features:
                if self.__instrumentDataChunkByFeature[feature] is not None:
                    frames.append(self.__instrumentDataChunkByFeature[feature][instrumentId])
                    columns.append(feature)
            if len(frames) == 0:
                self.__instrumentDataByInstrument[instrumentId] = None
            else:
                self.__instrumentDataByInstrument[instrumentId] = pd.concat(frames, axis=1)
                self.__instrumentDataByInstrument[instrumentId].columns = columns
        # for feature in self.__features:
            # if self.__instrumentDataChunkByFeature[feature] is not None:
                # for instrumentId in self.__instrumentDataChunkByFeature[feature].columns:
                    # self.__instrumentDataByInstrument[instrumentId][feature] = self.__instrumentDataChunkByFeature[feature][instrumentId]

    def writeInstrumentData(self, prepend=None):
        for instrumentId in self.__instrumentIds:
            if self.__instrumentDataByInstrument[instrumentId] is None:
                continue
            fileName = self.getFilePath(instrumentId)
            if prepend is True:     # prepend into the existing file
                self.prependInstrumentData(instrumentId, fileName, self.__instrumentDataByInstrument[instrumentId])
            elif prepend is False:  # append into the existing file
                self.appendInstrumentData(instrumentId, fileName, self.__instrumentDataByInstrument[instrumentId])
            elif os.path.isfile(fileName) and (not self.__firstChunk):  # append into the new file
                self.__instrumentDataByInstrument[instrumentId].to_csv(fileName, mode='a', header=False, float_format=FLOAT_FORMAT)
            else:                   # write into the new file
                self.__instrumentDataByInstrument[instrumentId].to_csv(fileName, mode='w', float_format=FLOAT_FORMAT)
        self.__firstChunk = False

    def appendInstrumentData(self, instrumentId, fileName, data):
        existingColumns = pd.read_csv(fileName, index_col=0, nrows=1).columns.tolist()
        if self.__lookbackSize is None:
            data.reindex(columns=existingColumns).to_csv(fileName, mode='a', header=False, float_format=FLOAT_FORMAT)
        else:
            data.iloc[self.__lookbackSize:].reindex(columns=existingColumns).to_csv(fileName, mode='a', header=False, float_format=FLOAT_FORMAT)

    def prependInstrumentData(self, instrumentId, fileName, data):
        name, ext = os.path.splitext(fileName)
        tempFileName =  name + '.temp'
        if self.__firstChunk:
            data.to_csv(tempFileName, mode='w', float_format=FLOAT_FORMAT)
        else:
            data.to_csv(tempFileName, mode='a', header=False, float_format=FLOAT_FORMAT)

    def appendExistingInstrumentData(self, chunkSize=None):
        NextOfEndDateStr = (parser.parse(self.__endDateStr) + timedelta(days=1)).strftime('%Y%m%d')
        newColumns = None
        for instrumentId in self.__instrumentIds:
            fileName = self.getFilePath(instrumentId)
            name, ext = os.path.splitext(fileName)
            tempFileName =  name + '.temp'
            # NOTE: Assuming all instruments have same column set
            if newColumns is None:
                newColumns = pd.read_csv(fileName, index_col=0, nrows=1).columns.tolist()
            existingData = InstrumentData(instrumentId, instrumentId, fileName, chunkSize)
            for i, chunk in existingData.getBookDataChunk():
                chunk[NextOfEndDateStr:].reindex(columns=newColumns).to_csv(tempFileName, mode='a', header=False, float_format=FLOAT_FORMAT)
            os.remove(fileName)
            os.rename(tempFileName, fileName)

    def readInstrumentData(self, instrumentId, useFile=True, chunkSize=None, usecols=None):
        if useFile:
            fileName = self.getFilePath(instrumentId)
            if os.path.isfile(fileName):
                self.__instrumentDataByInstrument[instrumentId] = InstrumentData(instrumentId, instrumentId,
                                                                                 fileName, chunkSize, usecols)
        else:
            instrumentData = InstrumentData(instrumentId, instrumentId)
            instrumentData.setBookData(self.__instrumentDataByInstrument[instrumentId])
            self.__instrumentDataByInstrument[instrumentId] = instrumentData

    def checkDataIntegrity(self, chunkNumber):
        missingFeatures = []
        for featureKey in self.__instrumentDataChunkCounter:
            if (self.__instrumentDataChunkCounter[featureKey] is not None) and (self.__instrumentDataChunkCounter[featureKey] != chunkNumber):
                missingFeatures.append(featureKey)
        if len(missingFeatures) == 0:
            return True
        for missingFeature in missingFeatures:
            logWarn("\"%s\" feature's total chunks (%d) didn't match with total number of global chunks (%d)" %
                    (missingFeature, self.__instrumentDataChunkCounter[missingFeature], chunkNumber))
        return False

    def saveInstrumentDataFingerprint(self, fileName, update=False, prepend=None):
        fileName = self.getFilePath(fileName, ext='.json')
        if update:
            self.updateInstrumentDataFingerprint(fileName, prepend)
            return
        fingerprint = {}
        fingerprint['stocks'] = self.__instrumentIds
        fingerprint['features'] = self.__features
        fingerprint['startDate'] = self.__startDateStr
        fingerprint['endDate'] = self.__endDateStr
        fingerprint['lookbackSize'] = self.__lookbackSize
        fingerprint['periodStartDate'] = self.__periodStartDateStr
        fingerprint['periodEndDate'] = self.__periodEndDateStr
        fingerprint['dataSize'] = len(self.__timestamps)
        with open(fileName, 'w') as fp:
            json.dump(fingerprint, fp, indent=4)

    def updateInstrumentDataFingerprint(self, fileName, prepend):
        with open(fileName, 'r') as fp:
            fingerprint = json.load(fp)
        fingerprint['stocks'] = list(set(fingerprint['stocks']).union(self.__instrumentIds))
        startDate = parser.parse(self.__startDateStr)
        endDate = parser.parse(self.__endDateStr)
        periodStartDate = parser.parse(self.__periodStartDateStr)
        periodEndDate = parser.parse(self.__periodEndDateStr)
        existingStartDate = parser.parse(fingerprint['startDate'])
        existingEndDate = parser.parse(fingerprint['endDate'])
        existingPeriodStartDate = parser.parse(fingerprint['periodStartDate'])
        existingPeriodEndDate = parser.parse(fingerprint['periodEndDate'])
        fingerprint['startDate'] = self.__startDateStr if startDate < existingStartDate else fingerprint['startDate']
        fingerprint['endDate'] = self.__endDateStr if endDate > existingEndDate else fingerprint['endDate']
        fingerprint['periodStartDate'] = self.__periodStartDateStr if periodStartDate < existingPeriodStartDate else fingerprint['periodStartDate']
        fingerprint['periodEndDate'] = self.__periodEndDateStr if periodEndDate > existingPeriodEndDate else fingerprint['periodEndDate']
        fingerprint['features'] = self.__features
        if startDate != existingStartDate or endDate != existingEndDate or prepend is not None:
            if prepend is True:
                fingerprint['dataSize'] += len(self.__timestamps) if self.__lookbackSize is None else (len(self.__timestamps) - 2*self.__lookbackSize - 1)
            else:
                fingerprint['dataSize'] += len(self.__timestamps) if self.__lookbackSize is None else (len(self.__timestamps) - self.__lookbackSize)
        with open(fileName, 'w') as fp:
            json.dump(fingerprint, fp, indent=4)

    def addFeatureValueForAllInstruments(self, featureKey, data):
        self.__instrumentDataByFeature[featureKey] = data

    def addAllFeaturesForInstrument(self, instrumentId, data):
        self.__instrumentDataByInstrument[instrumentId] = data

    def getInstrumentDataByInstrument(self, instrumentId, useFile, chunkSize):
        if self.__instrumentDataByInstrument[instrumentId] is None:
            self.readInstrumentData(instrumentId, useFile, chunkSize)
        return self.__instrumentDataByInstrument[instrumentId]

    def getInstrumentDataByFeature(self, featureKey):
        return self.__instrumentDataByFeature[featureKey]

    def getFilePath(self, fileName, newDir='', ext='.csv'):
        return os.path.join(self.__cachedFolderName, self.__dataSetId, self.__featureFolderName, newDir, os.path.splitext(fileName)[0] + ext)

    def getTemporaryFileName(self, fname, *fnames):
        tempFileName = str(fname)
        for name in fnames:
            tempFileName = tempFileName + "_" + str(name)
        return tempFileName

    def ensureDirectoryExists(self, cachedFolderName, *folderNames):
        if not os.path.exists(cachedFolderName):
            os.mkdir(cachedFolderName, 0o755)
        folderPath = cachedFolderName
        for folderName in folderNames:
            folderPath = os.path.join(folderPath, folderName)
            if not os.path.exists(folderPath):
                os.mkdir(folderPath)

    def cleanup(self, delInstrumentData=False):
        for feature in self.__features:
            del self.__instrumentDataByFeature[feature]
            del self.__instrumentDataGenerator[feature]
            del self.__instrumentDataChunkByFeature[feature]
        if delInstrumentData:
            for instrumentId in self.__instrumentIds:
                del self.__instrumentDataByInstrument[instrumentId]
                self.__instrumentDataByInstrument[instrumentId] = None
        gc.collect()
