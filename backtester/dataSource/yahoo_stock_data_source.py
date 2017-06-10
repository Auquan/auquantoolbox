try:
    # py3
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
except ImportError:
    # py2
    from urllib2 import Request, urlopen
    from urllib import urlencode
from datetime import datetime, timedelta
from backtester.instrumentUpdates import *
from backtester.constants import *
from data_source import DataSource
import os.path
import pandas


def get_historical_prices(symbol, start_date, end_date):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYY-MM-DD'
    Returns a nested dictionary (dict of dicts).
    outer dict keys are dates ('YYYY-MM-DD')
    """
    params = urlencode({
        's': symbol,
        'a': int(start_date[5:7]) - 1,
        'b': int(start_date[8:10]),
        'c': int(start_date[0:4]),
        'd': int(end_date[5:7]) - 1,
        'e': int(end_date[8:10]),
        'f': int(end_date[0:4]),
        'g': 'd',
        'ignore': '.csv',
    })
    url = 'http://real-chart.finance.yahoo.com/table.csv?%s' % params
    req = Request(url)
    resp = urlopen(req)
    content = str(resp.read().decode('utf-8').strip())
    daily_data = content.splitlines()
    hist_dict = dict()
    keys = daily_data[0].split(',')
    for day in daily_data[1:]:
        day_data = day.split(',')
        date = day_data[0]
        hist_dict[date] = \
            {keys[1]: day_data[1],
             keys[2]: day_data[2],
             keys[3]: day_data[3],
             keys[4]: day_data[4],
             keys[5]: day_data[5],
             keys[6]: day_data[6]}
    return hist_dict


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


# Returns the type of lineItems
def validateLineItem(lineItems):
    if len(lineItems) == 6:
        if lineItems[0] == "Date":
            return TYPE_LINE_HEADER
        elif checkDate(lineItems[0]):
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
    def __init__(self, cachedFolderName, stockSymbols, startDateStr, endDateStr):
        self.startDate = datetime.strptime(startDateStr, "%Y/%m/%d")
        self.endDate = datetime.strptime(endDateStr, "%Y/%m/%d")
        self.cachedFolderName = cachedFolderName
        self.stockSymbols = stockSymbols
        self.currentDate = self.startDate

    def downloadFile(self, instrumentId, fileName):
        data = get_historical_prices(instrumentId, self.startDate.strftime("%Y-%m-%d"), self.endDate.strftime("%Y-%m-%d"))
        pd = data.DataReader(instrumentId, 'google', self.startDate, self.endDate)
        pd.to_csv(fileName)

    def getFileName(self, instrumentType, instrumentId):
        return '%s/%s/%s_%s_%s.csv' % (self.folderName, instrumentType, instrumentId, self.startDate.strftime("%Y%m%d"), self.startDate.strftime("%Y%m%d"))

    def emitInstrumentUpdate(self):
        while (self.currentDate <= self.endDate):
            allInstrumentUpdates = []
            for instrumentType in self.instrumentIdsByType:
                instrumentIds = self.instrumentIdsByType[instrumentType]
                for instrumentId in instrumentIds:
                    fileName = self.getFileName(instrumentType, instrumentId)
                    if not os.path.isfile(fileName):
                        self.downloadFile(instrumentId, fileName)
                    fileHandler = InstrumentsFromFile(fileName=fileName, instrumentId=instrumentId)
                    instrumentUpdates = fileHandler.processLinesIntoInstruments()
                    allInstrumentUpdates = allInstrumentUpdates + instrumentUpdates
            allInstrumentUpdates.sort(key=lambda x: x.getTimeOfUpdate())
            for instrumentUpdate in allInstrumentUpdates:
                yield(instrumentUpdate)
            self.currentDate = self.currentDate + timedelta(days=1)


if __name__ == "__main__":
    ds = GoogleDataSource('a', '', '2017/05/10', '2017/06/09')
    
