from backtester.dataSource.data_source import DataSource
from backtester.instrumentUpdates import *
import os
from datetime import datetime
from backtester.dataSource.data_source_utils import groupAndSortByTimeUpdates
import csv
from backtester.logger import *
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
import pandas as pd
import time


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class QuantQuestDataSource(DataSource):
    def __init__(self, cachedFolderName, dataSetId, instrumentIds):
        self.__cachedFolderName = cachedFolderName
        self.__dataSetId = dataSetId
        self.ensureDirectoryExists(cachedFolderName, dataSetId)
        self.ensureAllInstrumentsFile(dataSetId)
        if instrumentIds is not None and len(instrumentIds) > 0:
            self.__instrumentIds = instrumentIds
        else:
            self.__instrumentIds = self.getAllInstrumentIds()
        self.__bookDataByFeature = {}
        self.__groupedInstrumentUpdates = self.getGroupedInstrumentUpdates()
        self.__allTimes = None
        print ('Processing instruments before beginning backtesting. This could take some time...')
        self.processGroupedInstrumentUpdates()

    def ensureDirectoryExists(self, cachedFolderName, dataSetId):
        if not os.path.exists(cachedFolderName):
            os.mkdir(cachedFolderName, 0o755)
        if not os.path.exists(cachedFolderName + '/' + dataSetId):
            os.mkdir(cachedFolderName + '/' + dataSetId)

    def getFileName(self, instrumentId):
        return self.__cachedFolderName + self.__dataSetId + '/' + instrumentId + '.csv'

    def ensureAllInstrumentsFile(self, dataSetId):
        stockListFileName = self.__cachedFolderName + self.__dataSetId + '/' + 'stock_list.txt'
        if os.path.isfile(stockListFileName):
            return True
        url = 'https://raw.githubusercontent.com/Auquan/auquan-historical-data/master/qq2Data/%s/stock_list.txt' % (
            dataSetId)
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
        stockListFileName = self.__cachedFolderName + self.__dataSetId + '/' + 'stock_list.txt'
        if not os.path.isfile(stockListFileName):
            logError('Stock list file not present. Please try running again.')
            return []

        with open(stockListFileName) as f:
            content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]
        return content

    def downloadFile(self, dataSetId, instrumentId, downloadLocation):
        url = 'https://raw.githubusercontent.com/Auquan/auquan-historical-data/master/qq2Data/%s/%s.csv' % (
            dataSetId, instrumentId)
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

    def getInstrumentUpdateFromRow(self, instrumentId, row):
        bookData = row
        for key in bookData:
            if is_number(bookData[key]):
                bookData[key] = float(bookData[key])
        timeKey = ''
        timeOfUpdate = datetime.strptime(row[timeKey], '%Y-%m-%d %H:%M:%S')
        bookData.pop(timeKey, None)
        inst = StockInstrumentUpdate(stockInstrumentId=instrumentId,
                                     tradeSymbol=instrumentId,
                                     timeOfUpdate=timeOfUpdate,
                                     bookData=bookData)
        return inst

    def getGroupedInstrumentUpdates(self):
        allInstrumentUpdates = []
        for instrumentId in self.__instrumentIds:
            print('Processing data for stock: %s' % (instrumentId))
            fileName = self.getFileName(instrumentId)
            if not os.path.exists(self.__cachedFolderName):
                os.mkdir(self.cachedFolderName, 0o755)
            if not os.path.isfile(fileName):
                if not self.downloadFile(self.__dataSetId, instrumentId, fileName):
                    logError('Skipping %s:' % (instrumentId))
                    continue
            with open(self.getFileName(instrumentId)) as f:
                records = csv.DictReader(f)
                for row in records:
                    inst = self.getInstrumentUpdateFromRow(instrumentId, row)
                    allInstrumentUpdates.append(inst)

        groupedInstrumentUpdates = groupAndSortByTimeUpdates(allInstrumentUpdates)
        return groupedInstrumentUpdates

    def processGroupedInstrumentUpdates(self):
        timeUpdates = []
        for timeOfUpdate, instrumentUpdates in self.__groupedInstrumentUpdates:
            timeUpdates.append(timeOfUpdate)
        self.__allTimes = timeUpdates

        limits = [0.20, 0.40, 0.60, 0.80, 1.0]
        if (len(self.__instrumentIds) > 30):
            limits = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0]
        currentLimitIdx = 0
        idx = 0.0
        for timeOfUpdate, instrumentUpdates in self.__groupedInstrumentUpdates:
            idx = idx + 1.0
            if (idx / len(timeUpdates)) > limits[currentLimitIdx]:
                print ('%d%% done...' % (limits[currentLimitIdx] * 100))
                currentLimitIdx = currentLimitIdx + 1
            for instrumentUpdate in instrumentUpdates:
                bookData = instrumentUpdate.getBookData()
                for featureKey in bookData:
                    # TODO: Fix for python 3
                    if featureKey not in self.__bookDataByFeature:
                        self.__bookDataByFeature[featureKey] = pd.DataFrame(columns=self.__instrumentIds,
                                                                            index=timeUpdates)
                    self.__bookDataByFeature[featureKey].set_value(timeOfUpdate, instrumentUpdate.getInstrumentId(), bookData[featureKey])
        for featureKey in self.__bookDataByFeature:
            self.__bookDataByFeature[featureKey].fillna(method='pad', inplace=True)

    def emitInstrumentUpdates(self):
        for timeOfUpdate, instrumentUpdates in self.__groupedInstrumentUpdates:
            yield([timeOfUpdate, instrumentUpdates])

    def getInstrumentIds(self):
        return self.__instrumentIds

    def getBookDataByFeature(self):
        return self.__bookDataByFeature

    def getAllTimes(self):
        return self.__allTimes

    def getClosingTime(self):
        return self.__allTimes[-1]

    def getBookDataFeatures(self):
        return self.__bookDataByFeature.keys()
