import sys, os
parentPath = os.path.abspath(".")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from backtester.trading_system_parameters import TradingSystemParameters
from backtester.model_learning_system_parameters import ModelLearningSystemParamters, MLSTrainingPredictionFeature
from backtester.model_learning_and_trading_system import MLandTradingSystem
from backtester.features.feature import Feature
from backtester.dataSource.yahoo_data_source import YahooStockDataSource
from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.trading_system import TradingSystem
from backtester.timeRule.us_time_rule import USTimeRule
from backtester.version import updateCheck
from backtester.constants import *
import pandas as pd



class MyTradingParams(TradingSystemParameters):
    '''
    initialize class
    place any global variables here
    '''
    def __init__(self):
        super(MyTradingParams, self).__init__()
        self.count = 0
        self.params = {}
        self.startDate = '2007/12/31'
        self.endDate = '2017/12/31'
        self.instrumentIds = ['AAPL', 'GOOG']
        self.dataSourceName = 'YahooStockDataSource'
        self.dataSourceParams = dict(cachedFolderName='yahooData/',
                                    dataSetId='test',
                                    instrumentIds=self.instrumentIds,
                                    startDateStr=self.startDate,
                                    endDateStr=self.endDate,
                                    event='history')

    '''
    Returns the list of instrument IDs
    '''

    def getInstrumentIds(self):
        return self.instrumentIds

    def getDates(self):
        return {'startDate' : self.startDate,
                'endDate' : self.endDate}

    def setDates(self, dateDict):
        self.startDate = dateDict['startDate']
        self.endDate = dateDict['endDate']

    def getDataSourceName(self):
        return self.dataSourceName

    def getDataSourceParams(self):
        return self.dataSourceParams

    '''
    Returns an instance of class DataParser. Source of data for instruments
    '''

    def getDataParser(self):
        return YahooStockDataSource(**self.dataSourceParams)

    '''
    Return starting capital - the initial amount of money you're putting into your trading system
    '''
    def getStartingCapital(self):
        return 1000000

    '''
    Returns an instance of class TimeRule, which describes the times at which
    we should update all the features and try to execute any trades based on
    execution logic.
    For eg, for intra day data, you might have a system, where you get data
    from exchange at a very fast rate (ie multiple times every second). However,
    you might want to run your logic of computing features or running your execution
    system, only at some fixed intervals (like once every 5 seconds). This depends on your
    strategy whether its a high, medium, low frequency trading strategy. Also, performance
    is another concern. if your execution system and features computation are taking
    a lot of time, you realistically wont be able to keep upto pace.
    '''
    def getTimeRuleForUpdates(self):
        return USTimeRule(startDate = self.startDate,
                          endDate = self.endDate)

    '''
    This is a way to use any custom features you might have made.
    Returns a dictionary where
    key: featureId to access this feature (Make sure this doesnt conflict with any of the pre defined feature Ids)
    value: Your custom Class which computes this feature. The class should be an instance of Feature
    Eg. if your custom class is MyCustomFeature, and you want to access this via featureId='my_custom_feature',
    you will import that class, and return this function as {'my_custom_feature': MyCustomFeature}
    '''

    def getCustomFeatures(self):
        customFeatures = {'my_custom_feature': MyCustomFeature,
                          'prediction': TrainingPredictionFeature}
        return customFeatures

    def getCustomFeatureSelectionMethods(self):
        return {}

    def getCustomFeatureTransformationMethods(self):
        return {}

    def getCustomModelMethods(self):
        return {}


    '''
    Returns a dictionary with:
    key: string representing instrument type. Right now INSTRUMENT_TYPE_OPTION, INSTRUMENT_TYPE_STOCK, INSTRUMENT_TYPE_FUTURE
    value: Array of instrument feature config dictionaries
        feature config Dictionary has the following keys:
        featureId: a string representing the type of feature you want to use
        featureKey: {optional} a string representing the key you will use to access the value of this feature.
                    If not present, will just use featureId
        params: {optional} A dictionary with which contains other optional params if needed by the feature
    Example:
    positionConfigDict = {'featureId': 'position'}
    vwapConfigDict = {'featureKey': 'price',
                          'featureId': 'vwap'}
    movingAvg_30Dict = {'featureKey': 'mv_avg_30',
                          'featureId': 'moving_average',
                          'params': {'days': 30}}
    movingAvg_90Dict = {'featureKey': 'mv_avg_90',
                          'featureId': 'moving_average',
                          'params': {'days': 90}}
    return {INSTRUMENT_TYPE_FUTURE: [positionConfigDict, vwapConfigDict],
            INSTRUMENT_TYPE_STOCK: [positionConfigDict, movingAvg_30Dict, movingAvg_90Dict]}

    For each future instrument, you will have features keyed by position and price.
    For each stock instrument, you will have features keyed by position, mv_avg_30, mv_avg_90
    '''

    def getInstrumentFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE

        predictionDict = {'featureKey': 'prediction',
                                'featureId': 'prediction',
                                'params': {}}

        ### TODO: FILL THIS FUNCTION TO CREATE DESIRED FEATURES for each stock
        ### USE TEMPLATE BELOW AS EXAMPLE
        ma1Dict = {'featureKey': 'ma_90',
                   'featureId': 'moving_average',
                   'params': {'period': 90,
                              'featureName': 'Adj Close'}}
        ma2Dict = {'featureKey': 'ma_5',
                   'featureId': 'moving_average',
                   'params': {'period': 5,
                              'featureName': 'Adj Close'}}
        sdevDict = {'featureKey': 'sdev_90',
                    'featureId': 'moving_sdev',
                    'params': {'period': 90,
                               'featureName': 'Adj Close'}}
        momDict = {'featureKey': 'mom_90',
                   'featureId': 'momentum',
                   'params': {'period': 30,
                              'featureName': 'Adj Close'}}
        rsiDict = {'featureKey': 'rsi_30',
                   'featureId': 'rsi',
                   'params': {'period': 30,
                              'featureName': 'Adj Close'}}
        signDict = {'featureKey' : 'scale',
                    'featureId' : 'scale',
                    'params' : {'period': 3,
                               'featureName': 'Adj Close',
                               'scale': 3}}
        self.__stockFeatureConfigs = [ma1Dict, ma2Dict, sdevDict, momDict, rsiDict, signDict]
        return {INSTRUMENT_TYPE_STOCK: self.__stockFeatureConfigs + [predictionDict]}

    def getStockFeatureConfigDicts(self):
        return self.__stockFeatureConfigs

    '''
    Returns an array of market feature config dictionaries
        market feature config Dictionary has the following keys:
        featureId: a string representing the type of feature you want to use
        featureKey: a string representing the key you will use to access the value of this feature.this
        params: A dictionary with which contains other optional params if needed by the feature
    '''

    def getMarketFeatureConfigDicts(self):
    # ADD RELEVANT FEATURES HERE
        scoreDict = {'featureKey': 'score',
                     'featureId': 'score_ll',
                     'params': {'featureName': self.getPriceFeatureKey(),
                                'instrument_score_feature': 'pnl'}}
        return [scoreDict]


    '''
    A function that returns your predicted value based on your heuristics.
    If you are just trading one asset like a stock, it could be the predicted value of the stock.
    If you are doing pair trading, the prediction could be the difference in the prices of the stocks.
    Arguments:
    time - When this prediction is being calculated
    currentMarketFeatures - Dictionary of market features which have been calculated at this update cycle.
    instrumentManager - Holder for all instruments and everything else if you need.
    '''

    def getPrediction(self, time, updateNum, instrumentManager):

        predictions = pd.Series(index = self.instrumentIds)

        # holder for all the instrument features
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()

        ### TODO : FILL THIS FUNCTION TO RETURN A BUY (1) or SELL (0) prediction for each stock
        ### USE TEMPLATE BELOW AS EXAMPLE

        # dataframe for a historical instrument feature (ma_5 in this case). The index is the timestamps
        # of upto lookback data points. The columns of this dataframe are the stock symbols/instrumentIds.
        ma5Data = lookbackInstrumentFeatures.getFeatureDf('ma_5')
        ma90Data = lookbackInstrumentFeatures.getFeatureDf('ma_90')
        sdevData = lookbackInstrumentFeatures.getFeatureDf('sdev_90')

        # Get the last row of the dataframe, the most recent datapoint
        if len(ma5Data.index) > 0:
            ma5 = ma5Data.iloc[-1]
            ma90 = ma90Data.iloc[-1]
            sdev = sdevData.iloc[-1]

            #create Zscore

            z_score = (ma5 - ma90)/sdev
            z_score[sdev==0] = 0


            predictions[z_score>1] = 1  #Buy the stock
            predictions[z_score<-1] = 0 #Sell the stock
            predictions[(z_score<1) & (z_score>0.5)] = 0.75 # Don't buy but don't close existing positions either
            predictions[(z_score>-1) & (z_score<-0.5)] = 0.25 # Don't sell but don't close existing positions either
            predictions[(z_score>-.5) & (z_score<0.5)] = 0.5 # Close existing positions

        return predictions

    '''
    Returns the type of execution system we want to use. Its an implementation of the class ExecutionSystem
    It converts prediction to intended trades for different instruments.
    Instruments with probability predictions values above enter_threshold are bought and below (1-enter_threshold) are sold.
    Instrument positions with probability predictions values betweem (1-exit_threshold) and exit_threshold are closed
    '''

    def getExecutionSystem(self):
        return SimpleExecutionSystem(enter_threshold=0.7,
                                 exit_threshold=0.55,
                                 longLimit=10000,
                                 shortLimit=10000,
                                 capitalUsageLimit=0.10 * self.getStartingCapital(),
                                 enterlotSize=1, exitlotSize=1)

    '''
    Returns the type of order placer we want to use. its an implementation of the class OrderPlacer.
    It helps place an order, and also read confirmations of orders being placed.
    For Backtesting, you can just use the BacktestingOrderPlacer, which places the order which you want, and automatically confirms it too.
    '''

    def getOrderPlacer(self):
        return BacktestingOrderPlacer()

    '''
    Returns the amount of lookback data you want for your calculations. The historical market features and instrument features are only
    stored upto this amount.
    This number is the number of times we have updated our features.
    '''

    def getLookbackSize(self):
        return 90


    def getPriceFeatureKey(self):
        return 'Adj Close'

class MyModelLearningParams(ModelLearningSystemParamters):
    """
    """
    def __init__(self, tsParams, splitRatio, chunkSize=None, modelDir='savedModels'):
        self.tsParams = tsParams
        super(MyModelLearningParams, self).__init__(tsParams.getInstrumentIds(), chunkSize, modelDir)
        dates = self.tsParams.getDates()
        self.splitData(splitRatio, dates['startDate'], dates['endDate'])
        self.classificationModelKeys = ['mlp_classification', 'logistic_regression', 'svm_model']
        self.regressionModelKeys = ['linear_regression', 'mlp_regression']

    def getDataSourceName(self):
        return self.tsParams.getDataSourceName()

    def getDataSourceBaseParams(self):
        return self.tsParams.getDataSourceParams()

    def getInstrumentFeatureConfigDicts(self):
        stockFeatureConfigs = self.tsParams.getStockFeatureConfigDicts()
        return {INSTRUMENT_TYPE_STOCK : stockFeatureConfigs}

    def getCustomFeatures(self):
        customFeatures = {'prediction': MLSTrainingPredictionFeature}
        return customFeatures

    def getTargetVariableConfigDicts(self):
        Y = {'featureKey' : 'Y',
             'featureId' : '',
             'params' : {}}
        tv = {'featureKey' : 'difference_tv',
                  'featureId' : 'difference',
                  'params' : {'period' : 5,
                              'featureName' : 'ma_5',
                              'shift' : 5}}
        ctv = {'featureKey' : 'sign_tv',
                  'featureId' : 'sign',
                  'params' : {'period': 5,
                              'featureName' : 'mom_90',
                              'shift' : 5}}
        return {INSTRUMENT_TYPE_STOCK : [ctv]}

    def getFeatureSelectionConfigDicts(self):
        corr = {'featureSelectionKey': 'corr',
                'featureSelectionId' : 'pearson_correlation',
                'params' : {'startPeriod' : 0,
                            'endPeriod' : 60,
                            'steps' : 10,
                            'threshold' : 0.1,
                            'topK' : 2}}

        genericSelect = {'featureSelectionKey' : 'gus',
                         'featureSelectionId' : 'generic_univariate_select',
                         'params' : {'scoreFunction' : 'f_classif',
                                     'mode' : 'k_best',
                                     'modeParam' : 'all'}}
        return {INSTRUMENT_TYPE_STOCK : [genericSelect]}

    def getFeatureTransformationConfigDicts(self):
        stdScaler = {'featureTransformKey': 'stdScaler',
                     'featureTransformId' : 'standard_transform',
                     'params' : {}}

        minmaxScaler = {'featureTransformKey' : 'minmaxScaler',
                        'featureTransformId' : 'minmax_transform',
                        'params' : {'low' : -1,
                                    'high' : 1}}
        return {INSTRUMENT_TYPE_STOCK : [stdScaler]}

    def getModelConfigDicts(self):
        regressionModel = {'modelKey': 'linear_regression',
                     'modelId' : 'linear_regression',
                     'params' : {}}

        classificationModel = {'modelKey': 'logistic_regression',
                     'modelId' : 'logistic_regression',
                     'params' : {}}

        mlpClassificationModel = {'modelKey': 'mlp_classification',
                    'modelId' : 'mlp_classification',
                    'params' : {}}

        mlpRegressionModel = {'modelKey': 'mlp_regression',
                    'modelId' : 'mlp_regression',
                    'params' : {}}

        svmModel = {'modelKey': 'svm_model',
                    'modelId' : 'support_vector_machine',
                    'params' : {}}

        return {INSTRUMENT_TYPE_STOCK : [classificationModel, mlpClassificationModel]}

    def getMetricConfigDicts(self):
        accuracyScoreMetric = {'metricKey' : 'accuracy_score',
                                 'metricId' : 'accuracy_score',
                                 'params' : {}}

        explainedVarianceScoreMetric = {'metricKey' : 'explained_variance_score',
                                    'metricId' : 'explained_variance_score',
                                    'params' : {}}

        return {INSTRUMENT_TYPE_STOCK : [explainedVarianceScoreMetric]}

    def getMetricSelectionKey(self):
        variance = 'explained_variance_score'
        accuracy = 'accuracy_score'
        return variance

class TrainingPredictionFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        t = MyTradingParams()
        return t.getPrediction(time, updateNum, instrumentManager)



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
        lookbackInstrumentValue = lookbackInstrumentFeatures.getFeatureDf('Adj Close')

        # The last row of the previous dataframe gives the last calculated value for that feature (basis in this case)
        # This returns a series with stocks/instrumentIds as the index.
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
        tsParams = MyTradingParams()
        mlsParams = MyModelLearningParams(tsParams, splitRatio=[0.6, 0, 0.4], chunkSize=1000)
        system = MLandTradingSystem(tsParams, mlsParams)
        system.trainAndBacktest(onlyAnalyze=False, shouldPlot=True, makeInstrumentCsvs=True, useTargetVaribleFromFile=False)
