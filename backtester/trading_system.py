import time
from backtester.logger import *
from instruments_manager import InstrumentManager
from datetime import datetime
from state_writer import StateWriter
from plotter import plot


class TradingSystem:
    '''
    tsParams: Instance of TradingSystemParameters
    '''

    def __init__(self, tsParams):
        self.tsParams = tsParams
        self.portfolioValue = 0
        self.capital = 0
        self.instrumentManager = InstrumentManager(self.tsParams)
        self.featuresUpdateTime = None
        self.totalTimeUpdating = 0  # for tracking perf
        self.totalUpdates = 0
        self.executionSystem = None
        self.orderPlacer = None
        self.stateWriter = StateWriter('runLogs', datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))

    def processInstrumentUpdate(self, instrumentUpdate):
        for placedOrder in self.orderPlacer.emitPlacedOrders():
            self.processPlacedOrder(placedOrder)
        self.tryUpdateFeaturesAndExecute(instrumentUpdate.getTimeOfUpdate())
        instrumentIdToUpdate = instrumentUpdate.getInstrumentId()
        instrumentToUpdate = self.instrumentManager.getInstrument(instrumentIdToUpdate)
        # if not present try to create an instrument from this update first.
        if instrumentToUpdate is None:
            instrumentToUpdate = self.instrumentManager.createInstrumentFromUpdate(instrumentUpdate, self.tsParams)
            if instrumentToUpdate is None:
                return
            self.instrumentManager.addInstrument(instrumentToUpdate)
        instrumentToUpdate.update(instrumentUpdate)

    def processPlacedOrder(self, placedOrder):
        instrumentId = placedOrder.getInstrumentId()
        changeInPosition = placedOrder.getChangeInPosition()
        placedInstrument = self.instrumentManager.getInstrument(instrumentId)
        placedInstrument.updatePosition(changeInPosition)

    def tryUpdateFeaturesAndExecute(self, timeOfUpdate):
        # TODO: Fix this to run independently of time of update of instrument and at regular frequency updates
        shouldUpdateFeatures = False
        if self.featuresUpdateTime is None:
            shouldUpdateFeatures = True
        elif timeOfUpdate >= (self.featuresUpdateTime + self.tsParams.getFrequencyOfFeatureUpdates()):
            shouldUpdateFeatures = True
        if shouldUpdateFeatures:
            self.featuresUpdateTime = timeOfUpdate
            self.updateFeatures(timeOfUpdate)
            instrumentsToExecute = self.getInstrumentsToExecute(timeOfUpdate)
            self.orderPlacer.placeOrders(timeOfUpdate, instrumentsToExecute, self.instrumentManager)
            self.portfolioValue = self.instrumentManager.getDataDf()['portfolio_value'][-1]
            self.capital = self.instrumentManager.getDataDf()['capital'][-1]
            self.saveCurrentState()

    def updateFeatures(self, timeOfUpdate):
        # tracking perf
        start = time.time()
        self.instrumentManager.updateFeatures(timeOfUpdate)
        end = time.time()
        diffms = (end - start) * 1000
        self.totalTimeUpdating = self.totalTimeUpdating + diffms
        self.totalUpdates = self.totalUpdates + 1
        logInfo('Update: %d, Time: %.2f, Average: %.2f' % (self.totalUpdates, diffms, self.totalTimeUpdating / self.totalUpdates))

    def getInstrumentsToExecute(self, time):
        return self.executionSystem.getExecutions(time, self.instrumentManager, self.capital)

    def saveCurrentState(self):
        self.stateWriter.writeCurrentState(self.instrumentManager)

    def closePositions(self, timeOfUpdate):
        instrumentsToExecute = self.executionSystem.exitPosition(self.instrumentManager, [], True)
        self.orderPlacer.placeOrders(timeOfUpdate, instrumentsToExecute, self.instrumentManager)
        for placedOrder in self.orderPlacer.emitPlacedOrders():
            self.processPlacedOrder(placedOrder)
        self.updateFeatures(timeOfUpdate)
        self.saveCurrentState()

    def startTrading(self):
        # TODO: Figure out a good way to handle order parsers with live data later on.
        dataParser = self.tsParams.getDataParser()
        self.executionSystem = self.tsParams.getExecutionSystem()
        self.orderPlacer = self.tsParams.getOrderPlacer()
        self.portfolioValue = self.tsParams.getStartingCapital()
        self.capital = self.tsParams.getStartingCapital()
        instrumentUpdates = dataParser.emitInstrumentUpdate()

        for instrumentUpdate in instrumentUpdates:
            # logInfo('TimeOfUpdate: %s TradeSymbol: %s, Volume: %.2f' % (instrumentUpdate.getTimeOfUpdate(), instrumentUpdate.getTradeSymbol(), instrumentUpdate.getBookData()['volume']))
            self.processInstrumentUpdate(instrumentUpdate)
            if self.portfolioValue < 0:
                break

        self.closePositions(instrumentUpdate.getTimeOfUpdate())
        self.stateWriter.closeStateWriter()
        plot(self.stateWriter.getFolderName(), self.stateWriter.getMarketFeaturesFilename(), \
            self.tsParams.getBenchmark(), self.tsParams.getPriceFeatureKey(), [])
