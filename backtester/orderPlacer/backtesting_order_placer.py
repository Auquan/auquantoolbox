from backtester.orderPlacer.base_order_placer import BaseOrderPlacer, PlacedOrder
from backtester.constants import *


class BacktestingOrderPlacer(BaseOrderPlacer):

    def __init__(self):
        self.__orders = []

    def mimicPriceOfConfirmation(self, instrument, timeOfExecution, timeOfConfirmation, instrumentsManager):
        tsParams = instrumentsManager.getTsParams()
        instrumentLookbackFeatures = instrumentsManager.getLookbackInstrumentFeatures()
        priceAtExecution = instrumentLookbackFeatures.getFeatureDf(tsParams.getPriceFeatureKey())[instrument.getInstrumentId()][-1]

        # priceAtExecution = instrument.getDataDf().iloc[-1][tsParams.getPriceFeatureKey()]
        # TODO: this price feature key should be present in book data
        priceAtConfirmation = instrument.getCurrentBookData()[tsParams.getPriceFeatureKey()]
        if ((timeOfConfirmation - timeOfExecution).seconds > 5):
            return priceAtExecution
        return priceAtConfirmation

    def placeOrders(self, time, instrumentExecutions, instrumentsManager):
        for instrumentExecution in instrumentExecutions:
            instrumentId = instrumentExecution.getInstrumentId()
            factor = 1 if instrumentExecution.getExecutionType() == INSTRUMENT_EXECUTION_BUY else -1
            changeInPosition = instrumentExecution.getVolume() * factor
            placedOrder = PlacedOrder(instrumentId=instrumentId,
                                      changeInPosition=changeInPosition,
                                      timeOfExecution=instrumentExecution.getTimeOfExecution(),
                                      tradeLoss=0.0)
            self.__orders.append(placedOrder)

    def emitPlacedOrders(self, time, instrumentsManager):
        for placedOrder in self.__orders:
            instrumentId = placedOrder.getInstrumentId()
            instrument = instrumentsManager.getInstrument(instrumentId)
            tradePrice = self.mimicPriceOfConfirmation(instrument, placedOrder.getTimeOfExecution(), time, instrumentsManager)
            placedOrder.setTradePrice(tradePrice)
            #placedOrder.changeInPosition = UpdateFromExchange
            yield(placedOrder)
        self.__orders = []
