from datetime import datetime
from backtester.instrumentUpdates import *
from backtester.constants import *
from backtester.logger import *
from backtester.dataSource.data_source import DataSource
import os
import os.path
import csv
import pandas as pd
from pandas_datareader import data
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


def validateLineItem(lineItems, lineLength):
    if len(lineItems) == lineLength:
        if lineItems[0] == "Date":
            return TYPE_LINE_HEADER
        elif checkDate(lineItems[0]) and isFloat(lineItems[1]) and isFloat(lineItems[2]) and isFloat(lineItems[3]) and isFloat(lineItems[4]) and isFloat(lineItems[5]):
            return TYPE_LINE_DATA
    return TYPE_LINE_UNDEFINED


def parseDataLine(lineItems, lineLength):
    if (len(lineItems) != lineLength):
        return None
    openPrice = float(lineItems[1])
    high = float(lineItems[2])
    low = float(lineItems[3])
    closePrice = float(lineItems[4])
    volume = float(lineItems[5])
    return {'open': openPrice,
            'high': high,
            'low': low,
            'close': closePrice,
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

    def processLine(self, line, lineLength):
        lineItems = line.split(',')
        lineItemType = validateLineItem(lineItems, lineLength)
        if (lineItemType == TYPE_LINE_DATA):
            inst = None
            if self.currentInstrumentSymbol is not None:
                self.currentTimeOfUpdate = datetime.strptime(lineItems[0], "%Y-%m-%d")
                self.currentInstrumentSymbol = self.instrumentId
                self.currentBookData = parseDataLine(lineItems, lineLength)
                if self.currentBookData is None:
                    return None
                # right now only works for stocks
                inst = StockInstrumentUpdate(stockInstrumentId=self.instrumentId,
                                             tradeSymbol=self.currentInstrumentSymbol,
                                             timeOfUpdate=self.currentTimeOfUpdate,
                                             bookData=self.currentBookData)
                return inst
        return None

    def processLinesIntoInstruments(self, lineLength):
        with open(self.fileName, "r") as ins:
            instruments = []
            for line in ins:
                inst = self.processLine(line, lineLength)
                if inst is not None:
                    instruments.append(inst)
            return instruments


class GoogleStockDataSource(DataSource):
    def __init__(self, cachedFolderName, dataSetId, instrumentIds, startDateStr, endDateStr, adjustPrice=False, downloadId = ".NS", liveUpdates=True, pad=True):
        super(GoogleStockDataSource, self).__init__(cachedFolderName, dataSetId, instrumentIds, startDateStr, endDateStr)
        self.__downloadId = downloadId
        self.__dateAppend = "_%sto%s"%(datetime.strptime(startDateStr, '%Y/%m/%d').strftime('%Y-%m-%d'),datetime.strptime(startDateStr, '%Y/%m/%d').strftime('%Y-%m-%d'))
        self.__adjustPrice = adjustPrice
        self.__bookDataByFeature = {}
        self.currentDate = self._startDate
        if liveUpdates:
            self._allTimes, self._groupedInstrumentUpdates = self.getGroupedInstrumentUpdates()
            self.processGroupedInstrumentUpdates()
        else:
            self._allTimes, self._instrumentDataDict = self.getAllInstrumentUpdates()
            if pad:
                self.padInstrumentUpdates()
            # self._allTimes, self._groupedInstrumentUpdates = self.getGroupedInstrumentUpdates()
            # self.processAllInstrumentUpdates(pad=pad)
            # del self._groupedInstrumentUpdates
            self.filterUpdatesByDates([(startDateStr, endDateStr)])
        self.lineLength = 6

    def downloadFile(self, instrumentId, fileName):
        logInfo('Downloading %s' % fileName)
        pd = data.DataReader(instrumentId, 'google', self._startDate, self._endDate)
        pd.to_csv(fileName)
        return True

    def downloadAndAdjustData(self, instrumentId, fileName):
        if not os.path.isfile(fileName):
            if not self.downloadFile(instrumentId, fileName):
                logError('Skipping %s:' % (instrumentId))
                return False
            if(self.__adjustPrice):
                self.adjustPriceForSplitAndDiv(instrumentId, fileName)
        return True

    def getFileName(self, instrumentId):
        return self._cachedFolderName + self._dataSetId + '/' + instrumentId + '%s.csv'%self.__dateAppend

    def processGroupedInstrumentUpdates(self):
        timeUpdates = self._allTimes
        # for timeOfUpdate, instrumentUpdates in self._groupedInstrumentUpdates:
        #     timeUpdates.append(timeOfUpdate)
        # self._allTimes = timeUpdates

        limits = [0.20, 0.40, 0.60, 0.80, 1.0]
        if (len(self._instrumentIds) > 30):
            limits = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0]
        currentLimitIdx = 0
        idx = 0.0
        for timeOfUpdate, instrumentUpdates in self._groupedInstrumentUpdates:
            idx = idx + 1.0
            if (idx / len(timeUpdates)) > limits[currentLimitIdx]:
                print ('%d%% done...' % (limits[currentLimitIdx] * 100))
                currentLimitIdx = currentLimitIdx + 1
            for instrumentUpdate in instrumentUpdates:
                bookData = instrumentUpdate.getBookData()
                for featureKey in bookData:
                    # TODO: Fix for python 3
                    if featureKey not in self.__bookDataByFeature:
                        self.__bookDataByFeature[featureKey] = pd.DataFrame(columns=self._instrumentIds,
                                                                            index=timeUpdates)
                    self.__bookDataByFeature[featureKey].set_value(timeOfUpdate, instrumentUpdate.getInstrumentId(), bookData[featureKey])
        for featureKey in self.__bookDataByFeature:
            self.__bookDataByFeature[featureKey].fillna(method='pad', inplace=True)

    # def getInstrumentUpdateFromRow(self, instrumentId, row):
    #     bookData = row
    #     for key in bookData:
    #         if is_number(bookData[key]):
    #             bookData[key] = float(bookData[key])
    #     timeKey = 'Date'
    #     timeOfUpdate = datetime.strptime(row[timeKey], '%Y-%m-%d')
    #     bookData.pop(timeKey, None)
    #     inst = StockInstrumentUpdate(stockInstrumentId=instrumentId,
    #                                  tradeSymbol=instrumentId,
    #                                  timeOfUpdate=timeOfUpdate,
    #                                  bookData=bookData)
    #     return inst

    def getInstrumentUpdateFromRow(self, instrumentId, row):
        bookData =  {'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': float(row['Volume'])}

        timeOfUpdate = datetime.strptime(row['Date'], '%Y-%m-%d')
        inst = StockInstrumentUpdate(stockInstrumentId=instrumentId,
                                     tradeSymbol=instrumentId,
                                     timeOfUpdate=timeOfUpdate,
                                     bookData=bookData)
        return inst

    def getBookDataByFeature(self):
        return self.__bookDataByFeature

    def getClosingTime(self):
        return self._allTimes[-1]

    def getBookDataFeatures(self):
        return self.__bookDataByFeature.keys()

    def adjustPriceForSplitAndDiv(self, instrumentId, fileName):
        multiplier = data_source_utils.getMultipliers(self,instrumentId,fileName,self.__downloadId)
        temp['Close'] = temp['Close'] * multiplier[0] * multiplier[1]
        temp['Open'] = temp['Open'] * multiplier[0] * multiplier[1]
        temp['High'] = temp['High'] * multiplier[0] * multiplier[1]
        temp['Low'] = temp['Low'] * multiplier[0] * multiplier[1]
        temp['Volume'] = temp['Volume'] / multiplier[1]

        del temp['Dividends']
        temp.to_csv(fileName)
