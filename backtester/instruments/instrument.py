from backtester.logger import *
from backtester.features.feature_config import FeatureConfig
from backtester.constants import *
import copy


class Instrument(object):

    def __init__(self, instrumentId, bookDataFeatures, tsParams):
        self.__instrumentId = instrumentId
        self.__currentInstrumentUpdate = None
        self.tsParams = tsParams
        self.__position = 0
        self.__lastTradePrice = 0
        self.__lastTradeLoss = 0

    def getInstrumentType(self):
        raise NotImplementedError
        return INSTRUMENT_TYPE_UNDEFINED

    def getInstrumentId(self):
        return self.__instrumentId

    def getTradeSymbol(self):
        return self.__currentInstrumentUpdate.getTradeSymbol()

    def getDataDf(self):
        raise NotImplementedError

    def update(self, instrumentUpdate):
        if (self.__currentInstrumentUpdate is not None) and (instrumentUpdate is not None):
            if self.__currentInstrumentUpdate.getTimeOfUpdate() > instrumentUpdate.getTimeOfUpdate():
                logWarn('Instrument update time is older than current instrument update time')

        self.__currentInstrumentUpdate = instrumentUpdate

    def updatePositionAtPrice(self, changeInPosition, tradePrice, tradeLoss):
        self.__position = self.__position + changeInPosition
        self.__lastTradePrice = tradePrice
        self.__lastTradeLoss = tradeLoss

    def getCurrentPosition(self):
        return self.__position

    def getLastTradePrice(self):
        return self.__lastTradePrice

    def getLastTradeLoss(self):
        return self.__lastTradeLoss

    def getCurrentBookData(self):
        return self.__currentInstrumentUpdate.getBookData()
