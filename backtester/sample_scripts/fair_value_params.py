from backtester.trading_system_parameters import TradingSystemParameters
from backtester.dataSource.csv_data_source import CsvDataSource
from backtester.executionSystem.basis_execution_system import BasisExecutionSystem
from backtester.executionSystem.QQ_execution_system import QQExecutionSystem
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.constants import *
from backtester.features.feature import Feature
from backtester.logger import *
import numpy as np
from backtester.timeRule.quant_quest_time_rule import QuantQuestTimeRule


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
        return CsvDataSource(cachedFolderName='historicalData/',
                             dataSetId=self.__dataSetId,
                             instrumentIds=instrumentIds,
                             downloadUrl = 'https://raw.githubusercontent.com/Auquan/auquan-historical-data/master/qq2Data',
                             timeKey = '',
                             timeStringFormat = '%Y-%m-%d %H:%M:%S',
                             startDateStr=None,
                             endDateStr=None,
                             liveUpdates=True,
                             pad=True)

    '''
    Returns an instance of class TimeRule, which describes the times at which
    we should update all the features and try to execute any trades based on
    execution logic.
    For eg, for intra day data, you might have a system, where you get data
    from exchange at a very fast rate (ie multiple times every second). However,
    you might want to run your logic of computing features or running your execution
    system, only at some fixed intervals (like once every 5 seconds). This depends on your
    strategy whether its a high, medium, low frequency trading strategy. Also, performance
    is another concern. if your execution system and features computation are taking
    a lot of time, you realistically wont be able to keep upto pace.
    '''
    def getTimeRuleForUpdates(self):
        return QuantQuestTimeRule(cachedFolderName='historicalData/',
                                  dataSetId=self.__dataSetId)

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
                       'enter_price':EnterPrice,
                       'enter_flag':EnterFlag,
                       'spread': SpreadCalculator,
                       'total_fees': TotalFeesCalculator,
                       'predictionString':predictionString})

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
        enterPriceDict = {'featureKey': 'enter_price',
                     'featureId': 'enter_price',
                     'params': {'price': self.getPriceFeatureKey()}}
        enterFlagDict = {'featureKey': 'enter_flag',
                     'featureId': 'enter_flag',
                     'params': {}}
        sdevDictForExec = {'featureKey': 'sdev_5_for_exec',
                           'featureId': 'moving_sdev',
                           'params': {'period': 375,
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
                [fairValuePrediction, sdevDictForExec,
                 spreadConfigDict, feesConfigDict,
                 profitlossConfigDict, capitalConfigDict, enterPriceDict, enterFlagDict]}

    '''
    Returns an array of market feature config dictionaries
        market feature config Dictionary has the following keys:
        featureId: a string representing the type of feature you want to use
        featureKey: a string representing the key you will use to access the value of this feature.this
        params: A dictionary with which contains other optional params if needed by the feature
    '''

    def getMarketFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE

        prediction = {'featureKey': 'predictionString',
                             'featureId': 'predictionString',
                             'params': {'prediction': 'prediction'}}

        pnl = {'featureKey': 'pnlString',
                             'featureId': 'predictionString',
                             'params': {'prediction': 'pnl'}}
        position = {'featureKey': 'positionString',
                             'featureId': 'predictionString',
                             'params': {'prediction': 'position'}}
        # scoreDict = {'featureKey': 'score',
        #              'featureId': 'prob1_score',
        #              'params': {'price': 'FairValue',
        #                         'instrument_score_feature': 'score',
        #                         'benchmark_score_feature': 'sdev_5_for_exec'}}
        return [prediction, pnl, position]#[scoreDict]
    '''
    Returns the type of execution system we want to use. Its an implementation of the class ExecutionSystem
    It converts prediction to intended positions for different instruments.
    '''

    def getExecutionSystem(self):
        return BasisExecutionSystem(basisEnter_threshold=.3, basisExit_threshold=0.1,
                                    basisLongLimit=2500, basisShortLimit=2500,
                                    basisCapitalUsageLimit=0.05, basisLotSize=100,
                                    basisLimitType='L', basis_thresholdParam='sdev_5_for_exec',
                                    price=self.getPriceFeatureKey(), feeDict=0.0001, feesRatio=1.5,
                                    spreadLimit=0.05)

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


class EnterPrice(Feature):
    problem1Solver = None

    @classmethod
    def setProblemSolver(cls, problem1Solver):
        Problem1PredictionFeature.problem1Solver = problem1Solver

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        try:
            priceData = instrumentLookbackData.getFeatureDf(featureParams['price'])
            currentPrice = priceData.iloc[-1]
        except KeyError:
            logError('Price Feature Key does not exist')
        positionData = instrumentLookbackData.getFeatureDf('position')
        previousPosition = 0 if updateNum <= 2 else positionData.iloc[-2]
        currentPosition = 0*currentPrice if updateNum <= 2 else positionData.iloc[-1]
        changeInPosition = 0 if updateNum <= 2 else positionData.iloc[-1] - positionData.iloc[-2]
        avgEnterPrice = 0*currentPrice if updateNum <= 2 else instrumentLookbackData.getFeatureDf(featureKey).iloc[-1]
        avgEnterPrice[currentPosition!=0] = (previousPosition*avgEnterPrice + changeInPosition * currentPrice)/currentPosition
        avgEnterPrice[currentPosition==0] = 0

        return avgEnterPrice


class EnterFlag(Feature):
    problem1Solver = None

    @classmethod
    def setProblemSolver(cls, problem1Solver):
        Problem1PredictionFeature.problem1Solver = problem1Solver

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        positionData = instrumentLookbackData.getFeatureDf('position')
        previousPosition = 0 if updateNum <= 2 else positionData.iloc[-2]
        currentPosition = 0*instrumentLookbackData.getFeatureDf('basis').iloc[-1] if updateNum <= 2 else positionData.iloc[-1]
        changeInPosition = currentPosition - previousPosition
        enterFlag = 0*currentPosition if updateNum <= 2 else instrumentLookbackData.getFeatureDf(featureKey).iloc[-1]
        enterFlag[changeInPosition!=0] = True
        enterFlag[changeInPosition==0] = False

        return enterFlag



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
        return np.minimum(currentSpread / 4.0, 0.20)


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

class predictionString(Feature):
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        predictionDict = instrumentLookbackData.getFeatureDf(featureParams['prediction']).iloc[-1]
        predictionStr = predictionDict.apply(lambda x: '%.3f'%x).values

        return ', '.join(predictionDict.apply(lambda x: '%.3f'%x).values)
