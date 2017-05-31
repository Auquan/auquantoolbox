from datetime import timedelta
from instrumentFeatures.instrument_feature_config import InstrumentFeatureConfig
from backtester.dataSource.nifty_data_source import NiftyDataSource


class TradingSystemParameters:

    '''
    Returns an instance of class DataParser
    '''
    def getDataParser(self):
        return NiftyDataSource('OptionLogFile1.txt', 'BANKNIFTY1180189800-10', '5/10/2017 15:30:00')

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
