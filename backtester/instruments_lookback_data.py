from backtester.lookback_data import LookbackDataEfficient


class InstrumentsLookbackData:
    def __init__(self, size, features, instrumentIds, frequencyGetter, initializer=None):
        self.__size = size
        self.__features = features
        self.__instrumentIds = instrumentIds
        self.__data = {}
        for feature in self.__features:
            if initializer is None:
                self.__data[feature] = LookbackDataEfficient(size, instrumentIds, frequencyGetter.emitTimeToTrade())
            else:
                self.__data[feature] = LookbackDataEfficient(size, instrumentIds, frequencyGetter.emitTimeToTrade(), initializer['instrument'][feature])


    def addFeatureValueForAllInstruments(self, timeOfUpdate, featureKey, values):
        self.__data[featureKey].addData(timeOfUpdate, values)

    def getData(self):
        return self.__data

    def getFeatureDf(self, featureKey):
        return self.__data[featureKey].getData()

    def getAllFeatures(self):
        return self.__features
