import pandas as pd
from collections import deque
import numpy as np

# removing set_value deprecation warning, currently keepin set_value becase the overhead is least
# refer https://stackoverflow.com/questions/28757389/loc-vs-iloc-vs-ix-vs-at-vs-iat/43968774#43968774
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

SIZE_FACTOR = 3
MIN_THRESHOLD = 500
MAX_THRESHOLD = 2000

# TODO: Use indexListGetter better
class LookbackDataEfficient:
    def __init__(self, lookbackSize, columns, indexListGetter, initializer=None):
        self.__isInitialized = False
        self.__lookbackSize = lookbackSize
        self.__columns = columns
        self.__indexList = []
        for t in indexListGetter:
            self.__indexList.append(t)
        self.__startLookbackData = 0
        self.__endLookbackData = 0
        self.__endIndexList = 0
        self.__maxSize = self.computeMaxSize(lookbackSize, len(self.__indexList))

        newEndIndexList = self.__endIndexList + self.__maxSize if (len(self.__indexList) > self.__endIndexList + self.__maxSize) else len(self.__indexList)
        if initializer is not None:
            self.__isInitialized = True
            initializerLookbackSize = min(lookbackSize, len(initializer.getData()))
            if lookbackSize < len(self.__indexList):
                self.__data = pd.DataFrame(columns=self.__columns, index=initializer.getIndexList()[-initializerLookbackSize:]+self.__indexList[self.__endIndexList:newEndIndexList-initializerLookbackSize])
                self.__endIndexList = newEndIndexList - initializerLookbackSize
            else:
                self.__data = pd.DataFrame(columns=self.__columns, index=initializer.getIndexList()[-initializerLookbackSize:]+self.__indexList[self.__endIndexList:newEndIndexList])
                self.__endIndexList = newEndIndexList
                self.__maxSize = initializerLookbackSize + newEndIndexList

            self.__data.iloc[0:initializerLookbackSize] = initializer.getData().iloc[-initializerLookbackSize:]
            self.__endLookbackData = initializerLookbackSize

        else:
            self.__data = pd.DataFrame(columns=self.__columns, index=self.__indexList[self.__endIndexList:newEndIndexList])
            self.__endIndexList = newEndIndexList
        self.__hasSetOnce = False


    def getIndexList(self):
        return self.__indexList

    # def getData(self):
    #     return self.__data

    def computeMaxSize(self, lookbackSize, lenIndexList):
        maxSize = lookbackSize * SIZE_FACTOR
        if (maxSize < MIN_THRESHOLD):
            maxSize = MIN_THRESHOLD
        if (maxSize > MAX_THRESHOLD):
            maxSize = MAX_THRESHOLD
        if (maxSize > 2*lenIndexList):
            return 2*lenIndexList
        if (maxSize < lookbackSize):
            return lookbackSize * SIZE_FACTOR
        return maxSize

    def addData(self, timeOfUpdate, data):
        
        if (self.__endLookbackData == self.__maxSize):
            # make a new dataframe and copy
            newEndIndexList = self.__endIndexList - self.__lookbackSize + self.__maxSize
            if newEndIndexList > len(self.__indexList):
                newEndIndexList = len(self.__indexList)
            if self.__isInitialized:
                newData = pd.DataFrame(columns=self.__columns, index=self.__indexList[np.max([self.__endIndexList - self.__lookbackSize,0]): newEndIndexList])
            else:
                newData = pd.DataFrame(columns=self.__columns, index=self.__indexList[np.max([self.__endIndexList - self.__lookbackSize,0]): newEndIndexList])
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
    def __init__(self, size, columns, initializer=None):
        self.__size = size
        self.__storedData = deque([])
        self.__times = deque([])
        if initializer is None:
            self.__columns = columns
            self.__data = pd.DataFrame(data=list(self.__storedData), columns=self.__columns, index=list(self.__times))
        else:
            self.__data = initializer['market']
            self.__columns = self.__data.columns
            self.__times.extendleft(reversed(self.__data.index))
            # self.__storedData.extendleft(reversed(self.__data.values))


        # self.__data = pd.DataFrame(data=self.__storedData, columns=self.__columns, index=self.__times)
        # self.__storedData = pd.DataFrame(columns=columns)

    def addData(self, timeOfUpdate, data):
        # self.__storedData.append(data)
        self.__times.append(timeOfUpdate)
        if len(self.__storedData) > self.__size:
            # self.__storedData.popleft()
            self.__times.popleft()
        self.__data = self.__data.reindex(pd.to_datetime(self.__times))
        #pd.DataFrame(data=list(self.__storedData), columns=self.__columns, index=pd.to_datetime(self.__times))
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
        if len(self.__data) == 1 :
            if (isinstance(featureVal, dict)):
                self.__data[featureKey] = self.__data[featureKey].astype(object)
            elif (isinstance(featureVal, str)):
                self.__data[featureKey] = self.__data[featureKey].astype(str)
        self.__data.at[timeOfUpdate, featureKey] = featureVal


if __name__ == "__main__":
    lookbackData = LookbackDataEfficient(3, ['A', 'B'], range(20))
    for i in range(20):
        lookbackData.addData(i, {'A': i, 'B': i})
        print(lookbackData.getData())
