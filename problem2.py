from backtester.features.feature import Feature
from backtester.trading_system import TradingSystem
from backtester.sample_scripts.feature_prediction_params import FeaturePredictionTradingParams
from backtester.version import updateCheck
import numpy as np
import scipy.stats as st


class Problem2Solver():

    def getTrainingDataSet(self):
        return "trainingDataP2_1"

    def getSymbolsToTrade(self):
        return ['JYW']

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
        rankDict = {'featureKey': 'rank',
                    'featureId': 'rank',
                    'params': {'period': 5,
                               'featureName': 'stockVWAP'}}
        bbandlowerDict = {'featureKey': 'bollinger_bands_lower',
                          'featureId': 'bollinger_bands_lower',
                          'params': {'period': 30,
                                     'featureName': 'stockVWAP'}}
        bbandupperDict = {'featureKey': 'bollinger_bands_upper',
                          'featureId': 'bollinger_bands_upper',
                          'params': {'period': 30,
                                     'featureName': 'stockVWAP'}}
        customFeatureDict = {'featureKey': 'custom_inst_feature',
                             'featureId': 'my_custom_feature',
                             'params': {'param1': 'value1'}}
        return [ma1Dict, ma2Dict, sdevDict, rankDict, bbandlowerDict, bbandupperDict, customFeatureDict]

    def getClassifierProbability(self, updateNum, time, instrumentManager):
        # holder for all the instrument features
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()

        # dataframe for a historical instrument feature (exponential_moving_average in this case). The index is the timestamps
        # atmost upto lookback data points. The columns of this dataframe are the stocks/instrumentIds.
        sdevDf = lookbackInstrumentFeatures.getFeatureDf('sdev_30')
        mavg30Df = lookbackInstrumentFeatures.getFeatureDf('ma_30')
        mavg5Df = lookbackInstrumentFeatures.getFeatureDf('ma_5')

        z_score = (mavg30Df.iloc[-1] - mavg5Df.iloc[-1]) / sdevDf.iloc[-1]
        z_score.fillna(0, inplace=True)
        return st.norm.cdf(z_score)


'''
We have already provided a bunch of commonly used features. But if you wish to make your own, define your own class like this.
Write a class that inherits from Feature and implement the one method provided.
'''


class MyCustomFeature(Feature):
    ''''
    Custom Feature to implement for instrument. This function would return the value of the feature you want to implement.
    This function would be called at every update cycle for every instrument. To use this feature you MUST do the following things:
    1. Define it in getCustomFeatures, where you specify the identifier with which you want to access this feature.
    2. To finally use it in a meaningful way, specify this feature in getFeatureConfigDicts with appropirate feature params.
    Example for this is provided below.
    Params:
    updateNum: current iteration of update. For first iteration, it will be 1.
    time: time in datetime format when this update for feature will be run
    featureParams: A dictionary of parameter and parameter values your features computation might depend on.
                   You define the structure for this. just have to make sure these parameters are provided when
                   you wanted to actually use this feature in getFeatureConfigDicts
    featureKey: Name of the key this will feature will be mapped against.
    instrumentManager: A holder for all the instruments
    Returns:
    A Pandas series with stocks/instrumentIds as the index and the corresponding data the value of your custom feature
    for that stock/instrumentId
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        # Custom parameter which can be used as input to computation of this feature
        param1Value = featureParams['param1']

        # A holder for the all the instrument features
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()

        # dataframe for a historical instrument feature (basis in this case). The index is the timestamps
        # atmost upto lookback data points. The columns of this dataframe are the stocks/instrumentIds.
        lookbackInstrumentVWAP = lookbackInstrumentFeatures.getFeatureDf('stockVWAP')

        # The last row of the previous dataframe gives the last calculated value for that feature (stockVWAP in this case)
        # This returns a series with stocks/instrumentIds as the index.
        currentVWAP = lookbackInstrumentVWAP.iloc[-1]

        if param1Value == 'value1':
            return currentVWAP * 0.1
        else:
            return currentVWAP * 0.4


if __name__ == "__main__":
    if updateCheck():
        print('Your version of the auquan toolbox package is old. Please update by running the following command:')
        print('pip install -U auquan_toolbox')
    else:
        problem2Solver = Problem2Solver()
        tsParams = FeaturePredictionTradingParams(problem2Solver)
        tradingSystem = TradingSystem(tsParams)
        # Set onlyAnalyze to True to quickly generate csv files with all the features
        # Set onlyAnalyze to False to run a full backtest
        # Set makeInstrumentCsvs to False to not make instrument specific csvs in runLogs. This improves the performance BY A LOT
        tradingSystem.startTrading(onlyAnalyze=False, shouldPlot=True, makeInstrumentCsvs=True)
