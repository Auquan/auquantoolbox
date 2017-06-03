from datetime import timedelta
from instrumentFeatures.instrument_feature_config import InstrumentFeatureConfig
from dataSource.nifty_data_source import NiftyDataSource
from marketFeatures.market_feature_config import MarketFeatureConfig
from executionSystem.simple_execution_system import SimpleExecutionSystem
from orderPlacer.backtesting_order_placer import BacktestingOrderPlacer


class TradingSystemParameters:

    '''
    Returns an instance of class DataParser
    '''
    def getDataParser(self):
        return NiftyDataSource('../OptionLogFile1.txt', 'BANKNIFTY1180189800-10', '5/10/2017 15:30:00')

    '''
    Returns a timedetla object to indicate frequency of updates to features
    Any updates within this frequncy to instruments do not trigger feature updates.
    Consequently any trading decisions that need to take place happen with the same
    frequency
    '''
    def getFrequencyOfFeatureUpdates(self):
        return timedelta(0, 5)

    def getFeatureConfigsForInstrumentType(self, instrumentType):
        vwapConfigDict = {'featureKey': 'price',
                          'featureId': 'vwap',
                          'data': {}}
        vwap = InstrumentFeatureConfig(vwapConfigDict)
        return [vwap]

    def getMarketFeatureConfigs(self):
        return []

    def getPrediction(self, time, currentMarketFeatures, instrumentsManager):
        lookbackMarketFeatures = instrumentsManager.getLookbackMarketFeatures().getData()
        return 0.0

    def getExecutionSystem(self):
        if self.__executionSystem is None:
            self.__executionSystem = SimpleExecutionSystem(longLimit=100, shortLimit=100)
        return self.__executionSystem

    def getOrderPlacer(self):
        if self.__orderPlacer is None:
            self.__orderPlacer = BacktestingOrderPlacer()
        return self.__orderPlacer
