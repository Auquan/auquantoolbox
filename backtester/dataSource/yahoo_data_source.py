from datetime import datetime
from backtester.instrumentUpdates import *
from backtester.constants import *
from backtester.logger import *
from backtester.dataSource.data_source import DataSource
import csv
import pandas as pd
import os
import os.path
from backtester.dataSource.data_source_utils import downloadFileFromYahoo, groupAndSortByTimeUpdates
import backtester.dataSource.data_source_utils as data_source_utils

TYPE_LINE_UNDEFINED = 0
TYPE_LINE_HEADER = 1
TYPE_LINE_DATA = 2


def checkDate(lineItem):
    try:
        datetime.strptime(lineItem, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def checkTimestamp(lineItem):
    return True


def isFloat(string):
    try:
        return float(string) or float(string) == 0.0
    except ValueError:  # if string is not a number
        return False

# Returns the type of lineItems


def validateLineItem(lineItems):
    if len(lineItems) == 7:
        if lineItems[0] == "Date":
            return TYPE_LINE_HEADER
        elif checkDate(lineItems[0]) and isFloat(lineItems[1]) and isFloat(lineItems[2]) and isFloat(lineItems[3]) and isFloat(lineItems[4]) and isFloat(lineItems[5]):
            return TYPE_LINE_DATA
    return TYPE_LINE_UNDEFINED


def parseDataLine(lineItems):
    if (len(lineItems) != 7):
        return None
    openPrice = float(lineItems[1])
    high = float(lineItems[2])
    low = float(lineItems[3])
    closePrice = float(lineItems[4])
    adjustedClose = float(lineItems[5])
    volume = float(lineItems[6])
    return {'open': openPrice,
            'high': high,
            'low': low,
            'close': closePrice,
            'adjClose' : adjustedClose,
            'volume': volume}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class InstrumentsFromFile():
    def __init__(self, fileName, instrumentId):
        self.fileName = fileName
        self.instrumentId = instrumentId
        self.currentInstrumentSymbol = instrumentId
        self.currentTimeOfUpdate = None
        self.currentBookData = None

    def processLine(self, line):
        lineItems = line.split(',')
        lineItemType = validateLineItem(lineItems)
        if (lineItemType == TYPE_LINE_DATA):
            inst = None
            if self.currentInstrumentSymbol is not None:
                self.currentTimeOfUpdate = datetime.strptime(lineItems[0], "%Y-%m-%d")
                self.currentInstrumentSymbol = self.instrumentId
                self.currentBookData = parseDataLine(lineItems)
                if self.currentBookData is None:
                    return None
                # right now only works for stocks
                inst = StockInstrumentUpdate(stockInstrumentId=self.instrumentId,
                                             tradeSymbol=self.currentInstrumentSymbol,
                                             timeOfUpdate=self.currentTimeOfUpdate,
                                             bookData=self.currentBookData)
                return inst
        return None

    def processLinesIntoInstruments(self):
        with open(self.fileName, "r") as ins:
            instruments = []
            for line in ins:
                inst = self.processLine(line)
                if inst is not None:
                    instruments.append(inst)
            return instruments


class YahooStockDataSource(DataSource):
    def __init__(self, cachedFolderName, dataSetId, instrumentIds, startDateStr, endDateStr,event='history',adjustPrice=False,downloadId=".NS"):
        self.startDate = datetime.strptime(startDateStr, "%Y/%m/%d")
        self.endDate = datetime.strptime(endDateStr, "%Y/%m/%d")
        self.dateAppend = "_%sto%s"%(datetime.strptime(startDateStr, '%Y/%m/%d').strftime('%Y-%m-%d'),datetime.strptime(startDateStr, '%Y/%m/%d').strftime('%Y-%m-%d'))
        self.__cachedFolderName = cachedFolderName
        self.__dataSetId = dataSetId
        self.ensureDirectoryExists(self.__dataSetId)
        self.__downloadId = downloadId
        if instrumentIds is not None and len(instrumentIds) > 0:
            self.__instrumentIds = instrumentIds
        else:
            self.__instrumentIds = self.getAllInstrumentIds()
        self.__bookDataByFeature = {}
        self.currentDate = self.startDate
        self.event = event
        self.adjustPrice = adjustPrice
        self.__groupedInstrumentUpdates = self.getGroupedInstrumentUpdates()
        self.processGroupedInstrumentUpdates()

    def getFileName(self, dataSetId, instrumentId):
        return self.__cachedFolderName + dataSetId + '/' + instrumentId + '%s.csv'%self.dateAppend

    def ensureDirectoryExists(self, dataSetId):
        if not os.path.exists(self.__cachedFolderName):
            os.mkdir(self.__cachedFolderName, 0o755)
        if not os.path.exists(self.__cachedFolderName + '/' + dataSetId):
            os.mkdir(self.__cachedFolderName + '/' + dataSetId)

    def getGroupedInstrumentUpdates(self):
        allInstrumentUpdates = []
        for instrumentId in self.__instrumentIds:
            print('Processing data for stock: %s' % (instrumentId))
            fileName = self.getFileName(self.__dataSetId, instrumentId)
            if not os.path.exists(self.__cachedFolderName):
                os.mkdir(self.__cachedFolderName, 0o755)
            if not os.path.isfile(fileName):
                if not downloadFileFromYahoo(self.startDate, self.endDate, instrumentId, fileName):
                    logError('Skipping %s:' % (instrumentId))
                    continue
                if(self.adjustPrice):
                    self.adjustPriceForSplitAndDiv(instrumentId,fileName)
            with open(self.getFileName(self.__dataSetId, instrumentId)) as f:
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

    def getInstrumentUpdateFromRow(self, instrumentId, row):
        bookData = row
        for key in bookData:
            if is_number(bookData[key]):
                bookData[key] = float(bookData[key])
        timeKey = 'Date'
        timeOfUpdate = datetime.strptime(row[timeKey], '%Y-%m-%d')
        bookData.pop(timeKey, None)
        inst = StockInstrumentUpdate(stockInstrumentId=instrumentId,
                                     tradeSymbol=instrumentId,
                                     timeOfUpdate=timeOfUpdate,
                                     bookData=bookData)
        return inst

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

    def adjustPriceForSplitAndDiv(self, instrumentId, fileName):
        multiplier = data_source_utils.getMultipliers(self,instrumentId,fileName,self.__downloadId)
        temp['Close'] = temp['Close'] * multiplier[0] * multiplier[1]
        temp['Open'] = temp['Open'] * multiplier[0] * multiplier[1]
        temp['High'] = temp['High'] * multiplier[0] * multiplier[1]
        temp['Low'] = temp['Low'] * multiplier[0] * multiplier[1]

        del temp['Dividends']
        temp.to_csv(fileName)


if __name__ == "__main__":
    instrumentIds = ['IBM', 'AAPL', 'MSFT']
    startDateStr = '2013/05/10'
    endDateStr = '2017/06/09'
    YahooStockDataSource(cachedFolderName='yahooData/',
                                     dataSetId="testTrading",
                                     instrumentIds=instrumentIds,
                                     startDateStr=startDateStr,
                                     endDateStr=endDateStr,
                                     event='history')
