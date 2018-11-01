from backtester.trading_system_parameters import TradingSystemParameters
from backtester.features.feature import Feature
from datetime import datetime, timedelta
from backtester.dataSource.csv_data_source import CsvDataSource
from problem2_execution_system import Problem2ExecutionSystem
from backtester.trading_system import TradingSystem
from backtester.version import updateCheck
from backtester.constants import *
from backtester.features.feature import Feature
from backtester.logger import *
import pandas as pd
import numpy as np
import sys
from problem2_trading_params import MyTradingParams

## Make your changes to the functions below.
## SPECIFY features you want to use in getInstrumentFeatureConfigDicts() and getMarketFeatureConfigDicts()
## Create your bid and offers using these features in makeMarket()
## SPECIFY any custom features in getCustomFeatures() below
## Don't change any other function
## The toolbox does the rest for you, from downloading and loading data to running backtest


class MyTradingFunctions():

    def __init__(self):  #Put any global variables here
        self.lookback = 1200  ## TODO: max number of historical datapoints you want at any given time
        self.dataSetId = 'QQ4Data'
        self.params = {}

        # for example you can import and store an ML model from scikit learn in this dict
        self.model = {}

        # and set a frequency at which you want to update the model

        self.updateFrequency = 5


    ###########################################
    ## ONLY FILL THE THREE FUNCTIONS BELOW    ##
    ###########################################

    '''
    Specify all Features you want to use by  by creating config dictionaries.
    Create one dictionary per feature and return them in an array.
    Feature config Dictionary have the following keys:
        featureId: a str for the type of feature you want to use
        featureKey: {optional} a str for the key you will use to call this feature
                    If not present, will just use featureId
        params: {optional} A dictionary with which contains other optional params if needed by the feature
    msDict = {'featureKey': 'ms_5',
              'featureId': 'moving_sum',
              'params': {'period': 5,
                         'featureName': 'basis'}}
    return [msDict]
    You can now use this feature by in getPRediction() calling it's featureKey, 'ms_5'
    '''

    def getInstrumentFeatureConfigDicts(self):

    ##############################################################################
    ### TODO 1: FILL THIS FUNCTION TO CREATE DESIRED FEATURES for each symbol. ###
    ### USE TEMPLATE BELOW AS EXAMPLE                                          ###
    ##############################################################################
        ask_mom1Dict = {'featureKey': 'ask_mom_5',
                   'featureId': 'momentum',
                   'params': {'period': 5,
                              'featureName': 'ask'}}
        ask_mom2Dict = {'featureKey': 'ask_mom_10',
                   'featureId': 'momentum',
                   'params': {'period': 10,
                              'featureName': 'ask'}}
        ask_ma1Dict = {'featureKey': 'ask_ma_5',
                   'featureId': 'moving_average',
                   'params': {'period': 5,
                              'featureName': 'ask'}}
        ask_ma2Dict = {'featureKey': 'ask_ma_10',
                   'featureId': 'moving_average',
                   'params': {'period': 10,
                              'featureName': 'ask'}}
        bid_mom1Dict = {'featureKey': 'bid_mom_5',
                       'featureId': 'momentum',
                       'params': {'period': 5,
                              'featureName': 'bid'}}
        bid_mom2Dict = {'featureKey': 'bid_mom_10',
                   'featureId': 'momentum',
                   'params': {'period': 10,
                              'featureName': 'bid'}}
        bid_ma1Dict = {'featureKey': 'bid_ma_5',
                   'featureId': 'moving_average',
                   'params': {'period': 5,
                              'featureName': 'bid'}}
        bid_ma2Dict = {'featureKey': 'bid_ma_10',
                   'featureId': 'moving_average',
                   'params': {'period': 10,
                              'featureName': 'bid'}}
        return [ask_mom1Dict, ask_mom2Dict, ask_ma1Dict, ask_ma2Dict, bid_mom1Dict, bid_mom2Dict, bid_ma1Dict, bid_ma2Dict]



    def getMarketFeatureConfigDicts(self):
    ###############################################################################
    ### TODO 2: FILL THIS FUNCTION TO CREATE features that use multiple symbols ###
    ### USE TEMPLATE BELOW AS EXAMPLE                                           ###
    ###############################################################################

        # customFeatureDict = {'featureKey': 'custom_mrkt_feature',
        #                      'featureId': 'my_custom_mrkt_feature',
        #                      'params': {'param1': 'value1'}}
        return []

    '''
    Combine all the features to create the desired market for each symbol.
    'marketSeries' is Pandas Series with symbol as index and tuple of (bid, ask) as values
    We first call the holder for all the instrument features for all symbols as
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()
    Then call the dataframe for a feature using its feature_key as
        ms5Data = lookbackInstrumentFeatures.getFeatureDf('ms_5')
    This returns a dataFrame for that feature for ALL symbols for all times upto lookback time
    Now you can call just the last data point for ALL symbols as
        ms5 = ms5Data.iloc[-1]
    You can call last datapoint for one symbol 'ABC' as
        value_for_abs = ms5['ABC']
    Output of the prediction function is used by the toolbox to make further trading decisions and evaluate your score.
    '''

    def makeMarket(self, time, updateNum, instrumentManager, marketSeries):
        # holder for all the instrument features for all instruments
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()
        # holder for all the market features
        lookbackMarketFeatures = instrumentManager.getDataDf()

        #############################################################################################
        ###  TODO 3 : FILL THIS FUNCTION TO RETURN A (bid,ask) for each stockID                   ###
        ###  You can use all the features created above and combine then using any logic you like ###
        ###  USE TEMPLATE BELOW AS EXAMPLE                                                        ###
        #############################################################################################

        # Time to start making the market.

        for stockId in self.getSymbolsToTrade():
            # First we get the bid and ask price series for all stocks
            askPrice = lookbackInstrumentFeatures.getFeatureDf('ask')[stockId]
            bidPrice = lookbackInstrumentFeatures.getFeatureDf('bid')[stockId]

            # This is a way to access the feature df's for every stock
            ask_ma_5 = lookbackInstrumentFeatures.getFeatureDf('ask_ma_5')[stockId]
            bid_ma_5 = lookbackInstrumentFeatures.getFeatureDf('bid_ma_5')[stockId]

            # In this simple case, we are just joining the market at current bid and ask price.
            marketSeries[stockId] = (bidPrice.iloc[-1], askPrice.iloc[-1])
        
        return marketSeries

    ###########################################
    ##         DONOT CHANGE THESE            ##
    ###########################################

    def getSymbolsToTrade(self):
        return ['SIZ','MLQ','MAI','PVV','IPV','DHP','EKA','EYC','YSB','SEP','INS','IIZ','DFY','OAX']

    def getPrediction(self, time, updateNum, instrumentManager,predictions):
        return self.makeMarket(time, updateNum, instrumentManager, predictions)

    def getLookbackSize(self):
        return self.lookback

    def getDataSetId(self):
        return self.dataSetId

    def getTargetVariableKey(self):
        return self.targetVariable

    def setTargetVariableKey(self, targetVariable):
        self.targetVariable = targetVariable

    ######################################################
    ##  TODO: CHANGE ONLY IF YOU HAVE CUSTOM FEATURES  ##
    ######################################################

    def getCustomFeatures(self):
        return {'my_custom_feature_identifier': MyCustomFeatureClassName}

####################################################
##   YOU CAN DEFINE ANY CUSTOM FEATURES HERE      ##
##  If YOU DO, MENTION THEM IN THE FUNCTION ABOVE ##
####################################################
class MyCustomFeatureClassName(Feature):
    ''''
    Custom Feature to implement for instrument. This function would return the value of the feature you want to implement.
    1. create a new class MyCustomFeatureClassName for the feature and implement your logic in the function computeForInstrument() -
    2. modify function getCustomFeatures() to return a dictionary with Id for this class
        (follow formats like {'my_custom_feature_identifier': MyCustomFeatureClassName}.
        Make sure 'my_custom_feature_identifier' doesnt conflict with any of the pre defined feature Ids
        def getCustomFeatures(self):
            return {'my_custom_feature_identifier': MyCustomFeatureClassName}
    3. create a dict for this feature in getInstrumentFeatureConfigDicts() above. Dict format is:
            customFeatureDict = {'featureKey': 'my_custom_feature_key',
                                'featureId': 'my_custom_feature_identifier',
                                'params': {'param1': 'value1'}}
    You can now use this feature by calling it's featureKey, 'my_custom_feature_key' in getPrediction()
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        # Custom parameter which can be used as input to computation of this feature
        param1Value = featureParams['param1']

        # A holder for the all the instrument features
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()

        # dataframe for a historical instrument feature (basis in this case). The index is the timestamps
        # atmost upto lookback data points. The columns of this dataframe are the symbols/instrumentIds.
        lookbackInstrumentValue = lookbackInstrumentFeatures.getFeatureDf('ask')

        # The last row of the previous dataframe gives the last calculated value for that feature (basis in this case)
        # This returns a series with symbols/instrumentIds as the index.
        currentValue = lookbackInstrumentValue.iloc[-1]

        if param1Value == 'value1':
            return currentValue * 0.1
        else:
            return currentValue * 0.5


if __name__ == "__main__":
    if updateCheck():
        print('Your version of the auquan toolbox package is old. Please update by running the following command:')
        print('pip install -U auquan_toolbox')
    else:
        print('Loading your config dicts and prediction function')
        tf = MyTradingFunctions()
        print('Loaded config dicts and prediction function, Loading Problem 2 Params')
        tsParams = MyTradingParams(tf)
        print('Loaded Problem 2 Params, Loading Backtester and Data')
        tradingSystem = TradingSystem(tsParams)
        print('Loaded Backtester and Data Loaded, Backtesting')
    # Set onlyAnalyze to True to quickly generate csv files with all the features
    # Set onlyAnalyze to False to run a full backtest
    # Set makeInstrumentCsvs to False to not make instrument specific csvs in runLogs. This improves the performance BY A LOT
        tradingSystem.startTrading(onlyAnalyze=False, shouldPlot=True, makeInstrumentCsvs=False)