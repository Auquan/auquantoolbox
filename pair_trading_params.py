from backtester.trading_system_parameters import TradingSystemParameters
from datetime import timedelta
from backtester.dataSource.yahoo_data_source import YahooStockDataSource
from backtester.dataSource.nse_data_source import NSEStockDataSource
from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem
from backtester.executionSystem.pair_execution_system import PairExecutionSystem
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.trading_system import TradingSystem
from backtester.constants import *
from my_custom_feature import MyCustomFeature
from backtester.timeRule.us_time_rule import USTimeRule
from backtester.features.feature import Feature

instrumentIds = ['AAPL', 'MSFT'] # This needs to be in alphabetical order :(


class MyTradingParams(TradingSystemParameters):
    '''
    Returns an instance of class DataParser. Source of data for instruments
    '''

    def getDataParser(self):
        startDateStr = '2010/01/01'
        endDateStr = '2011/06/30'
        return YahooStockDataSource(cachedFolderName='yahooData',
                                     dataSetId='',
                                     instrumentIds=instrumentIds,
                                     startDateStr=startDateStr,
                                     endDateStr=endDateStr)

    '''
    This is a way to use any custom features you might have made.
    Returns a dictionary where
    key: featureId to access this feature (Make sure this doesnt conflict with any of the pre defined feature Ids)
    value: Your custom Class which computes this feature. The class should be an instance of Feature
    Eg. if your custom class is MyCustomFeature, and you want to access this via featureId='my_custom_feature',
    you will import that class, and return this function as {'my_custom_feature': MyCustomFeature}
    '''

    def getBenchmark(self):
        return 'NIFTYBEES'

    def getCustomFeatures(self):
        return {'my_custom_feature': MyCustomFeature,
                'pairvalue_prediction': PairValuePredictionFeature}

    def getTimeRuleForUpdates(self):
        return USTimeRule(startDate = '2010/01/01',
                          endDate = '2017/06/30')

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
        # ADD RELEVANT FEATURES HERE
        ma1Dict = {'featureKey': 'ma_90',
                   'featureId': 'moving_average',
                   'params': {'period': 90,
                              'featureName': 'close'}}
        return {INSTRUMENT_TYPE_STOCK: [ma1Dict]}

    '''
    Returns an array of market feature config dictionaries
        market feature config Dictionary has the following keys:
        featureId: a string representing the type of feature you want to use
        featureKey: a string representing the key you will use to access the value of this feature.this
        params: A dictionary with which contains other optional params if needed by the feature
    '''

    def getMarketFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE

        ratioDict = {'featureKey': 'ratio',
                     'featureId': 'ratio',
                     'params': {'instrumentId1': instrumentIds[0],
                                'instrumentId2': instrumentIds[1],
                                'featureName': 'close'}}
        ma1Dict = {'featureKey': 'ma_90',
                   'featureId': 'moving_average',
                   'params': {'period': 90,
                              'featureName': 'ratio'}}
        ma2Dict = {'featureKey': 'ma_10',
                   'featureId': 'moving_average',
                   'params': {'period': 10,
                              'featureName': 'ratio'}}
        sdevDict = {'featureKey': 'sdev_90',
                    'featureId': 'moving_sdev',
                    'params': {'period': 90,
                               'featureName': 'ratio'}}
        correlDict = {'featureKey': 'correl_90',
                    'featureId': 'cross_instrument_correlation',
                    'params': {'period': 90,
                               'instrumentId1': instrumentIds[0],
                                'instrumentId2': instrumentIds[1],
                                'featureName': 'close'}}
        pairValuePrediction = {'featureKey': 'prediction',
                               'featureId': 'pairvalue_prediction',
                               'params': {}}
        # customFeatureDict = {'featureKey': 'custom_mrkt_feature',
        #                      'featureId': 'my_custom_mrkt_feature',
        #                      'params': {'param1': 'value1'}}
        return [ratioDict, ma1Dict, ma2Dict, sdevDict, correlDict, pairValuePrediction]

    '''
    Returns the type of execution system we want to use. Its an implementation of the class ExecutionSystem
    It converts prediction to intended positions for different instruments.
    '''

    def getExecutionSystem(self):
        return PairExecutionSystem(pair=[instrumentIds[0], instrumentIds[1]],
                                   pairRatio=0.3,
                                   pairEnter_threshold=0.7,
                                   pairExit_threshold=0.55,
                                   pairLongLimit=20000,
                                   pairShortLimit=20000,
                                   pairCapitalUsageLimit = 0.10*self.getStartingCapital(),
                                   pairLotSize=200)
        # return SimpleExecutionSystem(enter_threshold=0.7,
        #                              exit_threshold=0.55,
        #                              longLimit={'ADANIPOWER.BO': 100,'RPOWER.BO': 100 * ratio},
        #                              shortLimit={'ADANIPOWER.BO': -100,'RPOWER.BO': -100 * ratio},
        #                              lotSize={'ADANIPOWER.BO': 10,'RPOWER.BO': 10 * ratio})

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


class PairValuePredictionFeature(Feature):

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackMarketFeatures = instrumentManager.getDataDf()
        # IMPLEMENT THIS
        if currentMarketFeatures['sdev_90'] != 0:
            z_score = (currentMarketFeatures['ma_10'] - currentMarketFeatures['ma_90']) / currentMarketFeatures['sdev_90']
        else:
            z_score = 0
        instrument = instrumentManager.getInstrument(instrumentIds[0])
        #z_score = z_score + instrument.getDataDf()['position']/20000

        if currentMarketFeatures['correl_90'] < 0.5:
            z_score = 0

        if z_score > 1:
            return {instrumentIds[0]: .2,
                    instrumentIds[1]: .8}
        elif z_score < -1:
            return {instrumentIds[0]: .8,
                    instrumentIds[1]: 0.2}
        elif (z_score > 0.5) or (z_score < -0.5) :
            return {instrumentIds[0]: 0.6,
                    instrumentIds[1]: 0.6}
        else:
            return {instrumentIds[0]: 0.5,
                    instrumentIds[1]: 0.5}




if __name__ == "__main__":
    tsParams = MyTradingParams()
    tradingSystem = TradingSystem(tsParams)
    tradingSystem.startTrading(onlyAnalyze=False)
