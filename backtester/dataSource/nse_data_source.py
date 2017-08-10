from datetime import datetime, timedelta
from backtester.instrumentUpdates import *
from backtester.constants import *
from backtester.logger import *
from data_source import DataSource
import os
import os.path
import requests
import re
try:
    from urllib import urlretrieve, urlopen
except ImportError:
    from urllib.request import urlretrieve, urlopen
from time import mktime as mktime
import pandas as pd
import csv
from bs4 import BeautifulSoup
import urllib2
from urllib import urlencode, quote
import dateutil.parser
from backtester.dataSource.yahoo_data_source import YahooStockDataSource

TYPE_LINE_UNDEFINED = 0
TYPE_LINE_HEADER = 1
TYPE_LINE_DATA = 2


def checkDate(lineItem):
    try:
        datetime.strptime(lineItem, '%d-%b-%Y') #3-Aug-15
        return True
    except ValueError:
        try:
            datetime.strptime(lineItem, '%Y-%m-%d') #3-Aug-15
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
        elif checkDate(lineItems[0]) and isFloat(lineItems[2]) and isFloat(lineItems[3]) and isFloat(lineItems[4]) and isFloat(lineItems[5]) and isFloat(lineItems[6]):
            return TYPE_LINE_DATA
            #Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty
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
            'last' : last,
            'close': closePrice,
            'average' : average,
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
    def __init__(self, cachedFolderName, instrumentIds, startDateStr, endDateStr):
        self.startDate = datetime.strptime(startDateStr, "%Y/%m/%d")
        self.endDate = datetime.strptime(endDateStr, "%Y/%m/%d")
        self.cachedFolderName = cachedFolderName
        self.instrumentIds = instrumentIds
        self.currentDate = self.startDate
        self.lineLength = 13

    def getResponseFromUrl(self,url, isxml):
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
            page = urllib2.urlopen(req)
            content = page.read()
            return content
        except urllib2.HTTPError, e:
            print e.fp.read()
            return None


    def getInitialSymbolCountUrl(self,stock):
        url = 'https://nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol=' + stock
        return url


    def getSymbolCountForStock(self,stock):
        url = self.getInitialSymbolCountUrl(stock)
        return self.getResponseFromUrl(url, False).strip()


    def getDataUrl(self,stock, symbolCount, start, end):
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

    def getDataResponseForStock(self,stock, symbolCount, start, end):
        url = self.getDataUrl(stock, symbolCount, start, end)
        return self.getResponseFromUrl(url, True)

    def parseHtmlToCSV(self, soup, outputCsvFile):
        data = soup.find(id="csvContentDiv")
        if data is None:
            print 'No data'
            return
        data = data.get_text()
        dataRows = data.split(":")
        headers = [x.replace('"', '').strip() for x in dataRows[0].split(",")[2:]]
        headers = [x.replace(' Price', '').strip() for x in headers]
        rows = []
        for row in dataRows[1:-1]:
            rows.append([x.replace('"', '').strip() for x in row.split(",")[2:]])
        
        if not os.path.isfile(outputCsvFile) :
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
        soup = BeautifulSoup(content,'lxml')
        self.parseHtmlToCSV(soup, outputCsvFile)

    def downloadFile(self, instrumentId, fileName):
        logInfo('Downloading %s'%fileName)  
        tempStart = self.startDate

        while tempStart < self.endDate:
            tempEnd = min(tempStart + timedelta(days=364), self.endDate)
            self.parseNSEUrl(instrumentId, datetime.strftime(tempStart,'%d-%m-%Y'), datetime.strftime(tempEnd,'%d-%m-%Y'), fileName)
            tempStart = tempEnd + timedelta(days=1)

    def getFileName(self, instrumentType, instrumentId):
        return '%s/%s_%s_%s_%s.csv' % (self.cachedFolderName, instrumentId, instrumentType, self.startDate.strftime("%Y%m%d"), self.endDate.strftime("%Y%m%d"))

    def emitInstrumentUpdate(self, adjustPrice=True):
        allInstrumentUpdates = []
        
        if adjustPrice:
            yahooDS_div = YahooStockDataSource(cachedFolderName=self.cachedFolderName,
                            instrumentIds=self.instrumentIds,startDateStr=datetime.strftime(self.startDate, "%Y/%m/%d"),
                            endDateStr=datetime.strftime(self.endDate, "%Y/%m/%d"),event='div')
            yahooDS_split = YahooStockDataSource(cachedFolderName=self.cachedFolderName,
                             instrumentIds=self.instrumentIds,startDateStr=datetime.strftime(self.startDate, "%Y/%m/%d"),
                            endDateStr=datetime.strftime(self.endDate, "%Y/%m/%d"),event='split')
        
        for instrumentId in self.instrumentIds:
            fileName = self.getFileName(INSTRUMENT_TYPE_STOCK, instrumentId)
            
            if not os.path.exists(self.cachedFolderName):
                os.mkdir(self.cachedFolderName, 0755)
            
            if not os.path.isfile(fileName):
                self.downloadFile(instrumentId, fileName)
                if adjustPrice:
                    self.adjustPriceForSplitAndDiv(instrumentId,fileName,yahooDS_div,yahooDS_split)
            
            fileHandler = InstrumentsFromFile(fileName=fileName, instrumentId=instrumentId)
            instrumentUpdates = fileHandler.processLinesIntoInstruments(self.lineLength)
            allInstrumentUpdates = allInstrumentUpdates + instrumentUpdates
        
        allInstrumentUpdates.sort(key=lambda x: x.getTimeOfUpdate())
        for instrumentUpdate in allInstrumentUpdates:
            yield(instrumentUpdate)

    def adjustPriceForSplitAndDiv(self, instrumentId, fileName, yahooDS_div, yahooDS_split):
        divFile = self.getFileName('div', instrumentId)
        splitFile = self.getFileName('split', instrumentId)
        if not (os.path.isfile(divFile) and os.path.isfile(splitFile)):
            yahooDS_div.downloadFile('%s.NS'%instrumentId, divFile)
            yahooDS_split.downloadFile('%s.NS'%instrumentId, splitFile)
        div = pd.read_csv(divFile, engine='python', index_col= 'Date', parse_dates=True)
        split = pd.read_csv(splitFile, engine='python', index_col= 'Date', parse_dates=True)
        prices = pd.read_csv(fileName, engine='python', index_col= 'Date', parse_dates=True)
        temp = pd.concat([div,prices],axis=1).fillna(0)
        interim=(temp['Close']-temp['Dividends'])/temp['Close']
        multiplier1 = interim.sort_index(ascending=False).cumprod().sort_index(ascending=True) 
        temp2 = split['Stock Splits'].str.split('/',expand=True)
        if len(temp2.index) > 0:
            temp_mult = pd.to_numeric(temp2[1])/pd.to_numeric(temp2[0])
            multiplier2 = temp_mult.sort_index(ascending=False).cumprod().sort_index(ascending=True)
        else:
            multiplier2 = pd.Series(1, index = multiplier1.index)
        multiplier = pd.concat([multiplier1,multiplier2],axis=1).fillna(method='bfill').fillna(1)
        multiplier[1] = multiplier[1].shift(-1).fillna(1)
        temp['Close'] = temp['Close']* multiplier[0]*multiplier[1]
        temp['Open'] = temp['Open']* multiplier[0]*multiplier[1]
        temp['High'] = temp['High']* multiplier[0]*multiplier[1]
        temp['Low'] = temp['Low']* multiplier[0]*multiplier[1]
        temp['Last'] = temp['Last']* multiplier[0]*multiplier[1]
        temp['Average'] = temp['Average'] * multiplier[0]*multiplier[1]
        temp['Total Traded Quantity'] = temp['Total Traded Quantity']/multiplier[1]
        temp['Turnover'] =  temp['Turnover'] * multiplier[0]
        temp['Deliverable Qty'] = temp['Deliverable Qty']/multiplier[1]

        del temp['Dividends']
        temp.to_csv(fileName)


