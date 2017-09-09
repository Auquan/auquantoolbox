from backtester.dataSource.data_source import DataSource
from backtester.instrumentUpdates import *
import os
from datetime import datetime
from backtester.dataSource.data_source_utils import groupAndSortByTimeUpdates
import copy
import csv


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class QuantQuestDataSource(DataSource):
    def __init__(self, cachedFolderName, dataSetId, instrumentIds):
        self.__instrumentIds = instrumentIds
        self.__cachedFolderName = cachedFolderName
        self.__dataSetId = dataSetId

    def getFileName(self, instrumentId):
        return self.__cachedFolderName + '/' + self.__dataSetId + '/' + instrumentId + '.csv'

    def downloadFile(dataSetId):
        return ''

    def getInstrumentUpdateFromRow(self, instrumentId, row):
        bookData = copy.deepcopy(row)
        for key in bookData:
            if is_number(bookData[key]):
                bookData[key] = float(bookData[key])
        timeKey = ''
        bookData.pop(timeKey, None)
        timeOfUpdate = datetime.strptime(row[timeKey], '%Y-%m-%d %H:%M:%S')
        inst = StockInstrumentUpdate(stockInstrumentId=instrumentId,
                                     tradeSymbol=instrumentId,
                                     timeOfUpdate=timeOfUpdate,
                                     bookData=bookData)
        return inst

    def emitInstrumentUpdates(self):
        allInstrumentUpdates = []
        for instrumentId in self.__instrumentIds:
            fileName = self.getFileName(instrumentId)
            if not os.path.exists(self.__cachedFolderName):
                os.mkdir(self.cachedFolderName, 0755)
            if not os.path.isfile(fileName):
                self.downloadFile(self.__dataSetId)
            with open(self.getFileName(instrumentId)) as f:
                records = csv.DictReader(f)
                for row in records:
                    inst = self.getInstrumentUpdateFromRow(instrumentId, row)
                    allInstrumentUpdates.append(inst)

        groupedInstrumentUpdates = groupAndSortByTimeUpdates(allInstrumentUpdates)
        for timeOfUpdate, instrumentUpdates in groupedInstrumentUpdates:
            yield([timeOfUpdate, instrumentUpdates])