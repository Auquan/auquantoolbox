import time
from backtester.logger import *
from backtester.instruments_manager import InstrumentManager
from datetime import datetime
from backtester.state_writer import StateWriter
from backtester.process_result import processResult
from backtester.metrics.metrics import Metrics


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
        self.totalTimeUpdating = 0  # for tracking perf
        self.timeUpdatingFeatures = 0
        self.timeProcessingInstruments = 0
        self.totalUpdates = 0
        self.timeExecution = 0
        self.timeSavingState = 0
        self.dataParser = None
        self.executionSystem = None
        self.orderPlacer = None
        self.stateWriter = StateWriter('runLogs', datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
        self.dataParser = self.tsParams.getDataParser()
        self.executionSystem = self.tsParams.getExecutionSystem()
        self.orderPlacer = self.tsParams.getOrderPlacer()
        self.portfolioValue = self.tsParams.getStartingCapital()
        self.capital = self.tsParams.getStartingCapital()
        self.instrumentManager = InstrumentManager(self.tsParams, self.dataParser.getBookDataFeatures(), self.dataParser.getInstrumentIds(),
                                                   self.dataParser.getBookDataByFeature(), self.dataParser.getAllTimes())

    def processInstrumentUpdates(self, timeOfUpdate, instrumentUpdates, onlyAnalyze=False, isClose=False):
        start = time.time()
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
        end = time.time()
        diffms = (end - start) * 1000
        self.timeProcessingInstruments = self.timeProcessingInstruments + diffms
        logPerf('Update Processing Instruments: %d, Time: %.2f, Average: %.2f' % (self.totalUpdates + 1, diffms, self.timeProcessingInstruments / (self.totalUpdates + 1)))
        # update positions of placed orders
        for placedOrder in self.orderPlacer.emitPlacedOrders(timeOfUpdate, self.instrumentManager):
            self.processPlacedOrder(placedOrder)

        # close remaining positions too.
        if (isClose):
            instrumentsToExecute = self.executionSystem.getExecutionsAtClose(timeOfUpdate, self.instrumentManager)
            self.orderPlacer.placeOrders(timeOfUpdate, instrumentsToExecute, self.instrumentManager)
            for placedOrder in self.orderPlacer.emitPlacedOrders(timeOfUpdate, self.instrumentManager):
                self.processPlacedOrder(placedOrder)

        # Then we try to calculate features.
        self.tryUpdateFeaturesAndExecute(timeOfUpdate, isClose, onlyAnalyze)
        end = time.time()
        diffms = (end - start) * 1000
        self.totalTimeUpdating = self.totalTimeUpdating + diffms
        logPerf('Update Total Time: %d, Time: %.2f, Average: %.2f' % (self.totalUpdates, diffms, self.totalTimeUpdating / self.totalUpdates))

    def processPlacedOrder(self, placedOrder):
        instrumentId = placedOrder.getInstrumentId()
        changeInPosition = placedOrder.getChangeInPosition()
        placedInstrument = self.instrumentManager.getInstrument(instrumentId)
        tradePrice = placedOrder.getTradePrice()
        placedInstrument.updatePositionAtPrice(changeInPosition, tradePrice)

    def tryUpdateFeaturesAndExecute(self, timeOfUpdate, isClose, onlyAnalyze=False):
        # TODO: Fix this to run independently of time of update of instrument and at regular frequency updates
        shouldUpdateFeatures = False
        if self.featuresUpdateTime is None:
            shouldUpdateFeatures = True
        elif timeOfUpdate >= (self.featuresUpdateTime + self.tsParams.getFrequencyOfFeatureUpdates()):
            shouldUpdateFeatures = True
        if shouldUpdateFeatures:
            self.featuresUpdateTime = timeOfUpdate
            self.updateFeatures(timeOfUpdate)
            if not onlyAnalyze:
                start = time.time()
                if not isClose:
                    instrumentsToExecute = self.getInstrumentsToExecute(timeOfUpdate)
                    self.orderPlacer.placeOrders(timeOfUpdate, instrumentsToExecute, self.instrumentManager)
                self.portfolioValue = self.instrumentManager.getDataDf()['portfolio_value'][-1]  # TODO: find a better way to get this value
                self.capital = self.instrumentManager.getDataDf()['capital'][-1]  # TODO: find a better way to get this value
                end = time.time()
                diffms = (end - start) * 1000
                self.timeExecution = self.timeExecution + diffms
                logPerf('Update Execution System: %d, Time: %.2f, Average: %.2f' % (self.totalUpdates, diffms, self.timeExecution / (self.totalUpdates)))
            start = time.time()
            # self.saveCurrentState()
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
        self.totalUpdates = self.totalUpdates + 1
        logPerf('Update Features: %d, Time: %.2f, Average: %.2f' % (self.totalUpdates, diffms, self.timeUpdatingFeatures / self.totalUpdates))

    def getInstrumentsToExecute(self, time):
        return self.executionSystem.getExecutions(time, self.instrumentManager, self.capital)

    def saveCurrentState(self):
        self.stateWriter.writeCurrentState(self.instrumentManager)

    def getFinalMetrics(self, dateBounds, shouldPlotFeatures=True):
        allInstruments = self.instrumentManager.getAllInstrumentsByInstrumentId()
        resultDict = {}
        for instrumentId in allInstruments:
            instrument = allInstruments[instrumentId]
            lookbackData = instrument.getDataDf()
            metrics = Metrics(marketFeaturesDf=lookbackData)
            metrics.calculateMetrics(self.tsParams.getPriceFeatureKey(), self.tsParams.getStartingCapital())
            stats = metrics.getMetrics()
            metricString = metrics.getMetricsString()
            logInfo(metricString, True)
            resultDict.update(processResult(self.stateWriter.getFolderName(), None, None,
                                            stats, metricString, self.tsParams.getStartingCapital(), [self.stateWriter.getMarketFeaturesFilename()], shouldPlotFeatures))
        metrics = Metrics(marketFeaturesDf=self.instrumentManager.getDataDf())
        metrics.calculateMarketMetrics(None, self.tsParams.getPriceFeatureKey(), self.tsParams.getStartingCapital(), dateBounds)
        stats = metrics.getMetrics()
        metricString = metrics.getMarketMetricsString()
        logInfo(metricString, True)
        # Hack to always plot market
        shouldPlotMarket = True
        resultDict.update(processResult(self.stateWriter.getFolderName(), self.stateWriter.getMarketFeaturesFilename(),
                                        self.tsParams.getBenchmark(), stats, metricString, self.tsParams.getStartingCapital(), [], shouldPlotMarket))
        return resultDict

    def startTrading(self, onlyAnalyze=False, shouldPlot=True):
        # TODO: Figure out a good way to handle order parsers with live data later on.
        groupedInstrumentUpdates = self.dataParser.emitInstrumentUpdates()
        self.closingTime = self.dataParser.getClosingTime()

        for timeOfUpdate, instrumentUpdates in groupedInstrumentUpdates:
            # logInfo('TimeOfUpdate: %s TradeSymbol: %s' % (instrumentUpdate.getTimeOfUpdate(), instrumentUpdate.getTradeSymbol()))
            print(timeOfUpdate)
            if self.startDate is None:
                self.startDate = timeOfUpdate
            self.processInstrumentUpdates(timeOfUpdate, instrumentUpdates, onlyAnalyze, (closingTime == timeOfUpdate))
            if not onlyAnalyze and self.portfolioValue < 0:
                logError('Trading will STOP - OUT OF MONEY!!!!')
                break

        self.stateWriter.closeStateWriter()

        return self.getFinalMetrics([self.startDate, timeOfUpdate], shouldPlot)
