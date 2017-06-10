import time
from backtester.logger import *
from instruments_manager import InstrumentManager
from datetime import datetime


class TradingSystem:
    '''
    tsParams: Instance of TradingSystemParameters
    '''

    def __init__(self, tsParams):
        self.tsParams = tsParams
        self.instrumentManager = InstrumentManager(self.tsParams)
        self.featuresUpdateTime = None
        self.totalTimeUpdating = 0  # for tracking perf
        self.totalUpdates = 0
        self.executionSystem = None
        self.orderPlacer = None
        self.runLogFolder = 'runLog_' + str(datetime.now())

    def processInstrumentUpdate(self, instrumentUpdate):
        # TODO: Not sure if this is the right place for updating placed orders
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
        return self.executionSystem.getExecutions(time, self.instrumentManager)

    def saveCurrentState(self):
        # TODO:
        marketFeaturesFileName = self.runLogFolder + '/marketFeatures'

    def startTrading(self):
        # TODO: Figure out a good way to handle order parsers with live data later on.
        dataParser = self.tsParams.getDataParser()
        self.executionSystem = self.tsParams.getExecutionSystem()
        self.orderPlacer = self.tsParams.getOrderPlacer()
        instrumentUpdates = dataParser.emitInstrumentUpdate()

        for instrumentUpdate in instrumentUpdates:
            logInfo('TimeOfUpdate: %s TradeSymbol: %s, Volume: %.2f' % (instrumentUpdate.getTimeOfUpdate(), instrumentUpdate.getTradeSymbol(), instrumentUpdate.getBookData()['volume']))
            self.processInstrumentUpdate(instrumentUpdate)
