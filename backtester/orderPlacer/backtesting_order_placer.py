from backtester.orderPlacer.base_order_placer import BaseOrderPlacer, PlacedOrder
from backtester.constants import *


class BacktestingOrderPlacer(BaseOrderPlacer):

    def __init__(self):
        self.__orders = []

    def mimicPriceOfConfirmation(self, instrument, timeOfExecution, timeOfConfirmation, instrumentsManager):
        tsParams = instrumentsManager.getTsParams()
        priceAtExecution = instrument.getDataDf().iloc[-2][tsParams.getPriceFeatureKey()]
        priceAtConfirmation = instrument.getDataDf().iloc[-1][tsParams.getPriceFeatureKey()]
        if ((timeOfConfirmation - timeOfExecution).seconds > 5):
            return priceAtExecution
        return priceAtConfirmation

    def placeOrders(self, time, instrumentExecutions, instrumentsManager):
        for instrumentExecution in instrumentExecutions:
            instrumentId = instrumentExecution.getInstrumentId()
            instrument = instrumentsManager.getInstrument(instrumentId)
            factor = 1 if instrumentExecution.getExecutionType() == INSTRUMENT_EXECUTION_BUY else -1
            changeInPosition = instrumentExecution.getVolume() * factor
            tradePrice = self.mimicPriceOfConfirmation(instrument, instrumentExecution.getTimeOfExecution(), time, instrumentsManager)
            placedOrder = PlacedOrder(instrumentId=instrumentId,
                                      changeInPosition=changeInPosition,
                                      tradePrice=tradePrice)
            self.__orders.append(placedOrder)

    def emitPlacedOrders(self):
        for placedOrder in self.__orders:
            #placedOrder.changeInPosition = UpdateFromExchange
            yield(placedOrder)
        self.__orders = []
