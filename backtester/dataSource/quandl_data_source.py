from backtester.dataSource.data_source import DataSource
from backtester.instrumentUpdates import *
import os
from datetime import datetime
import csv
from backtester.logger import *
try:
    from urllib2 import urlopen
    import urllib2 as ue
except ImportError:
    from urllib.request import urlopen
    import urllib.error as ue
import pandas as pd
import time

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def checkDate(lineItem):
    try:
        datetime.strptime(lineItem, '%Y-%m-%d')
        return True
    except ValueError:
        return False

class QuandlDataSource(DataSource):
    def __init__(self, cachedFolderName, dataSetId, instrumentIds, startDate, endDate, liveUpdates=True, pad=True):
        super(QuandlDataSource, self).__init__(cachedFolderName, dataSetId, instrumentIds, startDate, endDate)
        if(not checkDate(startDate)):
            self.__startDate = datetime.strptime(startDate, '%Y/%m/%d').strftime('%Y-%m-%d')
        if(not checkDate(endDate)):
            self.__endDate = datetime.strptime(endDate, '%Y/%m/%d').strftime('%Y-%m-%d')
        self.__dateAppend = "_%sto%s"%(datetime.strptime(startDate, '%Y/%m/%d').strftime('%Y-%m-%d'),datetime.strptime(startDate, '%Y/%m/%d').strftime('%Y-%m-%d'))
        self.__bookDataByFeature = {}
        if liveUpdates:
            self._allTimes, self._groupedInstrumentUpdates = self.getGroupedInstrumentUpdates()
            print ('Processing instruments before beginning backtesting. This could take some time...')
            self.processGroupedInstrumentUpdates()
            self._bookDataFeatureKeys = self.__bookDataByFeature.keys()
        else:
            self._allTimes, self._bookDataByInstrument = self.getAllInstrumentUpdates()
            if pad:
                self.padInstrumentUpdates()
            self.filterUpdatesByDates([(startDate, endDate)])

    def downloadFile(self, instrumentId, downloadLocation):
        url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.csv?start_date=%s&end_date=%s'%(instrumentId,self.__startDate,self.__endDate)
        try:
            response = urlopen(url)
        except ue.HTTPError:
            logError('Instrument not present')
            return False
        status = response.getcode()
        if status == 200:
            print('Downloading %s data to file: %s' % (instrumentId, downloadLocation))
            with open(downloadLocation, 'w') as f:
                f.write(response.read().decode('utf8'))
            return True
        else:
            logError('File not found. Please check settings!')
            return False

    def downloadAndAdjustData(self, instrumentId, fileName):
        if not os.path.isfile(fileName):
            if not self.downloadFile(instrumentId, fileName):
                logError('Skipping %s:' % (instrumentId))
                return False
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
        timeOfUpdate = datetime.strptime(row[timeKey], '%Y-%m-%d')
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
