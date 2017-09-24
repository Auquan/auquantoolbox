from backtester.features.feature import Feature
from backtester.trading_system import TradingSystem
from backtester.sample_scripts.fair_value_params import FairValueTradingParams
from backtester.version import updateCheck


class Problem1Solver():

    '''
    Specifies which training data set to use. Right now support
    sampleData, trainingData1, trainingData2, trainingData3.
    '''

    def getTrainingDataSet(self):
        return "trainingData1"

    '''
    Returns the stocks to trade.
    If empty, uses all the stocks.
    '''

    def getSymbolsToTrade(self):
        return ['AGW', 'CHV']

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
        ma2Dict = {'featureKey': 'ma_5',
                   'featureId': 'moving_average',
                   'params': {'period': 5,
                              'featureName': 'stockTopAskPrice'}}
        ma1Dict = {'featureKey': 'ma_5',
                   'featureId': 'moving_average',
                   'params': {'period': 5,
                              'featureName': 'basis'}}
        expma = {'featureKey': 'exponential_moving_average',
                 'featureId': 'exponential_moving_average',
                 'params': {'period': 20,
                              'featureName': 'basis'}}
        sdevDict = {'featureKey': 'sdev_5',
                    'featureId': 'moving_sdev',
                    'params': {'period': 5,
                               'featureName': 'basis'}}
        customFeatureDict = {'featureKey': 'custom_inst_feature',
                             'featureId': 'my_custom_feature',
                             'params': {'param1': 'value1'}}
        return [ma1Dict, sdevDict, expma]

    '''
    Using all the features you have calculated in getFeatureConfigDicts, combine them in a meaningful way
    to compute the fair value as specified in the question
    Params:
    time: time at which this is being calculated
    instrumentManager: Holder for all the instruments
    Returns:
    A Pandas DataSeries with instrumentIds as the index, and the corresponding data your estimation of the fair value
    for that stock/instrumentId
    '''

    def getFairValue(self, updateNum, time, instrumentManager):
        # holder for all the instrument features
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()

        # dataframe for a historical instrument feature (ma_5 in this case). The index is the timestamps
        # atmost upto lookback data points. The columns of this dataframe are the stock symbols/instrumentIds.
        ma5Data = lookbackInstrumentFeatures.getFeatureDf('ma_5')

        # Returns a series with index as all the instrumentIds. This returns the value of the feature at the last
        # time update.
        ma5 = ma5Data.iloc[-1]

        return ma5


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
        lookbackInstrumentBasis = lookbackInstrumentFeatures.getFeatureDf('basis')

        # The last row of the previous dataframe gives the last calculated value for that feature (basis in this case)
        # This returns a series with stocks/instrumentIds as the index.
        currentBasisValue = lookbackInstrumentBasis.iloc[-1]

        if param1Value == 'value1':
            return currentBasisValue * 0.1
        else:
            return currentBasisValue * 0.5


if __name__ == "__main__":
    if updateCheck():
        print('Your version of the auquan toolbox package is old. Please update by running the following command:')
        print('pip install -U auquan_toolbox')
    else:
        problem1Solver = Problem1Solver()
        tsParams = FairValueTradingParams(problem1Solver)
        tradingSystem = TradingSystem(tsParams)
        # Set onlyAnalyze to True to quickly generate csv files with all the features
        # Set onlyAnalyze to False to run a full backtest
        # Set makeInstrumentCsvs to False to not make instrument specific csvs in runLogs. This improves the performance BY A LOT
        tradingSystem.startTrading(onlyAnalyze=False, shouldPlot=True, makeInstrumentCsvs=True)
