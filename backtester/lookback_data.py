import pandas as pd
from collections import deque


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
