from backtester.trading_system_parameters import TradingSystemParameters
from datetime import timedelta
from backtester.dataSource.auquan_data_source import AuquanDataSource
from backtester.dataSource.yahoo_data_source import YahooDataSource
from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.trading_system import TradingSystem
from backtester.constants import *
from my_custom_instrument_feature import MyCustomInstrumentFeature
from my_custom_market_feature import MyCustomMarketFeature


class MyTradingParams(TradingSystemParameters):
    '''
    Returns an instance of class DataParser
    '''
    def getDataParser(self):
        '''
        instrumentIdsByType = {'futures': ['banknifty', 'nifty']}
        startDateStr = '2016/07/01'
        endDateStr = '2016/07/04'
        return AuquanDataSource(folderName='historicalData',
                                instrumentIdsByType=instrumentIdsByType,
                                startDateStr=startDateStr,
                                endDateStr=endDateStr)
        '''
        instrumentIdsByType = {'stock': ['YHOO', 'GOOG']}
        startDateStr = '2017/05/10'
        endDateStr = '2017/06/09'
        return YahooDataSource(folderName='historicalData',
                               instrumentIdsByType=instrumentIdsByType,
                               startDateStr=startDateStr,
                               endDateStr=endDateStr)

    '''
    Returns a timedetla object to indicate frequency of updates to features
    Any updates within this frequncy to instruments do not trigger feature updates.
    Consequently any trading decisions that need to take place happen with the same
    frequency
    '''
    def getFrequencyOfFeatureUpdates(self):
        return timedelta(0, 30)

    def getCustomInstrumentFeatures(self):
        return {'my_custom_inst_feature': MyCustomInstrumentFeature}

    def getInstrumentFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE
        positionConfigDict = {'featureKey': 'position',
                              'featureId': 'position',
                              'params': {}}
        vwapConfigDict = {'featureKey': 'price',
                          'featureId': 'vwap',
                          'params': {}}
        customFeatureDict = {'featureKey': 'custom_inst_feature',
                             'featureId': 'my_custom_inst_feature',
                             'params': {'param1': 'value1'}}
        return {INSTRUMENT_TYPE_FUTURE: [positionConfigDict, vwapConfigDict, customFeatureDict]}

    def getCustomMarketFeatures(self):
        return {'my_custom_mrkt_feature': MyCustomMarketFeature}

    def getMarketFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE
        customFeatureDict = {'featureKey': 'custom_mrkt_feature',
                             'featureId': 'my_custom_mrkt_feature',
                             'params': {'param1': 'value1'}}
        return [customFeatureDict]

    def getPrediction(self, time, currentMarketFeatures, instrumentManager):
        lookbackMarketFeatures = instrumentManager.getLookbackMarketFeatures().getData()
        # IMPLEMENT THIS
        return 0.0

    def getExecutionSystem(self):
        return SimpleExecutionSystem(longLimit=12000, shortLimit=12000)

    def getOrderPlacer(self):
        return BacktestingOrderPlacer()

    def getLookbackSize(self):
        return 500


if __name__ == "__main__":
    tsParams = MyTradingParams()
    tradingSystem = TradingSystem(tsParams)
    tradingSystem.startTrading()
