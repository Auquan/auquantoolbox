from backtester.trading_system_parameters import TradingSystemParameters
from datetime import timedelta
from backtester.dataSource.google_data_source import GoogleStockDataSource
from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.trading_system import TradingSystem
from backtester.constants import *
from my_custom_feature import MyCustomFeature


class MyTradingParams(TradingSystemParameters):
    '''
    Returns an instance of class DataParser. Source of data for instruments
    '''

    def getDataParser(self):
        instrumentIds = ['AAPL']
        startDateStr = '2011/01/10'
        endDateStr = '2017/02/09'
        return GoogleStockDataSource(cachedFolderName='googleData',
                                     instrumentIds=instrumentIds,
                                     startDateStr=startDateStr,
                                     endDateStr=endDateStr)

    def getStartingCapital(self):
        return 100000
    '''
    Returns a timedetla object to indicate frequency of updates to features
    Any updates within this frequncy to instruments do not trigger feature updates.
    Consequently any trading decisions that need to take place happen with the same
    frequency
    '''

    def getFrequencyOfFeatureUpdates(self):
        return timedelta(0, 30)  # minutes, seconds

    '''
    This is a way to use any custom features you might have made.
    Returns a dictionary where
    key: featureId to access this feature (Make sure this doesnt conflict with any of the pre defined feature Ids)
    value: Your custom Class which computes this feature. The class should be an instance of Feature
    Eg. if your custom class is MyCustomFeature, and you want to access this via featureId='my_custom_feature',
    you will import that class, and return this function as {'my_custom_feature': MyCustomFeature}
    '''

    def getCustomFeatures(self):
        return {'my_custom_feature': MyCustomFeature}

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
        positionConfigDict = {'featureKey': 'position',
                              'featureId': 'position',
                              'params': {}}
        feesConfigDict = {'featureKey': 'fees',
                              'featureId': 'fees',
                              'params': {'price':'close',
                                         'feesDict':{-1 : 0.001, 1: 0.001, 0: 0}}}
        profitlossConfigDict = {'featureKey': 'pnl',
                              'featureId': 'pnl',
                              'params': {'price':'close',
                                          'fees' : 'fees'}}
        capitalConfigDict = {'featureKey': 'capital',
                              'featureId': 'capital',
                              'params': {'price':'close', 'fees' : 'fees'}}
        ma1Dict = {'featureKey': 'ma_60',
                   'featureId': 'moving_average',
                   'params': {'period': 10,
                              'featureName': 'close'}}
        ma2Dict = {'featureKey': 'ma_10',
                   'featureId': 'moving_average',
                   'params': {'period': 3,
                              'featureName': 'close'}}
        sdevDict = {'featureKey': 'sdev_60',
                    'featureId': 'moving_sdev',
                    'params': {'period': 10,
                               'featureName': 'close'}}
        return {INSTRUMENT_TYPE_STOCK: [positionConfigDict, feesConfigDict, profitlossConfigDict, capitalConfigDict, \
                                        ma1Dict, ma2Dict, sdevDict]}

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
        profitlossConfigDict = {'featureKey': 'pnl',
                              'featureId': 'pnl',
                              'params': {'instrument_pnl_feature':'pnl'}}
        capitalConfigDict = {'featureKey': 'capital',
                              'featureId': 'capital',
                              'params': {'initial_capital':self.getStartingCapital(),
                                         'capital':'capital',
                                         'pnl' : 'pnl' }}
        portfoliovalueConfigDict = {'featureKey': 'portfolio_value',
                                    'featureId': 'portfolio_value',
                                    'params': {'initial_capital':self.getStartingCapital(),
                                                'pnl':'pnl' }}
        return [profitlossConfigDict, capitalConfigDict, portfoliovalueConfigDict]

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
        instrument = instrumentManager.getInstrument('AAPL')
        if instrument is None:
            return {'AAPL': 0.5}

        lookbackInstrumentFeatures = instrument.getDataDf().iloc[-1]
        # IMPLEMENT THIS
        if lookbackInstrumentFeatures['sdev_60'] != 0:
            z_score = (lookbackInstrumentFeatures['ma_10'] - lookbackInstrumentFeatures['ma_60']) / lookbackInstrumentFeatures['sdev_60']
        else:
            z_score = 0
        if z_score > 1:
            return {'AAPL': 0.2}
        elif z_score < -1:
            return {'AAPL': 0.8}
        elif (z_score > 0.5) or (z_score < -0.5) :
            return {'AAPL': 0.6}
        else:
            return {'AAPL': 0.5}

    '''
    Returns the type of execution system we want to use. Its an implementation of the class ExecutionSystem
    It converts prediction to intended positions for different instruments.
    '''

    def getExecutionSystem(self):
        return SimpleExecutionSystem(enter_threshold=0.7, 
                                     exit_threshold=0.55, 
                                     longLimit=1000, 
                                     shortLimit=1000,
                                     capitalUsageLimit = 0.10*self.getStartingCapital(), 
                                     lotSize=10)

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
        return 10


if __name__ == "__main__":
    tsParams = MyTradingParams()
    tradingSystem = TradingSystem(tsParams)
    tradingSystem.startTrading()
