from backtester.trading_system_parameters import TradingSystemParameters
from datetime import timedelta
from backtester.dataSource.quant_quest_data_source import QuantQuestDataSource
from backtester.executionSystem.basis_execution_system import BasisExecutionSystem
from backtester.executionSystem.QQ_execution_system import QQExecutionSystem
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.constants import *
from backtester.features.feature import Feature
from backtester.logger import *
import numpy as np


class FairValueTradingParams(TradingSystemParameters):

    def __init__(self, problem1Solver):
        self.__problem1Solver = problem1Solver
        Problem1PredictionFeature.setProblemSolver(problem1Solver)
        self.__dataSetId = problem1Solver.getTrainingDataSet()
        super(FairValueTradingParams, self).__init__()

    def getStartingCapital(self):
        instrumentIds = self.__problem1Solver.getSymbolsToTrade()
        if instrumentIds and len(instrumentIds) > 0:
            return len(instrumentIds) * 50000
        return 2000000

    '''
    Returns an instance of class DataParser. Source of data for instruments
    '''

    def getDataParser(self):
        instrumentIds = self.__problem1Solver.getSymbolsToTrade()
        return QuantQuestDataSource(cachedFolderName='historicalData/',
                                    dataSetId=self.__dataSetId,
                                    instrumentIds=instrumentIds)

    '''
    Returns a timedetla object to indicate frequency of updates to features
    Any updates within this frequncy to instruments do not trigger feature updates.
    Consequently any trading decisions that need to take place happen with the same
    frequency
    '''

    def getFrequencyOfFeatureUpdates(self):
        return timedelta(0, 30)  # minutes, seconds

    def getBenchmark(self):
        return None

    '''
    This is a way to use any custom features you might have made.
    Returns a dictionary where
    key: featureId to access this feature (Make sure this doesnt conflict with any of the pre defined feature Ids)
    value: Your custom Class which computes this feature. The class should be an instance of Feature
    Eg. if your custom class is MyCustomFeature, and you want to access this via featureId='my_custom_feature',
    you will import that class, and return this function as {'my_custom_feature': MyCustomFeature}
    '''

    def getCustomFeatures(self):
        return dict(self.__problem1Solver.getCustomFeatures(),
                    **{'problem1_prediction': Problem1PredictionFeature,
                       'spread': SpreadCalculator,
                       'total_fees': TotalFeesCalculator})

    '''
    Returns a dictionary with:
    key: string representing instrument type. Right now INSTRUMENT_TYPE_OPTION, INSTRUMENT_TYPE_STOCK, INSTRUMENT_TYPE_FUTURE
    value: Array of instrument feature config dictionaries
        feature config Dictionary has the following keys:
        featureId: a string representing the type of feature you want to use
        featureKey: {optional} a string representing the key you will use to access the value of this feature.
                    If not present, will just use featureId
        params: {optional} A dictionary with which contains other optional params if needed by the feature
    Example:
    positionConfigDict = {'featureId': 'position'}
    vwapConfigDict = {'featureKey': 'price',
                          'featureId': 'vwap'}
    movingAvg_30Dict = {'featureKey': 'mv_avg_30',
                          'featureId': 'moving_average',
                          'params': {'days': 30}}
    movingAvg_90Dict = {'featureKey': 'mv_avg_90',
                          'featureId': 'moving_average',
                          'params': {'days': 90}}
    return {INSTRUMENT_TYPE_FUTURE: [positionConfigDict, vwapConfigDict],
            INSTRUMENT_TYPE_STOCK: [positionConfigDict, movingAvg_30Dict, movingAvg_90Dict]}

    For each future instrument, you will have features keyed by position and price.
    For each stock instrument, you will have features keyed by position, mv_avg_30, mv_avg_90
    '''

    def getInstrumentFeatureConfigDicts(self):
        stockFeatureConfigs = self.__problem1Solver.getFeatureConfigDicts()
        fairValuePrediction = {'featureKey': 'prediction',
                               'featureId': 'problem1_prediction',
                               'params': {}}
        scoreDict = {'featureKey': 'score',
                     'featureId': 'prob1_score',
                     'params': {'predictionKey': 'prediction',
                                'price': 'FairValue'}}
        sdevDictForExec = {'featureKey': 'sdev_5_for_exec',
                           'featureId': 'moving_sdev',
                           'params': {'period': 5,
                                      'featureName': 'basis'}}
        spreadConfigDict = {'featureKey': 'spread',
                            'featureId': 'spread',
                            'params': {}}
        feesConfigDict = {'featureKey': 'fees',
                          'featureId': 'total_fees',
                          'params': {'price': 'stockVWAP',
                                     'feesDict': {1: 0.0001, -1: 0.0001, 0: 0},
                                     'spread': 'spread'}}
        profitlossConfigDict = {'featureKey': 'pnl',
                                'featureId': 'pnl',
                                'params': {'price': self.getPriceFeatureKey(),
                                           'fees': 'fees'}}
        capitalConfigDict = {'featureKey': 'capital',
                             'featureId': 'capital',
                             'params': {'price': 'stockVWAP',
                                        'fees': 'fees',
                                        'capitalReqPercent': 0.15}}
        return {INSTRUMENT_TYPE_STOCK: stockFeatureConfigs +
                [fairValuePrediction, sdevDictForExec, scoreDict,
                 spreadConfigDict, feesConfigDict,
                 profitlossConfigDict, capitalConfigDict]}

    '''
    Returns an array of market feature config dictionaries
        market feature config Dictionary has the following keys:
        featureId: a string representing the type of feature you want to use
        featureKey: a string representing the key you will use to access the value of this feature.this
        params: A dictionary with which contains other optional params if needed by the feature
    '''

    def getMarketFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE

        # customFeatureDict = {'featureKey': 'custom_mrkt_feature',
        #                      'featureId': 'my_custom_mrkt_feature',
        #                      'params': {'param1': 'value1'}}
        scoreDict = {'featureKey': 'score',
                     'featureId': 'prob1_score',
                     'params': {'price': 'FairValue',
                                'instrument_score_feature': 'score',
                                'benchmark_score_feature': 'benchmark_score'}}
        return [scoreDict]

    '''
    Returns the type of execution system we want to use. Its an implementation of the class ExecutionSystem
    It converts prediction to intended positions for different instruments.
    '''

    def getExecutionSystem(self):
        return BasisExecutionSystem(basisEnter_threshold=0.25, basisExit_threshold=0.01,
                                    basisLongLimit=5000, basisShortLimit=5000,
                                    basisCapitalUsageLimit=0.05, basisLotSize=100,
                                    basisLimitType='L', basis_thresholdParam='sdev_5_for_exec',
                                    price=self.getPriceFeatureKey())

    '''
    Returns the type of order placer we want to use. its an implementation of the class OrderPlacer.
    It helps place an order, and also read confirmations of orders being placed.
    For Backtesting, you can just use the BacktestingOrderPlacer, which places the order which you want, and automatically confirms it too.
    '''

    def getOrderPlacer(self):
        return BacktestingOrderPlacer()

    '''
    Returns the amount of lookback data you want for your calculations. The historical market features and instrument features are only
    stored upto this amount.
    This number is the number of times we have updated our features.
    '''

    def getLookbackSize(self):
        return 120

    def getPriceFeatureKey(self):
        return 'basis'

    def getDataSetId(self):
        return self.__dataSetId

    def setDataSetId(self, dataSetId):
        self.__dataSetId = dataSetId


class Problem1PredictionFeature(Feature):
    problem1Solver = None

    @classmethod
    def setProblemSolver(cls, problem1Solver):
        Problem1PredictionFeature.problem1Solver = problem1Solver

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        return Problem1PredictionFeature.problem1Solver.getFairValue(updateNum, time, instrumentManager)


class SpreadCalculator(Feature):
    problem1Solver = None

    @classmethod
    def setProblemSolver(cls, problem1Solver):
        Problem1PredictionFeature.problem1Solver = problem1Solver

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        try:
            # TODO: Change the hard key references
            currentStockBidPrice = instrumentLookbackData.getFeatureDf('stockTopBidPrice').iloc[-1]
            currentStockAskPrice = instrumentLookbackData.getFeatureDf('stockTopAskPrice').iloc[-1]
            currentFutureBidPrice = instrumentLookbackData.getFeatureDf('futureTopBidPrice').iloc[-1]
            currentFutureAskPrice = instrumentLookbackData.getFeatureDf('futureTopAskPrice').iloc[-1]
        except KeyError:
            logError('Bid and Ask Price Feature Key does not exist')

        currentSpread = currentStockAskPrice - currentStockBidPrice + currentFutureAskPrice - currentFutureBidPrice
        return np.minimum(currentSpread / 8.0, 0.025)


class TotalFeesCalculator(Feature):
    problem1Solver = None

    @classmethod
    def setProblemSolver(cls, problem1Solver):
        Problem1PredictionFeature.problem1Solver = problem1Solver

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()

        positionData = instrumentLookbackData.getFeatureDf('position')
        feesDict = featureParams['feesDict']
        currentPosition = positionData.iloc[-1]
        previousPosition = 0 if updateNum < 2 else positionData.iloc[-2]
        changeInPosition = currentPosition - previousPosition
        fees = np.abs(changeInPosition) * [feesDict[np.sign(x)] for x in changeInPosition]
        if 'price' in featureParams:
            try:
                priceData = instrumentLookbackData.getFeatureDf(featureParams['price'])
                currentPrice = priceData.iloc[-1]
            except KeyError:
                logError('Price Feature Key does not exist')

            fees = fees * currentPrice

        total = 2 * fees \
                + (np.abs(changeInPosition) * instrumentLookbackData.getFeatureDf(featureParams['spread']).iloc[-1])
        return total
