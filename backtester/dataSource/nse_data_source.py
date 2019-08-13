from datetime import datetime, timedelta
from backtester.instrumentUpdates import *
from backtester.constants import *
from backtester.logger import *
from backtester.dataSource.data_source import DataSource
import os
import os.path
import pandas as pd
import csv
from bs4 import BeautifulSoup
try:
    import urllib.request as urllib2
    from urllib.request import urlopen
    import urllib.error as urllib2
    from urllib.parse import quote
except ImportError:
    import urllib2
    from urllib2 import urlopen
    from urllib import quote
import backtester.dataSource.data_source_utils as data_source_utils
TYPE_LINE_UNDEFINED = 0
TYPE_LINE_HEADER = 1
TYPE_LINE_DATA = 2


def checkDate(lineItem):
    try:
        datetime.strptime(lineItem, '%d-%b-%Y')  # 3-Aug-15
        return True
    except ValueError:
        try:
            datetime.strptime(lineItem, '%Y-%m-%d')  # 3-Aug-15
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

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Returns the type of lineItems


def validateLineItem(lineItems, lineLength):
    if len(lineItems) == lineLength:
        if lineItems[0] == "Date":
            return TYPE_LINE_HEADER
        elif checkDate(lineItems[0]) and isFloat(lineItems[2]) and isFloat(lineItems[3]) and isFloat(lineItems[4]) and isFloat(lineItems[5]) and isFloat(lineItems[6]):
            return TYPE_LINE_DATA
            # Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty
    print(len(lineItems), lineLength, checkDate(lineItems[0]))
    logInfo('Bad Line')
    return TYPE_LINE_UNDEFINED


def parseDataLine(lineItems, lineLength):
    if (len(lineItems) != lineLength):
        logInfo('Bad Line')
        return None
    openPrice = float(lineItems[2])
    high = float(lineItems[3])
    low = float(lineItems[4])
    last = float(lineItems[5])
    closePrice = float(lineItems[6])
    average = float(lineItems[7])
    volume = float(lineItems[8])
    return {'open': openPrice,
            'high': high,
            'low': low,
            'last': last,
            'close': closePrice,
            'average': average,
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
                try:
                    self.currentTimeOfUpdate = datetime.strptime(lineItems[0], '%d-%b-%Y')
                except ValueError:
                    self.currentTimeOfUpdate = datetime.strptime(lineItems[0], '%Y-%m-%d')
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


class NSEStockDataSource(DataSource):
    def __init__(self, cachedFolderName, dataSetId, instrumentIds, startDateStr, endDateStr, adjustPrice=False, downloadId = ".NS", liveUpdates=True, pad=True):
        super(NSEStockDataSource, self).__init__(cachedFolderName, dataSetId, instrumentIds, startDateStr, endDateStr)
        self.__dateAppend = "_%sto%s"%(datetime.strptime(startDateStr, '%Y/%m/%d').strftime('%Y-%m-%d'),datetime.strptime(startDateStr, '%Y/%m/%d').strftime('%Y-%m-%d'))
        self.__downloadId = downloadId
        self.__bookDataByFeature = {}
        self.__adjustPrice = adjustPrice
        self.currentDate = self._startDate
        if liveUpdates:
            self._allTimes, self._groupedInstrumentUpdates = self.getGroupedInstrumentUpdates()
            self.processGroupedInstrumentUpdates()
            self._bookDataFeatureKeys = self.__bookDataByFeature.keys()
        else:
            self._allTimes, self._bookDataByInstrument = self.getAllInstrumentUpdates()
            if pad:
                self.padInstrumentUpdates()
            self.filterUpdatesByDates([(startDateStr, endDateStr)])
        self.lineLength = 13

    def getResponseFromUrl(self, url, isxml):
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'en-US,en;q=0.8',
               'Host': 'nseindia.com',
               'Connection': 'keep-alive',
               'Referer': 'https://nseindia.com/products/content/equities/equities/eq_security.htm',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'}
        if isxml:
            hdr['X-Requested-With'] = 'XMLHttpRequest'
        req = urllib2.Request(url, headers=hdr)
        try:
            page = urlopen(req)
            content = page.read().decode('utf8')
            return content
        except urllib2.HTTPError as e:
            print(e.fp.read())
            return None

    def getInitialSymbolCountUrl(self, stock):
        url = 'https://nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol=' + stock
        return url

    def getSymbolCountForStock(self, stock):
        url = self.getInitialSymbolCountUrl(stock)
        return self.getResponseFromUrl(url, False).strip()

    def getDataUrl(self, stock, symbolCount, start, end):
        parameters = {'symbol': stock,
                      'segmentLink': '3',
                      'symbolCount': symbolCount,
                      'series': 'EQ',
                      'dateRange': '+',
                      'fromDate': start,
                      'toDate': end,
                      'dataType': 'PRICEVOLUMEDELIVERABLE'}
        orderedKeys = ['symbol', 'segmentLink', 'symbolCount', 'series', 'dateRange', 'fromDate', 'toDate', 'dataType']
        encodedparams = "&".join("%s=%s" % (key, quote(
            parameters[key], safe="+")) for key in orderedKeys)
        return 'https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?' + encodedparams

    def getDataResponseForStock(self, stock, symbolCount, start, end):
        url = self.getDataUrl(stock, symbolCount, start, end)
        return self.getResponseFromUrl(url, True)

    def parseHtmlToCSV(self, soup, outputCsvFile):
        data = soup.find(id="csvContentDiv")
        if data is None:
            print('No data')
            return
        data = data.get_text()
        dataRows = data.split(":")
        headers = [x.replace('"', '').strip() for x in dataRows[0].split(",")[2:]]
        headers = [x.replace(' Price', '').strip() for x in headers]
        rows = []
        for row in dataRows[1:-1]:
            rows.append([x.replace('"', '').strip() for x in row.split(",")[2:]])
        if not os.path.isfile(outputCsvFile):
            f = open(outputCsvFile, 'wb')
            writer = csv.writer(f)
            writer.writerow(headers)
            f.close()

        with open(outputCsvFile, 'ab') as f:
            writer = csv.writer(f)
            writer.writerows(row for row in rows if row)
            f.close()

    def parseNSEUrl(self, stock, start, end, outputCsvFile):
        symbolCount = self.getSymbolCountForStock(stock)
        content = self.getDataResponseForStock(stock, symbolCount, start, end)
        soup = BeautifulSoup(content, 'lxml')
        self.parseHtmlToCSV(soup, outputCsvFile)

    def downloadFile(self, instrumentId, fileName):
        logInfo('Downloading %s' % fileName)
        tempStart = self._startDate
        while tempStart < self._endDate:
            tempEnd = min(tempStart + timedelta(days=364), self._endDate)
            self.parseNSEUrl(instrumentId, datetime.strftime(tempStart, '%d-%m-%Y'), datetime.strftime(tempEnd, '%d-%m-%Y'), fileName)
            tempStart = tempEnd + timedelta(days=1)
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

    def getInstrumentUpdateFromRow(self, instrumentId, row):
        bookData = row
        for key in bookData:
            if is_number(bookData[key]):
                bookData[key] = float(bookData[key])
        timeKey = 'Date'
        timeOfUpdate = datetime.strptime(row[timeKey], '%d-%b-%Y')
        bookData.pop(timeKey, None)
        inst = StockInstrumentUpdate(stockInstrumentId=instrumentId,
                                     tradeSymbol=instrumentId,
                                     timeOfUpdate=timeOfUpdate,
                                     bookData=bookData)
        return inst

    def getBookDataByFeature(self):
        return self.__bookDataByFeature

    def getClosingTime(self):
        return self._allTimes[-1]

    def adjustPriceForSplitAndDiv(self, instrumentId, fileName):
        multiplier = data_source_utils.getMultipliers(self,instrumentId,fileName,self.__downloadId)
        temp['Close'] = temp['Close'] * multiplier[0] * multiplier[1]
        temp['Open'] = temp['Open'] * multiplier[0] * multiplier[1]
        temp['High'] = temp['High'] * multiplier[0] * multiplier[1]
        temp['Low'] = temp['Low'] * multiplier[0] * multiplier[1]
        temp['Last'] = temp['Last'] * multiplier[0] * multiplier[1]
        temp['Average'] = temp['Average'] * multiplier[0] * multiplier[1]
        temp['Total Traded Quantity'] = temp['Total Traded Quantity'] / multiplier[1]
        temp['Turnover'] = temp['Turnover'] * multiplier[0]
        temp['Deliverable Qty'] = temp['Deliverable Qty'] / multiplier[1]

        del temp['Dividends']
        temp.to_csv(fileName)
