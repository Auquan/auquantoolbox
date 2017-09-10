from backtester.features.feature import Feature
from backtester.trading_system import TradingSystem
from backtester.sample_scripts.fair_value_params import FairValueTradingParams
from backtester.version import updateCheck


class Problem1Solver():

    '''
    Specifies which training data set to use. Right now support
    trainingData1, trainingData2, trainingData3.
    '''

    def getTrainingDataSet(self):
        return "trainingData1"

    '''
    Returns the stocks to trade.
    If empty, uses all the stocks.
    '''

    def getSymbolsToTrade(self):
        return ['AGW']

    '''
    [Optional] This is a way to use any custom features you might have made.
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
    value: Array of instrument feature config dictionaries
        feature config Dictionary has the following keys:
        featureId: a string representing the type of feature you want to use
        featureKey: {optional} a string representing the key you will use to access the value of this feature.
                    If not present, will just use featureId
        params: {optional} A dictionary with which contains other optional params if needed by the feature
    Example:
    ma1Dict = {'featureKey': 'ma_5',
               'featureId': 'moving_average',
               'params': {'period': 5,
                          'featureName': 'stockVWAP'}}
    sdevDict = {'featureKey': 'sdev_5',
                'featureId': 'moving_sdev',
                'params': {'period': 5,
                           'featureName': 'stockVWAP'}}
    customFeatureDict = {'featureKey': 'custom_inst_feature',
                         'featureId': 'my_custom_feature',
                          'params': {'param1': 'value1'}}
    return [ma1Dict, sdevDict, customFeatureDict]
    For  instrument, you will have features keyed by ma_5, sdev_5, custom_inst_feature
    '''

    def getFeatureConfigDicts(self):
        ma1Dict = {'featureKey': 'ma_5',
                   'featureId': 'moving_average',
                   'params': {'period': 5,
                              'featureName': 'basis'}}
        sdevDict = {'featureKey': 'sdev_5',
                    'featureId': 'moving_sdev',
                    'params': {'period': 5,
                               'featureName': 'basis'}}
        customFeatureDict = {'featureKey': 'custom_inst_feature',
                             'featureId': 'my_custom_feature',
                             'params': {'param1': 'value1'}}
        return [ma1Dict, sdevDict, customFeatureDict]

    '''
    Using all the features you have calculated in getFeatureConfigDicts, combine them in a meaningful way
    to compute the fair value as specified in the question for this instrument
    Params:
    time: time at which this is being calculated
    instrument: Instrument for which this is being calculated
    instrumentManager: Holder for all the instruments
    '''

    def getFairValue(self, time, instrument, instrumentManager):
        # dataframe for historical instrument features. The last row of this data frame
        # would contain the features which are being calculated in this update cycle or for this time.
        # The second to last row (if exists) would have the features for the previous
        # time update. Columns will be featureKeys for different features
        lookbackInstrumentFeatures = instrument.getDataDf()
        basisFairValue = lookbackInstrumentFeatures.iloc[-1]['ma_5']

        return basisFairValue


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
    featureParams: A dictionary of parameter and parameter values your features computation might depend on.
                   You define the structure for this. just have to make sure these parameters are provided when
                   you wanted to actually use this feature in getFeatureConfigDicts
    featureKey: Name of the key this will feature will be mapped against.
    currentFeatures: Dictionary with featurekey: featureValue of the instrument features which have been already calculated in this update
                     cycle. The features are computed sequentially in order of how they appear in your config.
    instrument: Instrument for which this feature is being calculated
    instrumentManager: A holder for all the instruments
    '''
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):
        # Current Book Data (dictionary) for the Instrument. This is the last update to the instrument
        bookData = instrument.getCurrentBookData()

        # Custom parameter which can be used as input to computation of this feature
        param1Value = featureParams['param1']

        # dataframe for historical instrument features. The last row of this data frame
        # would contain the features which are being calculated in this update cycle or for this time.
        # The second to last row (if exists) would have the features for the previous
        # time update. Columns will be featureKeys for different features
        lookbackInstrumentFeaturesDf = instrument.getDataDf()

        return 0


if __name__ == "__main__":
    if not updateCheck():
        print 'Your version of the auquan toolbox package is old. Please update by running the following command:'
        print 'pip install -U auquan_toolbox'
    problem1Solver = Problem1Solver()
    tsParams = FairValueTradingParams(problem1Solver)
    tradingSystem = TradingSystem(tsParams)
    # Set onlyAnalyze to True to quickly generate csv files with all the features
    # Set onlyAnalyze to False to run a full backtest
    tradingSystem.startTrading(onlyAnalyze=False, shouldPlot=False)
