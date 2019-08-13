from backtester.dataSource.data_source import DataSource
from backtester.instrumentUpdates import *
import os
from datetime import datetime
import csv
from backtester.logger import *
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


class CsvDataSource(DataSource):
    def __init__(self, cachedFolderName, dataSetId, instrumentIds, downloadUrl = None, timeKey = None, timeStringFormat = None, startDateStr=None, endDateStr=None, liveUpdates=True, pad=True):
        self._cachedFolderName = cachedFolderName
        self._dataSetId = dataSetId
        self._downloadUrl = downloadUrl
        self._timeKey = timeKey
        self._timeStringFormat = timeStringFormat
        self.ensureDirectoryExists(self._cachedFolderName, self._dataSetId)
        self.ensureAllInstrumentsFile(dataSetId)
        super(CsvDataSource, self).__init__(cachedFolderName, dataSetId, instrumentIds, startDateStr, endDateStr)
        if liveUpdates:
            self._allTimes, self._groupedInstrumentUpdates = self.getGroupedInstrumentUpdates()
        else:
            self._allTimes, self._bookDataByInstrument = self.getAllInstrumentUpdates()
            if pad:
                self.padInstrumentUpdates()
            if (startDateStr is not None) and (endDateStr is not None):
                self.filterUpdatesByDates([(startDateStr, endDateStr)])

    def getFileName(self, instrumentId):
        return self._cachedFolderName + self._dataSetId + '/' + instrumentId + '.csv'

    def ensureAllInstrumentsFile(self, dataSetId):
        stockListFileName = self._cachedFolderName + self._dataSetId + '/' + 'stock_list.txt'
        if os.path.isfile(stockListFileName):
            return True
        url = ''
        if self._dataSetId != '':
            url = '%s/%s/stock_list.txt' % (self._downloadUrl, self._dataSetId)
        else:
            url = '%s/stock_list.txt' % (self._downloadUrl)
        print(url)
        response = urlopen(url)
        status = response.getcode()
        if status == 200:
            print('Downloading list of stocks to file: %s' % (stockListFileName))
            with open(stockListFileName, 'w') as f:
                f.write(response.read().decode('utf8'))
            return True
        else:
            logError('File not found. Please check internet')
            return False

    def getAllInstrumentIds(self):
        stockListFileName = self._cachedFolderName + self._dataSetId + '/' + 'stock_list.txt'
        if not os.path.isfile(stockListFileName):
            logError('Stock list file not present. Please try running again.')
            return []

        with open(stockListFileName) as f:
            content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]
        return content

    def downloadFile(self, instrumentId, downloadLocation):
        url = ''
        if self._dataSetId != '':
            url = '%s/%s/%s.csv' % (self._downloadUrl, self._dataSetId, instrumentId)
        else:
            url = '%s/%s.csv' % (self._downloadUrl, instrumentId)

        response = urlopen(url)
        status = response.getcode()
        if status == 200:
            print('Downloading %s data to file: %s' % (instrumentId, downloadLocation))
            with open(downloadLocation, 'w') as f:
                f.write(response.read().decode('utf8'))
            return True
        else:
            logError('File not found. Please check settings!')
            return False

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
