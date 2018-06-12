from backtester.dataSource.data_source import DataSource
from backtester.instrumentUpdates import *
import os
from datetime import datetime
import csv
from backtester.logger import *
from backtester.instrumentUpdates.instrument_data import InstrumentData
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class FeaturesDataSource(DataSource):
    def __init__(self, cachedFolderName, dataSetId, instrumentIds, features, startDateStr=None, endDateStr=None, featureFolderName='features', downloadUrl=None, timeKey=None, timeStringFormat=None, liveUpdates=True, pad=True):
        super(FeaturesDataSource, self).__init__(cachedFolderName, dataSetId, instrumentIds, startDateStr, endDateStr)
        self._usecols = features
        self._featureFolderName = featureFolderName
        self._downloadUrl = downloadUrl
        self._timeKey = timeKey
        self._timeStringFormat = timeStringFormat
        self._liveUpdates = liveUpdates
        self._pad = pad
        self._startDateStr = startDateStr
        self._endDateStr = endDateStr
        self.ensureAllInstrumentsFile()

    def loadAllInstrumentUpdates(self):
        if self._liveUpdates:
            self._allTimes, self._groupedInstrumentUpdates = self.getGroupedInstrumentUpdates()
        else:
            self._allTimes, self._bookDataByInstrument = self.getAllInstrumentUpdates()
            if self._pad:
                self.padInstrumentUpdates()
            if (self._startDateStr is not None) and (self._endDateStr is not None):
                self.filterUpdatesByDates([(self._startDateStr, self._endDateStr)])

    def getInstrumentUpdates(self, instrumentId, chunkSize=None):
        fileName = self.getFileName(instrumentId)
        if not self.downloadAndAdjustData(instrumentId, fileName):
            return None
        return InstrumentData(instrumentId, instrumentId, fileName, chunkSize=chunkSize, usecols=self._usecols)

    def getFileName(self, instrumentId):
        return os.path.join(self._cachedFolderName, self._dataSetId, self._featureFolderName, instrumentId + '.csv')

    def ensureAllInstrumentsFile(self):
        stockDataFileName = os.path.join(self._cachedFolderName, self._dataSetId, self._featureFolderName, 'stock_data.json')
        if os.path.isfile(stockListFileName):
            return True
        # TODO: Download from server
        raise NotImplementedError

    def downloadFile(self, instrumentId, downloadLocation):
        raise NotImplementedError

    def downloadAndAdjustData(self, instrumentId, fileName):
        if not os.path.isfile(fileName):
            if not self.downloadFile(instrumentId, fileName):
                logError('Skipping %s:' % (instrumentId))
                return False
        return True

    def getInstrumentUpdateFromRow(self, instrumentId, row):
        bookData = row
        for key in bookData:
            if is_number(bookData[key]):
                bookData[key] = float(bookData[key])
        timeKey = self._timeKey
        timeOfUpdate = datetime.strptime(row[timeKey], self._timeStringFormat)
        bookData.pop(timeKey, None)
        inst = StockInstrumentUpdate(stockInstrumentId=instrumentId,
                                     tradeSymbol=instrumentId,
                                     timeOfUpdate=timeOfUpdate,
                                     bookData=bookData)
        if self._bookDataFeatureKeys is None:
            self._bookDataFeatureKeys = bookData.keys()  # just setting to the first one we encounter
        return inst
