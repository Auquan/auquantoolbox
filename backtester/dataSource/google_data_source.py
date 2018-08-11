from datetime import datetime
from backtester.instrumentUpdates import *
from backtester.constants import *
from backtester.logger import *
from backtester.dataSource.data_source import DataSource
import os
import os.path
from pandas_datareader import data
from backtester.dataSource.data_source_utils import downloadFileFromYahoo, groupAndSortByTimeUpdates

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
    def __init__(self, cachedFolderName, instrumentIds, startDateStr, endDateStr):
        self.startDate = datetime.strptime(startDateStr, "%Y/%m/%d")
        self.endDate = datetime.strptime(endDateStr, "%Y/%m/%d")
        self.cachedFolderName = cachedFolderName
        self.instrumentIds = instrumentIds
        self.currentDate = self.startDate
        self.lineLength = 6

    def downloadFile(self, instrumentId, fileName):
        logInfo('Downloading %s' % fileName)
        pd = data.DataReader(instrumentId, 'google', self.startDate, self.endDate)
        pd.to_csv(fileName)

    def getFileName(self, instrumentType, instrumentId):
        return '%s/%s_%s_%s_%s.csv' % (self.cachedFolderName, instrumentId, instrumentType, self.startDate.strftime("%Y%m%d"), self.endDate.strftime("%Y%m%d"))

    def emitInstrumentUpdates(self, adjustPrice=True):
        allInstrumentUpdates = []

        for instrumentId in self.instrumentIds:
            fileName = self.getFileName(INSTRUMENT_TYPE_STOCK, instrumentId)
            if not os.path.exists(self.cachedFolderName):
                os.mkdir(self.cachedFolderName, 0o755)
            if not os.path.isfile(fileName):
                self.downloadFile(instrumentId, fileName)
                if adjustPrice:
                    self.adjustPriceForSplitAndDiv(instrumentId, fileName)
            fileHandler = InstrumentsFromFile(fileName=fileName, instrumentId=instrumentId)
            instrumentUpdates = fileHandler.processLinesIntoInstruments()
            allInstrumentUpdates = allInstrumentUpdates + instrumentUpdates

        groupedInstrumentUpdates = groupAndSortByTimeUpdates(allInstrumentUpdates)
        for timeOfUpdate, instrumentUpdates in groupedInstrumentUpdates:
            yield([timeOfUpdate, instrumentUpdates])

    def adjustPriceForSplitAndDiv(self, instrumentId, fileName):
        divFile = self.getFileName('div', instrumentId)
        splitFile = self.getFileName('split', instrumentId)
        if not (os.path.isfile(divFile) and os.path.isfile(splitFile)):
            downloadFileFromYahoo(self.startDate, self.endDate, '%s.NS' % instrumentId, divFile, event='div')
            downloadFileFromYahoo(self.startDate, self.endDate, '%s.NS' % instrumentId, splitFile, event='split')
        div = pd.read_csv(divFile, engine='python', index_col='Date', parse_dates=True)
        split = pd.read_csv(splitFile, engine='python', index_col='Date', parse_dates=True)
        prices = pd.read_csv(fileName, engine='python', index_col='Date', parse_dates=True)
        temp = pd.concat([div, prices], axis=1).fillna(0)
        interim = (temp['Close'] - temp['Dividends']) / temp['Close']
        multiplier1 = interim.sort_index(ascending=False).cumprod().sort_index(ascending=True)
        temp2 = split['Stock Splits'].str.split('/', expand=True)
        if len(temp2.index) > 0:
            temp_mult = pd.to_numeric(temp2[1]) / pd.to_numeric(temp2[0])
            multiplier2 = temp_mult.sort_index(ascending=False).cumprod().sort_index(ascending=True)
        else:
            multiplier2 = pd.Series(1, index=multiplier1.index)
        multiplier = pd.concat([multiplier1, multiplier2], axis=1).fillna(method='bfill').fillna(1)
        multiplier[1] = multiplier[1].shift(-1).fillna(1)
        temp['Close'] = temp['Close'] * multiplier[0] * multiplier[1]
        temp['Open'] = temp['Open'] * multiplier[0] * multiplier[1]
        temp['High'] = temp['High'] * multiplier[0] * multiplier[1]
        temp['Low'] = temp['Low'] * multiplier[0] * multiplier[1]
        temp['Volume'] = temp['Volume'] / multiplier[1]

        del temp['Dividends']
        temp.to_csv(fileName)
