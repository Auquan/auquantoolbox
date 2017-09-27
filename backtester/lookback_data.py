import pandas as pd
from collections import deque
import numpy as np

SIZE_FACTOR = 3
MIN_THRESHOLD = 500
MAX_THRESHOLD = 2000


class LookbackDataEfficient:
    def __init__(self, lookbackSize, columns, indexList):
        self.__lookbackSize = lookbackSize
        self.__columns = columns
        self.__indexList = indexList
        self.__startLookbackData = 0
        self.__endLookbackData = 0
        self.__endIndexList = 0
        self.__maxSize = self.computeMaxSize(lookbackSize, len(indexList))
        newEndIndexList = self.__endIndexList + self.__maxSize if (len(indexList) > self.__endIndexList + self.__maxSize) else len(self.__indexList)
        self.__data = pd.DataFrame(columns=self.__columns, index=self.__indexList[self.__endIndexList:newEndIndexList])
        self.__endIndexList = newEndIndexList
        self.__hasSetOnce = False

    def computeMaxSize(self, lookbackSize, lenIndexList):
        maxSize = lookbackSize * SIZE_FACTOR
        if (maxSize < MIN_THRESHOLD):
            maxSize = MIN_THRESHOLD
        if (maxSize > MAX_THRESHOLD):
            maxSize = MAX_THRESHOLD
        if (maxSize > lenIndexList):
            return lenIndexList
        if (maxSize < lookbackSize):
            return lookbackSize * SIZE_FACTOR
        return maxSize

    def addData(self, timeOfUpdate, data):
        if (self.__endLookbackData == self.__maxSize):
            # make a new dataframe and copy
            newEndIndexList = self.__endIndexList - self.__lookbackSize + self.__maxSize
            if newEndIndexList > len(self.__indexList):
                newEndIndexList = len(self.__indexList)
            newData = pd.DataFrame(columns=self.__columns, index=self.__indexList[self.__endIndexList - self.__lookbackSize: newEndIndexList])
            self.__endIndexList = newEndIndexList
            newData.iloc[0:self.__lookbackSize] = self.__data.iloc[self.__startLookbackData:self.__endLookbackData]
            self.__startLookbackData = 0
            self.__endLookbackData = self.__lookbackSize
            self.__data = newData
            self.__hasSetOnce = False
        self.__data.loc[timeOfUpdate] = data
        self.__endLookbackData = self.__endLookbackData + 1
        if (self.__endLookbackData - self.__startLookbackData) > self.__lookbackSize:
            self.__startLookbackData = self.__startLookbackData + 1
        if not self.__hasSetOnce:
            self.__data = self.__data.astype(float, errors='ignore')
            self.__hasSetOnce = True

    def getData(self):
        return self.__data.iloc[self.__startLookbackData:self.__endLookbackData]


class LookbackData:
    def __init__(self, size, columns):
        self.__size = size
        self.__columns = columns
        self.__storedData = deque([])
        self.__times = deque([])
        self.__data = pd.DataFrame(data=list(self.__storedData), columns=self.__columns, index=list(self.__times))
        # self.__data = pd.DataFrame(data=self.__storedData, columns=self.__columns, index=self.__times)
        # self.__storedData = pd.DataFrame(columns=columns)

    def addData(self, timeOfUpdate, data):
        self.__storedData.append(data)
        self.__times.append(timeOfUpdate)
        if len(self.__storedData) > self.__size:
            self.__storedData.popleft()
            self.__times.popleft()
        self.__data = pd.DataFrame(data=list(self.__storedData), columns=self.__columns, index=list(self.__times))
        # self.__storedData.loc[timeOfUpdate] = data

    '''
    returns a pandas dataframe index is time.
    '''
    def getData(self):
        return self.__data

    def getLastData(self):
        return self.__data.iloc[-1]

    def addFeatureVal(self, timeOfUpdate, featureKey, featureVal):
        # have to do this because in case featureVal is a dictionary and we have already set the first row
        # for this column to Nan, it raises an error if you try to update the cell which has value Nan
        # to dictionary.
        # only need to do it once for the first update
        if len(self.__data) == 1 and (isinstance(featureVal, dict)):
            self.__data[featureKey] = self.__data[featureKey].astype(object)
        self.__data.set_value(timeOfUpdate, featureKey, featureVal)


if __name__ == "__main__":
    lookbackData = LookbackDataEfficient(3, ['A', 'B'], range(20))
    for i in range(20):
        lookbackData.addData(i, {'A': i, 'B': i})
        print(lookbackData.getData())
