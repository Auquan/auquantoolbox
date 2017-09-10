class PlacedOrder():
    def __init__(self, instrumentId, changeInPosition, tradePrice):
        self.__instrumentId = instrumentId
        self.__changeInPosition = changeInPosition
        self.__tradePrice = tradePrice

    def getInstrumentId(self):
        return self.__instrumentId

    def getChangeInPosition(self):
        return self.__changeInPosition

    def getTradePrice(self):
        return self.__tradePrice


# TODO: For live orders, we need a way to track what orders we have placed but havent gotten 
# a confirmation for. Also, need something for failure of orders.
class BaseOrderPlacer():

    '''
    instrumentExecutions: Array of InstrumentExecution
    '''
    def placeOrders(self, time, instrumentExecutions, instrumentsManager):
        raise NotImplementedError

    def emitPlacedOrders(self):
        raise NotImplementedError
