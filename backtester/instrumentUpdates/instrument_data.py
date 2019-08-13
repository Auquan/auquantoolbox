import pandas as pd
import numpy as np
from backtester.constants import *


class InstrumentData(object):
    '''
    '''
    def __init__(self, instrumentId, tradeSymbol, fileName=None, chunkSize=None):
        self.__instrumentId = instrumentId
        self.__tradeSymbol = tradeSymbol
        self.__fileName = fileName
        self.__bookDataSize = None
        if chunkSize is None:
            if fileName:
                self.__bookData = pd.read_csv(fileName, index_col=0, parse_dates=True, dtype=float)
                self.__bookData.dropna(inplace=True)
                self.__bookDataSize = len(self.__bookData)
            self.getBookDataChunk = self.__getBookDataInChunksFromDataFrame
        else:
            self.__bookData = pd.read_csv(fileName, index_col=0, parse_dates=True, dtype=float, chunksize=chunkSize)
            self.getBookDataChunk = self.__getBookDataInChunksFromFile

    def getInstrumentId(self):
        return self.__instrumentId

    def getTradeSymbol(self):
        return self.__tradeSymbol

    def getBookDataSize(self):
        if self.__bookDataSize is None:
            self.__bookDataSize = len(pd.read_csv(self.__fileName, index_col=0, usecols=[0]))
        return self.__bookDataSize

    def setBookData(self, data):
        self.__bookData = data
        self.__bookDataSize = len(self.__bookData)

    def getBookData(self):
        return self.__bookData

    def getBookDataByFeature(self, feature):
        return self.__bookData[feature]

    # returns a chunk from already completely loaded data
    def __getBookDataInChunksFromDataFrame(self, chunkSize):
        if chunkSize <=0 :
            logError("chunkSize must be a positive integer")
        for chunkNumber, bookDataChunk in self.__bookData.groupby(np.arange(self.__bookDataSize) // chunkSize):
            yield (chunkNumber, bookDataChunk)

    # returns a chunk from __bookData generator after processing data
    # TODO: implement proper padding such that all instruments have same index set (timeUpdates)
    def __getBookDataInChunksFromFile(self, dateRange):
        chunkNumber = -1
        for bookDataChunk in self.__bookData:
            chunkNumber += 1
            bookDataChunk = self.filterDataByDates(bookDataChunk, dateRange)
            yield (chunkNumber, bookDataChunk)

    # returns all timestamps in pandas series format
    def getAllTimestamps(self):
        if isinstance(self.__bookData, pd.DataFrame):
            return self.__bookData.index
        else:
            return pd.read_csv(self.__fileName, index_col=0, usecols=[0]).index

    # returns list of bookDataFeatures (columns)
    def getBookDataFeatures(self):
        if isinstance(self.__bookData, pd.DataFrame):
            return list(self.__bookData.columns)
        else:
            return list(pd.read_csv(self.__fileName, index_col=0, nrows=1).columns)

    def getTypeOfInstrument(self):
        return INSTRUMENT_TYPE_STOCK

    def filterDataByDates(self, dateRange):
        if (dateRange is []) or (dateRange is ()):
            return
        elif type(dateRange) is list:
            frames = []
            for dr in dateRange:
                frames.append(self.__bookData[dr[0]:dr[1]])
            self.__bookData = pd.concat(frames)
        else:
            self.__bookData = self.__bookData[dateRange[0]:dateRange[1]]
        self.__bookDataSize = len(self.__bookData)

    def padInstrumentData(self, timeUpdates, method='ffill'):
        timeUpdateSeries = pd.Series(timeUpdates)
        if not timeUpdateSeries.isin(self.__bookData.index).all():
            df = pd.DataFrame(index=timeUpdates, columns=self.__bookData.columns)
            df.at[self.__bookData.index] = self.__bookData.copy()
            df.fillna(method=method, inplace=True)
            df.fillna(0.0, inplace=True)
            del self.__bookData
            self.__bookData = df
            self.__bookDataSize = len(self.__bookData)

    # For internal use only
    def __padInstrumentData(self, timeUpdates, data, method='ffill'):
        timeUpdateSeries = pd.Series(timeUpdates)
        if not timeUpdateSeries.isin(data.index).all():
            newDataDf = pd.DataFrame(index=timeUpdates, columns=data.columns)
            newDataDf.at[data.index] = data
            newDataDf.fillna(method=method, inplace=True)
            newDataDf.fillna(0.0, inplace=True)
            return newDataDf
        return data

    def __filterDataByDates(self, data, dateRange):
        if (dateRange is []) or (dateRange is ()) or data is None:
            return data
        elif type(dateRange) is list:
            frames = []
            for dr in dateRange:
                frames.append(data[dr[0]:dr[1]])
            return pd.concat(frames)
        else:
            return data[dateRange[0]:dateRange[1]]
