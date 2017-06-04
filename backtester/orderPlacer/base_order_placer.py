class PlacedOrder():
    def __init__(self, instrumentId, changeInPosition, changeInCash, fees):
        self.__instrumentId = instrumentId
        self.__changeInPosition = changeInPosition
        self.__changeInCash = changeInCash
        self.__fees = fees

    def getInstrumentId(self):
        return self.__instrumentId

    def getChangeInPosition(self):
        return self.__changeInPosition

    def getChangeInCash(self):
        return self.__changeInCash

    def getFees(self):
        return self.__fees


class BaseOrderPlacer():

    '''
    instrumentExecutions: Array of InstrumentExecution
    '''
    def placeOrders(self, time, instrumentExecutions, instrumentsManager):
        raise NotImplementedError

    def emitPlacedOrders(self):
        raise NotImplementedError
