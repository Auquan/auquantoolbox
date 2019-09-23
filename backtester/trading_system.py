import time
import json
import os
import os.path
try:
    import _pickle as cPickle
except:
    import cPickle
from backtester.logger import *
from backtester.instruments_manager import InstrumentManager
from datetime import datetime
from backtester.state_writer import StateWriter

from backtester.metrics.metrics_logger import MetricsLogger

class TradingSystem:
    '''
    tsParams: Instance of TradingSystemParameters
    '''

    def __init__(self, tsParams):
        self.tsParams = tsParams
        self.portfolioValue = 0
        self.capital = 0
        self.startDate = None
        self.featuresUpdateTime = None
        self.totalUpdates = 0
        self.totalTimeUpdating = 0  # for tracking perf
        self.timeUpdatingFeatures = 0
        self.timeExecution = 0
        self.timeSavingState = 0
        self.dataParser = None
        self.executionSystem = None
        self.orderPlacer = None
        self.dataParser = self.tsParams.getDataParser()
        self.executionSystem = self.tsParams.getExecutionSystem()
        self.orderPlacer = self.tsParams.getOrderPlacer()
        self.portfolioValue = self.tsParams.getStartingCapital()
        self.capital = self.tsParams.getStartingCapital()
        self.initializer = None
        initializerFile = self.tsParams.getInitializer()
        if initializerFile is not None:
            with open(initializerFile, 'rb') as oldFile:
                self.initializer = cPickle.load(oldFile)
        self.instrumentManager = InstrumentManager(self.tsParams, self.dataParser.getBookDataFeatures(), self.dataParser.getInstrumentIds(),
                                                   self.tsParams.getTimeRuleForUpdates(), self.initializer)

        self.metricsLogger = MetricsLogger(self.tsParams.getMetricsToLogRealtime(), self.instrumentManager, self.tsParams.getPriceFeatureKey(), self.tsParams.getStartingCapital())


    def processInstrumentUpdates(self, timeOfUpdate, instrumentUpdates, onlyAnalyze=False, isClose=False):
        # Process instrument updates first
        for instrumentUpdate in instrumentUpdates:
            instrumentIdToUpdate = instrumentUpdate.getInstrumentId()
            instrumentToUpdate = self.instrumentManager.getInstrument(instrumentIdToUpdate)
            # if not present try to create an instrument from this update first.
            if instrumentToUpdate is None:
                instrumentToUpdate = self.instrumentManager.createInstrumentFromUpdate(instrumentUpdate, self.tsParams)
                if instrumentToUpdate is None:
                    return
                self.instrumentManager.addInstrument(instrumentToUpdate)
            instrumentToUpdate.update(instrumentUpdate)
        # update positions of placed orders
        for placedOrder in self.orderPlacer.emitPlacedOrders(timeOfUpdate, self.instrumentManager):
            self.processPlacedOrder(placedOrder)

        # close remaining positions too.
        if (isClose):
            instrumentsToExecute = self.executionSystem.getExecutionsAtClose(timeOfUpdate, self.instrumentManager)
            self.orderPlacer.placeOrders(timeOfUpdate, instrumentsToExecute, self.instrumentManager)
            for placedOrder in self.orderPlacer.emitPlacedOrders(timeOfUpdate, self.instrumentManager):
                self.processPlacedOrder(placedOrder)

    def processPlacedOrder(self, placedOrder):
        instrumentId = placedOrder.getInstrumentId()
        changeInPosition = placedOrder.getChangeInPosition()
        placedInstrument = self.instrumentManager.getInstrument(instrumentId)
        tradePrice = placedOrder.getTradePrice()
        tradeLoss = placedOrder.getTradeLoss()
        placedInstrument.updatePositionAtPrice(changeInPosition, tradePrice, tradeLoss)

    def updateFeaturesAndExecute(self, timeOfUpdate, isClose, onlyAnalyze=False, global_step=0):
        print(timeOfUpdate)
        self.totalUpdates = self.totalUpdates + 1
        self.updateFeatures(timeOfUpdate)
        if not onlyAnalyze:
            start = time.time()
            if not isClose:
                instrumentsToExecute = self.getInstrumentsToExecute(timeOfUpdate)
                self.orderPlacer.placeOrders(timeOfUpdate, instrumentsToExecute, self.instrumentManager)
            self.portfolioValue = self.instrumentManager.getDataDf()['portfolio_value'][-1]  # TODO: find a better way to get this value
            self.capital = self.instrumentManager.getDataDf()['capital'][-1]  # TODO: find a better way to get this value
            # Log in tensorboard
            self.metricsLogger.log_tensorboard(global_step)
            end = time.time()
            diffms = (end - start) * 1000
            self.timeExecution = self.timeExecution + diffms
            logPerf('Update Execution System: %d, Time: %.2f, Average: %.2f' % (self.totalUpdates, diffms, self.timeExecution / (self.totalUpdates)))
        start = time.time()
        self.metricsLogger.saveCurrentState(timeOfUpdate)
        end = time.time()
        diffms = (end - start) * 1000
        self.timeSavingState = self.timeSavingState + diffms
        logPerf('Update Saving state: %d, Time: %.2f, Average: %.2f' % (self.totalUpdates, diffms, self.timeSavingState / (self.totalUpdates)))

    def updateFeatures(self, timeOfUpdate):
        # tracking perf
        start = time.time()
        # if self.totalUpdates > 0:
        # Dont call for the first time
        self.instrumentManager.updateFeatures(timeOfUpdate)
        end = time.time()
        diffms = (end - start) * 1000
        self.timeUpdatingFeatures = self.timeUpdatingFeatures + diffms
        logPerf('Update Features: %d, Time: %.2f, Average: %.2f' % (self.totalUpdates, diffms, self.timeUpdatingFeatures / self.totalUpdates))

    def getInstrumentsToExecute(self, time):
        return self.executionSystem.getExecutions(time, self.instrumentManager, self.capital)


    def startTrading(self, onlyAnalyze=False, shouldPlot=True, makeInstrumentCsvs=True,createResultDict=False, logFileName=''):
        # TODO: Figure out a good way to handle order parsers with live data later on.
        groupedInstrumentUpdates = self.dataParser.emitInstrumentUpdates()
        timeGetter = self.tsParams.getTimeRuleForUpdates().emitTimeToTrade()
        timeOfNextFeatureUpdate = next(timeGetter)
        self.startDate = timeOfNextFeatureUpdate
        timeOfUpdate, instrumentUpdates = next(groupedInstrumentUpdates)
        isClose = False
        global_step = 0
        while True:
            if (timeOfUpdate <= timeOfNextFeatureUpdate):
                self.processInstrumentUpdates(timeOfUpdate, instrumentUpdates, onlyAnalyze)
                try:
                    timeOfUpdate, instrumentUpdates = next(groupedInstrumentUpdates)
                except StopIteration:
                    isClose = True
                    self.updateFeaturesAndExecute(timeOfNextFeatureUpdate, isClose, onlyAnalyze, global_step=global_step)
            else:
                currentTimeUpdate = timeOfNextFeatureUpdate
                try:
                    timeOfNextFeatureUpdate = next(timeGetter)
                except StopIteration:
                    isClose = True
                self.updateFeaturesAndExecute(currentTimeUpdate, isClose, onlyAnalyze, global_step=global_step)

            if not onlyAnalyze and self.portfolioValue < 0:
                logError('Trading will STOP - OUT OF MONEY!!!!')
                break
            if isClose:
                break
            global_step += 1

        self.orderPlacer.cleanup()
        self.dataParser.cleanup()
        marketFeaturesDf = self.instrumentManager.getDataDf()
        instrumentLookbackData = self.instrumentManager.getLookbackInstrumentFeatures().getData()
        dataToStore = {'market':marketFeaturesDf, 'instrument':instrumentLookbackData}
        with open('savedData%s'%datetime.strftime(datetime.now(), '%Y%m%d'), 'wb') as myFile:
            cPickle.dump(dataToStore, myFile)
        self.metricsLogger.tensorboard_writer.close()
        return self.metricsLogger.get_final_metrics([self.startDate, timeOfUpdate])
