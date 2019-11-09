from datetime import timedelta
from backtester.features.feature_config import FeatureConfig
from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.constants import *


class TradingSystemParameters(object):
    def __init__(self):
        FeatureConfig.setupCustomFeatures(self.getCustomFeatures())
        self.__instrumentFeatureConfigs = {}
        instrumentFeatureConfigDicts = self.getInstrumentFeatureConfigDicts()
        for instrumentType in instrumentFeatureConfigDicts:
            self.__instrumentFeatureConfigs[instrumentType] = list(map(lambda x: FeatureConfig(x), instrumentFeatureConfigDicts[instrumentType]))
        self.__marketFeatureConfigs = list(map(lambda x: FeatureConfig(x), self.getMarketFeatureConfigDicts()))

    #####################################################################
    ###      START OF OVERRIDING METHODS
    #####################################################################

    '''
    Returns an instance of class DataParser. Source of data for instruments
    '''
    def getDataParser(self):
        raise NotImplementedError
        return None

    '''
    Return starting capital
    '''
    def getStartingCapital(self):
        return 10000000

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
        return NotImplementedError
    '''
     Returns the symbol to use as benchmark for market returns
    '''
    def getBenchmark(self):
        raise NotImplementedError
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
        return {}

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
        return {}

    '''
    Returns an array of market feature config dictionaries
        market feature config Dictionary has the following keys:
        featureId: a string representing the type of feature you want to use
        featureKey: a string representing the key you will use to access the value of this feature.this
        params: A dictionary with which contains other optional params if needed by the feature
    '''
    def getMarketFeatureConfigDicts(self):
        return []

    '''
    Returns the feature key of instrument to use for price calculations ie pnl, fees etc.
    type: Type of Instrument
    For example, for stocks close should be fine.
    Defaults to close for all insturment types
    '''
    def getPriceFeatureKey(self):
        return 'close'

    '''
    A function that returns your predicted value based on your heuristics.
    If you are just trading one asset like a stock, it could be the predicted value of the stock.
    If you are doing pair trading, the prediction could be the difference in the prices of the stocks.
    Arguments:
    time - When this prediction is being calculated
    currentMarketFeatures - Dictionary of market features which have been calculated at this update cycle.
    instrumentManager - Holder for all instruments and everything else if you need.
    '''
    def getPrediction(self, time, currentMarketFeatures, instrumentManager):
        return 0.0

    '''
    Returns the type of execution system we want to use. Its an implementation of the class ExecutionSystem
    Basically, it converts prediction to intended positions for different instruments.
    '''
    def getExecutionSystem(self):
        return SimpleExecutionSystem(longLimit=12000, shortLimit=12000)

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
        return 500

    def getMetricsToLogRealtime(self):
        '''
        Function returning the names of metrics to log at every step and visualize them in tensorflow. For visualization:
        1. Open a new terminal window and cd to the directory where trading params file is
        2. Enter the command tensorboard --logdir=tbLogs and go to localhost

        Returns:
            features_dict (dict): name of market and instrument features that'll be logged, by default everything is logged
        '''
        return {
            'market': None,
            'instruments': None
        }

    #####################################################################
    ###      END OF OVERRIDING METHODS
    #####################################################################

    def getFeatureConfigsForInstrumentType(self, instrumentType):
        if instrumentType in self.__instrumentFeatureConfigs:
            return self.__instrumentFeatureConfigs[instrumentType]
        else:
            return []

    def getMarketFeatureConfigs(self):
        return self.__marketFeatureConfigs

    def getInitializer(self):
        return None

    