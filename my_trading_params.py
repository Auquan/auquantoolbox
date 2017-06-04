from backtester.trading_system_parameters import TradingSystemParameters
from datetime import timedelta
from backtester.instrumentFeatures.instrument_feature_config import InstrumentFeatureConfig
from backtester.dataSource.auquan_data_source import AuquanDataSource
from backtester.marketFeatures.market_feature_config import MarketFeatureConfig
from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.trading_system import TradingSystem


class MyTradingParams(TradingSystemParameters):
    '''
    Returns an instance of class DataParser
    '''
    def getDataParser(self):
        instrumentIdsByType = {'futures': ['banknifty', 'nifty']}
        startDateStr = '2016/07/01'
        endDateStr = '2016/07/04'
        return AuquanDataSource(folderName='historicalData',
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


if __name__ == "__main__":
    tsParams = MyTradingParams()
    tradingSystem = TradingSystem(tsParams)
    tradingSystem.startTrading()
