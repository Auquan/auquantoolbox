from backtester.logger import *


class PlacedOrder():
    def __init__(self, instrumentId, changeInPosition, timeOfExecution, tradeLoss):
        self.__instrumentId = instrumentId
        self.__changeInPosition = changeInPosition
        self.__tradePrice = None
        self.__timeOfExecution = timeOfExecution
        self.__tradeLoss = tradeLoss

    def getInstrumentId(self):
        return self.__instrumentId

    def getChangeInPosition(self):
        return self.__changeInPosition

    def getTradePrice(self):
        if self.__tradePrice is None:
            logError('tradePrice is not set yet')
            return 0
        return self.__tradePrice

    def setTradePrice(self, tradePrice):
        self.__tradePrice = tradePrice

    def getTimeOfExecution(self):
        return self.__timeOfExecution

    def getTradeLoss(self):
        return self.__tradeLoss


# TODO: For live orders, we need a way to track what orders we have placed but havent gotten
# a confirmation for. Also, need something for failure of orders.
class BaseOrderPlacer():

    '''
    instrumentExecutions: Array of InstrumentExecution
    '''
    def placeOrders(self, time, instrumentExecutions, instrumentsManager):
        raise NotImplementedError

    def emitPlacedOrders(self, time, instrumentsManager):
        raise NotImplementedError

    '''
    Called at end of trading to cleanup stuff
    '''
    def cleanup(self):
        return
