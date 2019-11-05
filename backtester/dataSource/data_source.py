import pandas as pd
import os, csv
from datetime import datetime
from backtester.dataSource.data_source_utils import groupAndSortByTimeUpdates
from backtester.instrumentUpdates.instrument_data import InstrumentData
from backtester.logger import *

class DataSource(object):
    def __init__(self, cachedFolderName, dataSetId, instrumentIds, startDateStr, endDateStr):
        self._cachedFolderName = cachedFolderName
        self._dataSetId = dataSetId
        self.ensureDirectoryExists(self._cachedFolderName, self._dataSetId)
        if instrumentIds is not None and len(instrumentIds) > 0:
            self._instrumentIds = instrumentIds
        else:
            self._instrumentIds = self.getAllInstrumentIds()

        if startDateStr and endDateStr:
            # # TODO: write method to also parse date string in different formats
            self._startDate = datetime.strptime(startDateStr, "%Y/%m/%d")
            self._endDate = datetime.strptime(endDateStr, "%Y/%m/%d")

        # Class variables: To be set by child class
        self._allTimes = None
        self._groupedInstrumentUpdates = None
        self._bookDataByInstrument = None
        self._bookDataFeatureKeys = None

    def getInstrumentUpdateFromRow(self, instrumentId, row):
        raise NotImplementedError

    def downloadAndAdjustData(self, instrumentId, fileName):
        raise NotImplementedError

    # returns a list of all instrument identifiers
    def getAllInstrumentIds(self):
        logError("No instrument provided")
        raise NotImplementedError

    # returns a list of instrument identifiers
    def getInstrumentIds(self):
        return self._instrumentIds

    # returns a list of feature keys which are already present in the data.
    def getBookDataFeatures(self):
        return self._bookDataFeatureKeys

    # emits list of instrument updates at the same time.
    # The caller needs to ensure all these updates are happening at the same time
    # emits [t1, [i1, i2, i3]], where i1, i2, i3 are updates happening at time t1
    def emitInstrumentUpdates(self):
        if self._groupedInstrumentUpdates is None:
            logError("groupedInstrumentUpdates has not been computed")
        for timeOfUpdate, instrumentUpdates in self._groupedInstrumentUpdates:
            yield([timeOfUpdate, instrumentUpdates])

    # emits the dict of all instrument updates where
    # keys are instrumentId and values are pandas dataframe
    def emitAllInstrumentUpdates(self):
        return self._bookDataByInstrument

    def getGroupedInstrumentUpdates(self):
        allInstrumentUpdates = []
        for instrumentId in self._instrumentIds:
            print('Processing data for stock: %s' % (instrumentId))
            fileName = self.getFileName(instrumentId)
            if not self.downloadAndAdjustData(instrumentId, fileName):
                continue
            with open(fileName) as f:
                records = csv.DictReader(f)
                for row in records:
                    try:
                        inst = self.getInstrumentUpdateFromRow(instrumentId, row)
                        allInstrumentUpdates.append(inst)
                    except:
                        continue
        timeUpdates, groupedInstrumentUpdates = groupAndSortByTimeUpdates(allInstrumentUpdates)
        return timeUpdates, groupedInstrumentUpdates

    def getAllInstrumentUpdates(self, chunks=None):
        allInstrumentUpdates = {instrumentId : None for instrumentId in self._instrumentIds}
        timeUpdates = []
        for instrumentId in self._instrumentIds:
            print('Processing data for stock: %s' % (instrumentId))
            fileName = self.getFileName(instrumentId)
            if not self.downloadAndAdjustData(instrumentId, fileName):
                continue
            ### TODO: Assumes file is a csv, this is should not be in base class but ds type specific
            allInstrumentUpdates[instrumentId] = InstrumentData(instrumentId, instrumentId, fileName, chunkSize=None)
            timeUpdates = allInstrumentUpdates[instrumentId].getAllTimestamps().union(timeUpdates)
            # NOTE: Assuming data is sorted by timeUpdates and all instruments have same columns
            if self._bookDataFeatureKeys is None:
                self._bookDataFeatureKeys = allInstrumentUpdates[instrumentId].getBookDataFeatures()
        timeUpdates = list(timeUpdates)
        return timeUpdates, allInstrumentUpdates

    # set same timestamps in all instrument data and then pad
    ## TODO: Change thisto supply a df
    def padInstrumentUpdates(self):
        for instrumentId in self._instrumentIds:
            self._bookDataByInstrument[instrumentId].padInstrumentData(self._allTimes)

    # selects only those instrument updates which lie within dateRange
    def filterUpdatesByDates(self, dateRange=None):
        dateRange = dateRange if dateRange else (self._startDate.strftime("%Y%m%d"), self._endDateStr.strftime("%Y%m%d"))
        for instrumentId in self._instrumentIds:
            self._bookDataByInstrument[instrumentId].filterDataByDates(dateRange)

    # accretes all instrument updates using emitInstrumentUpdates method
    def processAllInstrumentUpdates(self, pad=True):
        self._bookDataByInstrument = {instrumentId : pd.DataFrame(index=self._allTimes) for instrumentId in self._instrumentIds}
        for timeOfUpdate, instrumentUpdates in self.emitInstrumentUpdates():
            for instrumentUpdate in instrumentUpdates:
                instrumentId = instrumentUpdate.getInstrumentId()
                for col in instrumentUpdate.getBookData():
                    self._bookDataByInstrument[instrumentId].at[timeOfUpdate, col] = instrumentUpdate.getBookData()[col]
        for instrumentId in self._bookDataByInstrument:
            if pad:
                self._bookDataByInstrument[instrumentId].fillna(method='ffill', inplace=True)
                self._bookDataByInstrument[instrumentId].fillna(0.0, inplace=True)
            else:
                self._bookDataByInstrument[instrumentId].dropna(inplace=True)
            instrumentData = InstrumentData(instrumentId, instrumentId)
            instrumentData.setBookData(self._bookDataByInstrument[instrumentId])
            self._bookDataByInstrument[instrumentId] = instrumentData

    def setStartDate(self, startDateStr):
        self._startDate = datetime.strptime(startDateStr, "%Y/%m/%d")

    def setEndDate(self, endDateStr):
        self._endDate = datetime.strptime(endDateStr, "%Y/%m/%d")

    def setDateRange(self, dateRange):
        self._dateRange = dateRange

    '''
    Helper Functions
    '''

    def ensureDirectoryExists(self, cachedFolderName, dataSetId):
        if not os.path.exists(cachedFolderName):
            os.mkdir(cachedFolderName, 0o755)
        if not os.path.exists(cachedFolderName + '/' + dataSetId):
            os.mkdir(cachedFolderName + '/' + dataSetId)

    '''
    Called at end of trading to cleanup stuff
    '''
    def cleanup(self):
        return
