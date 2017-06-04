from datetime import timedelta
from instrumentFeatures.instrument_feature_config import InstrumentFeatureConfig
from dataSource.auquan_data_source import AuquanDataSource
from marketFeatures.market_feature_config import MarketFeatureConfig
from executionSystem.simple_execution_system import SimpleExecutionSystem
from orderPlacer.backtesting_order_placer import BacktestingOrderPlacer


class TradingSystemParameters(object):
    '''
    Returns an instance of class DataParser
    '''
    def getDataParser(self):
        raise NotImplementedError
        return None

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
                          'params': {}}
        vwap = InstrumentFeatureConfig(vwapConfigDict)
        return [vwap]

    def getMarketFeatureConfigs(self):
        return []

    def getPrediction(self, time, currentMarketFeatures, instrumentsManager):
        lookbackMarketFeatures = instrumentsManager.getLookbackMarketFeatures().getData()
        return 0.0

    def getExecutionSystem(self):
        return SimpleExecutionSystem(longLimit=12000, shortLimit=12000)

    def getOrderPlacer(self):
        return BacktestingOrderPlacer()

    def getLookbackSize(self):
        return 500
