from datetime import datetime
from backtester.instrumentUpdates import *
from backtester.constants import *
from data_source import DataSource
import os
import os.path
from pandas_datareader import data

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
    if len(lineItems) == 6:
        if lineItems[0] == "Date":
            return TYPE_LINE_HEADER
        elif checkDate(lineItems[0]) and isFloat(lineItems[1]) and isFloat(lineItems[2]) and isFloat(lineItems[3]) and isFloat(lineItems[4]) and isFloat(lineItems[5]):
            return TYPE_LINE_DATA
    return TYPE_LINE_UNDEFINED


def parseDataLine(lineItems):
    if (len(lineItems) != 6):
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


class GoogleStockDataSource(DataSource):
    def __init__(self, cachedFolderName, instrumentIds, startDateStr, endDateStr):
        self.startDate = datetime.strptime(startDateStr, "%Y/%m/%d")
        self.endDate = datetime.strptime(endDateStr, "%Y/%m/%d")
        self.cachedFolderName = cachedFolderName
        self.instrumentIds = instrumentIds
        self.currentDate = self.startDate

    def downloadFile(self, instrumentId, fileName):
        pd = data.DataReader(instrumentId, 'google', self.startDate, self.endDate)
        pd.to_csv(fileName)

    def getFileName(self, instrumentType, instrumentId):
        return '%s/%s_%s_%s_%s.csv' % (self.cachedFolderName, instrumentId, instrumentType, self.startDate.strftime("%Y%m%d"), self.endDate.strftime("%Y%m%d"))

    def emitInstrumentUpdate(self):
        allInstrumentUpdates = []
        for instrumentId in self.instrumentIds:
            fileName = self.getFileName(INSTRUMENT_TYPE_STOCK, instrumentId)
            if not os.path.exists(self.cachedFolderName):
                os.mkdir(self.cachedFolderName, 0755)
            if not os.path.isfile(fileName):
                self.downloadFile(instrumentId, fileName)
            fileHandler = InstrumentsFromFile(fileName=fileName, instrumentId=instrumentId)
            instrumentUpdates = fileHandler.processLinesIntoInstruments()
            allInstrumentUpdates = allInstrumentUpdates + instrumentUpdates
        allInstrumentUpdates.sort(key=lambda x: x.getTimeOfUpdate())
        for instrumentUpdate in allInstrumentUpdates:
            yield(instrumentUpdate)


if __name__ == "__main__":
    a = datetime.strptime('2017/06/30', "%Y/%m/%d")
    print get_exp_date(a)
