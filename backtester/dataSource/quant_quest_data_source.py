from backtester.dataSource.data_source import DataSource
from backtester.instrumentUpdates import *
import os
from datetime import datetime
from backtester.dataSource.data_source_utils import groupAndSortByTimeUpdates
import csv
from backtester.logger import *


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
        if instrumentIds is not None and len(instrumentIds) > 0:
            self.__instrumentIds = instrumentIds
        else:
            self.__instrumentIds = self.getAllInstrumentIds()
        self.__groupedInstrumentUpdates = self.getGroupedInstrumentUpdates()

    def getFileName(self, instrumentId):
        return self.__cachedFolderName + self.__dataSetId + '/' + instrumentId + '.csv'

    def getAllInstrumentIds(self):
        stockListFileName = self.__cachedFolderName + self.__dataSetId + '/' + 'stock_list.txt'
        if not os.path.isfile(stockListFileName):
            logError('Stock list file not present. Please download the data first.')
            return []

        with open(stockListFileName) as f:
            content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]
        return content

    def downloadFile(dataSetId):
        return None

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
            logInfo('Processing data for stock: %s' % (instrumentId))
            fileName = self.getFileName(instrumentId)
            if not os.path.exists(self.__cachedFolderName):
                os.mkdir(self.cachedFolderName, 0755)
            if not os.path.isfile(fileName):
                logError('Data missing for stock: %s, at path: %s' % (instrumentId, fileName))
                continue
            with open(self.getFileName(instrumentId)) as f:
                records = csv.DictReader(f)
                for row in records:
                    inst = self.getInstrumentUpdateFromRow(instrumentId, row)
                    allInstrumentUpdates.append(inst)

        groupedInstrumentUpdates = groupAndSortByTimeUpdates(allInstrumentUpdates)
        return groupedInstrumentUpdates

    def emitInstrumentUpdates(self):
        for timeOfUpdate, instrumentUpdates in self.__groupedInstrumentUpdates:
            yield([timeOfUpdate, instrumentUpdates])
