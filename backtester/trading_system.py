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
from backtester.process_result import processResult
from backtester.metrics.metrics import Metrics
from backtester.plotter import generateGraph

from tensorboardX import SummaryWriter

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
        self.stateWriter = None
        self.dataParser = self.tsParams.getDataParser()
        self.executionSystem = self.tsParams.getExecutionSystem()
        self.orderPlacer = self.tsParams.getOrderPlacer()
        self.portfolioValue = self.tsParams.getStartingCapital()
        self.capital = self.tsParams.getStartingCapital()
        self.initializer = None
        self.tensorboard_writer = None

        initializerFile = self.tsParams.getInitializer()
        if initializerFile is not None:
            with open(initializerFile, 'rb') as oldFile:
                self.initializer = cPickle.load(oldFile)
        self.instrumentManager = InstrumentManager(self.tsParams, self.dataParser.getBookDataFeatures(), self.dataParser.getInstrumentIds(),
                                                   self.tsParams.getTimeRuleForUpdates(), self.initializer)

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
            self.log_tensorboard(global_step)
            end = time.time()
            diffms = (end - start) * 1000
            self.timeExecution = self.timeExecution + diffms
            logPerf('Update Execution System: %d, Time: %.2f, Average: %.2f' % (self.totalUpdates, diffms, self.timeExecution / (self.totalUpdates)))
        start = time.time()
        self.saveCurrentState(timeOfUpdate)
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

    def saveCurrentState(self, timeOfUpdate):
        self.stateWriter.writeCurrentState(timeOfUpdate, self.instrumentManager)
    
    def log_tensorboard(self, global_step):
        instrumentIds = self.instrumentManager.getAllInstrumentsByInstrumentId()
        marketFeaturesDf = self.instrumentManager.getDataDf()
        instrumentLookbackData = self.instrumentManager.getLookbackInstrumentFeatures()

        metrics = Metrics(marketFeaturesDf=None)
        startingCapital = self.tsParams.getStartingCapital()
        market_stats = metrics.calculateMarketMetricsRealtime(marketFeaturesDf, startingCapital)
        instrument_stats = metrics.calculateInstrumentFeatureMetricsRealtime(instrumentIds, instrumentLookbackData, startingCapital)

        portfolio_value = marketFeaturesDf['portfolio_value'][-1]  # TODO: find a better way to get this value
        capital = marketFeaturesDf['capital'][-1]  # TODO: find a better way to get this value
        score = marketFeaturesDf['score'][-1]
        self.tensorboard_writer.add_scalars('capital_and_portfolio', {'capital': capital, 'portfolio_value': portfolio_value}, global_step)
        self.tensorboard_writer.add_scalar('score', score, global_step)

        for scalar in market_stats.keys():
            val = market_stats[scalar]
            # self.writer.add_scalars('marketFeature'+scalar, market_stats[scalar], global_step)
            self.tensorboard_writer.add_scalars('market_features', {scalar: val}, global_step)

        for scalar in instrument_stats.keys():
            self.tensorboard_writer.add_scalars(scalar, instrument_stats[scalar], global_step)
            
    def getFinalMetrics(self, dateBounds, shouldPlotFeatures=True, createResultDict=False):
        allInstruments = self.instrumentManager.getAllInstrumentsByInstrumentId()
        resultDict = {}
        resultDict['instrument_names'] = []
        resultDict['instrument_stats'] = []
        for instrumentId in allInstruments:
            metrics = Metrics(marketFeaturesDf=None)
            metrics.calculateInstrumentFeatureMetrics(instrumentId=instrumentId,
                                                      priceFeature=self.tsParams.getPriceFeatureKey(),
                                                      startingCapital=self.tsParams.getStartingCapital(),
                                                      instrumentLookbackData=self.instrumentManager.getLookbackInstrumentFeatures())
            stats = metrics.getMetrics()
            metricString = metrics.getInstrumentMetricsString()
            logInfo('%s: %s' % (instrumentId, metricString), True)
            if createResultDict:
                resultDict['instrument_names'] += [instrumentId]
                resultDict['instrument_stats'] += [{'total_pnl': stats['Total Pnl(%)'], 'score': stats['Score']}]
                if 'Normalized Score' in stats:
                    resultDict['instrument_stats'][-1]['normalized_score'] = stats['Normalized Score']
        metrics = Metrics(marketFeaturesDf=self.instrumentManager.getDataDf())
        metrics.calculateMarketMetrics(None, self.tsParams.getPriceFeatureKey(), self.tsParams.getStartingCapital(), dateBounds)
        stats = metrics.getMetrics()
        metricString = metrics.getMarketMetricsString()
        logInfo(metricString, True)
        if createResultDict:
            resultDict.update(processResult(stats, self.stateWriter.getFolderName(), self.stateWriter.getMarketFeaturesFilename()))
        if shouldPlotFeatures:
            generateGraph(self.instrumentManager.getDataDf(), self.stateWriter.getMarketFeaturesFilename(), metricString, None)
        return resultDict

    def startTrading(self, onlyAnalyze=False, shouldPlot=True, makeInstrumentCsvs=True,createResultDict=False, logFileName=''):
        self.stateWriter = StateWriter('runLogs', datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'), not makeInstrumentCsvs, logFileName)
        self.tensorboard_writer = SummaryWriter(logdir='tb_logs\\'+datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
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
        self.stateWriter.closeStateWriter()
        marketFeaturesDf = self.instrumentManager.getDataDf()
        instrumentLookbackData = self.instrumentManager.getLookbackInstrumentFeatures().getData()
        dataToStore = {'market':marketFeaturesDf, 'instrument':instrumentLookbackData}
        with open('savedData%s'%datetime.strftime(datetime.now(), '%Y%m%d'), 'wb') as myFile:
            cPickle.dump(dataToStore, myFile)
        return self.getFinalMetrics([self.startDate, timeOfUpdate], shouldPlot, createResultDict)
