from backtester.features.feature import Feature
from backtester.trading_system import TradingSystem
from problem1_trading_params import FairValueTradingParams


class MyCustomFeature(Feature):
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):
        # Current Book Data For the Instrument. This is the last update to the instrument
        bookData = instrument.getCurrentBookData()
        # Custom parameter which can be used as input to computation of this feature
        param1Value = featureParams['param1']
        # dataframe for historical instrument features,
        lookbackInstrumentFeaturesDf = instrument.getDataDf()
        # columns will be featureKeys for different features
        return 0


class Problem1Solver():

    def getTrainingDataSet(self):
        return "trainingData1"

    def getSymbolsToTrade(self):
        return ['PNB', 'FEDERALBNK']
        # 'ICICIBANK', 'CANBK', 'SBIN', 'YESBANK', 'KOTAKBANK',
        # 'BANKBARODA', 'HDFCBANK', 'AXISBANK', 'INDUSINDBK', 'NIFTYBEES']

    def getCustomFeatures(self):
        return {'my_custom_feature': MyCustomFeature}

    def getFeatureConfigDicts(self):
        ma1Dict = {'featureKey': 'ma_5',
                   'featureId': 'moving_average',
                   'params': {'period': 5,
                              'featureName': 'close'}}
        sdevDict = {'featureKey': 'sdev_5',
                    'featureId': 'moving_sdev',
                    'params': {'period': 5,
                               'featureName': 'close'}}
        customFeatureDict = {'featureKey': 'custom_inst_feature',
                             'featureId': 'my_custom_feature',
                             'params': {'param1': 'value1'}}
        return [ma1Dict, sdevDict, customFeatureDict]

    def getFairValue(self, time, instrument, instrumentManager):
        lookbackInstrumentFeatures = instrument.getDataDf()
        return lookbackInstrumentFeatures.iloc[-1]['ma_5']


if __name__ == "__main__":
    problem1Solver = Problem1Solver()
    tsParams = FairValueTradingParams(problem1Solver)
    tradingSystem = TradingSystem(tsParams)
    tradingSystem.startTrading(onlyAnalyze=False, shouldPlot=True)
