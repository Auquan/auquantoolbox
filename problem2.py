from backtester.features.feature import Feature
from backtester.trading_system import TradingSystem
from backtester.sample_scripts.feature_prediction_params import FeaturePredictionTradingParams
from backtester.version import updateCheck
import scipy.stats as st
import numpy as np


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


class Problem2Solver():

    def getTrainingDataSet(self):
        return "trainingData1"

    def getSymbolsToTrade(self):
        return ['ADANIENT']
        # 'ICICIBANK', 'CANBK', 'SBIN', 'YESBANK', 'KOTAKBANK',
        # 'BANKBARODA', 'HDFCBANK', 'AXISBANK', 'INDUSINDBK', 'NIFTYBEES']

    def getCustomFeatures(self):
        return {'my_custom_feature': MyCustomFeature}

    def getFeatureConfigDicts(self):
        ma1Dict = {'featureKey': 'ma_30',
                   'featureId': 'moving_average',
                   'params': {'period': 30,
                              'featureName': 'stockVWAP'}}
        ma2Dict = {'featureKey': 'ma_5',
                   'featureId': 'moving_average',
                   'params': {'period': 5,
                              'featureName': 'stockVWAP'}}
        sdevDict = {'featureKey': 'sdev_30',
                    'featureId': 'moving_sdev',
                    'params': {'period': 30,
                               'featureName': 'stockVWAP'}}
        customFeatureDict = {'featureKey': 'custom_inst_feature',
                             'featureId': 'my_custom_feature',
                             'params': {'param1': 'value1'}}
        return [ma1Dict, ma2Dict, sdevDict, customFeatureDict]

    def getPredictionForVariable(self, time, instrument, instrumentManager):
        lookbackInstrumentFeatures = instrument.getDataDf().iloc[-1]
        z_score = 0
        if lookbackInstrumentFeatures['sdev_30'] != 0 and not np.isnan(lookbackInstrumentFeatures['sdev_30']):
            z_score = (lookbackInstrumentFeatures['ma_30'] - lookbackInstrumentFeatures['ma_5']) / lookbackInstrumentFeatures['sdev_30']
        return st.norm.cdf(z_score)


if __name__ == "__main__":
    if updateCheck():
        print('Your version of the auquan toolbox package is old. Please update by running the following command:')
        print('pip install -U auquan_toolbox')
    problem2Solver = Problem2Solver()
    tsParams = FeaturePredictionTradingParams(problem2Solver)
    tradingSystem = TradingSystem(tsParams)
    tradingSystem.startTrading(onlyAnalyze=True, shouldPlot=True)
