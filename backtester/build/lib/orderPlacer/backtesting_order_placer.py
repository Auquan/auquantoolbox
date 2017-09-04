from base_order_placer import BaseOrderPlacer, PlacedOrder
from backtester.constants import *


class BacktestingOrderPlacer(BaseOrderPlacer):

    def __init__(self):
        self.__orders = []

    def placeOrders(self, time, instrumentExecutions, instrumentsManager):
        for instrumentExecution in instrumentExecutions:
            instrumentId = instrumentExecution.getInstrumentId()
            factor = 1 if instrumentExecution.getExecutionType() == INSTRUMENT_EXECUTION_BUY else -1
            changeInPosition = instrumentExecution.getVolume() * factor
            placedOrder = PlacedOrder(instrumentId=instrumentId,
                                      changeInPosition=changeInPosition)
            self.__orders.append(placedOrder)

    def emitPlacedOrders(self):
        for placedOrder in self.__orders:
            #placedOrder.changeInPosition = UpdateFromExchange
            yield(placedOrder)
        self.__orders = []
