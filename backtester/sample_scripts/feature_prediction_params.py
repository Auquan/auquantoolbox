from backtester.trading_system_parameters import TradingSystemParameters
from datetime import timedelta
from backtester.dataSource.csv_data_source import CsvDataSource
from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.trading_system import TradingSystem
from backtester.constants import *
from backtester.features.feature import Feature
from backtester.timeRule.quant_quest_time_rule import QuantQuestTimeRule


class FeaturePredictionTradingParams(TradingSystemParameters):

    def __init__(self, problem2Solver):
        self.__problem2Solver = problem2Solver
        Problem2PredictionFeature.setProblemSolver(problem2Solver)
        self.__dataSetId = problem2Solver.getTrainingDataSet()
        super(FeaturePredictionTradingParams, self).__init__()

    def getStartingCapital(self):
        instrumentIds = self.__problem2Solver.getSymbolsToTrade()
        if instrumentIds and len(instrumentIds) > 0:
            return len(instrumentIds) * 1000000
        return 50000000
    '''
    Returns an instance of class DataParser. Source of data for instruments
    '''

    def getDataParser(self):
        instrumentIds = self.__problem2Solver.getSymbolsToTrade()
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
        return dict(self.__problem2Solver.getCustomFeatures(),
                    **{'problem2_prediction': Problem2PredictionFeature,
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
    movingAvg_30Dict = {'featureKey': 'mv_avg_30',
                          'featureId': 'moving_average',
                          'params': {'days': 30}}
    return {INSTRUMENT_TYPE_FUTURE: [positionConfigDict, vwapConfigDict],
            INSTRUMENT_TYPE_STOCK: [positionConfigDict, movingAvg_30Dict, movingAvg_30Dict]}

    For each future instrument, you will have features keyed by position and price.
    For each stock instrument, you will have features keyed by position, mv_avg_30, mv_avg_30
    '''

    def getInstrumentFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE
        stockFeatureConfigs = self.__problem2Solver.getFeatureConfigDicts()
        classifierPrediction = {'featureKey': 'prediction',
                                'featureId': 'problem2_prediction',
                                'params': {}}
        scoreDict = {'featureKey': 'score',
                     'featureId': 'score_ll',
                     'params': {'predictionKey': 'prediction',
                                'target': 'Y'}}
        spreadConfigDict = {'featureKey': 'spread',
                            'featureId': 'spread',
                            'params': {}}
        feesConfigDict = {'featureKey': 'fees',
                          'featureId': 'total_fees',
                          'params': {'price': self.getPriceFeatureKey(),
                                     'feesDict': {1: 0.0001, -1: 0.0001, 0: 0},
                                     'spread': 'spread'}}
        profitlossConfigDict = {'featureKey': 'pnl',
                                'featureId': 'pnl',
                                'params': {'price': self.getPriceFeatureKey(),
                                           'fees': 'fees'}}
        capitalConfigDict = {'featureKey': 'capital',
                             'featureId': 'capital',
                             'params': {'price': self.getPriceFeatureKey(),
                                        'fees': 'fees',
                                        'capitalReqPercent': 0.15}}
        return {INSTRUMENT_TYPE_STOCK: stockFeatureConfigs + [classifierPrediction, scoreDict,
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
                     'featureId': 'score_ll',
                     'params': {'featureName': self.getPriceFeatureKey(),
                                'instrument_score_feature': 'score'}}
        return [scoreDict]

    '''
    Returns the type of execution system we want to use. Its an implementation of the class ExecutionSystem
    It converts prediction to intended positions for different instruments.
    '''

    def getExecutionSystem(self):
        return SimpleExecutionSystem(enter_threshold=0.8, exit_threshold=0.6,
                                     longLimit=10000, shortLimit=10000, capitalUsageLimit=0.05,
                                     lotSize=500, limitType='L', price=self.getPriceFeatureKey())

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
        return 90

    def getPriceFeatureKey(self):
        return 'stockVWAP'

    def getDataSetId(self):
        return self.__dataSetId

    def setDataSetId(self, dataSetId):
        self.__dataSetId = dataSetId


class Problem2PredictionFeature(Feature):
    problem2Solver = None

    @classmethod
    def setProblemSolver(cls, problem2Solver):
        Problem2PredictionFeature.problem2Solver = problem2Solver

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        return Problem2PredictionFeature.problem2Solver.getClassifierProbability(updateNum, time, instrumentManager)

class SpreadCalculator(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        try:
            # TODO: Change the hard key references
            currentStockBidPrice = instrumentLookbackData.getFeatureDf('stockTopBidPrice').iloc[-1]
            currentStockAskPrice = instrumentLookbackData.getFeatureDf('stockTopAskPrice').iloc[-1]
        except KeyError:
            logError('Bid and Ask Price Feature Key does not exist')

        currentSpread = currentStockAskPrice - currentStockBidPrice
        return np.minimum(currentSpread / 2.0, 0.1)

class TotalFeesCalculator(Feature):

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
