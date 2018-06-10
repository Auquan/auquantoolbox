from backtester.trading_system_parameters import TradingSystemParameters
from datetime import timedelta
from backtester.dataSource.yahoo_data_source import YahooStockDataSource
from backtester.dataSource.nse_data_source import NSEStockDataSource
from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem
from backtester.executionSystem.pair_execution_system import PairExecutionSystem
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.trading_system import TradingSystem
from backtester.constants import *
from my_custom_feature import MyCustomFeature
from backtester.timeRule.us_time_rule import USTimeRule
from backtester.features.feature import Feature
import pandas as pd
import numpy as np


PAIRIDS = {1 : ['AAPL', 'GOOG'],
           2 : ['ADBE', 'MSFT']}

instrumentIds = ['AAPL', 'ADBE', 'GOOG', 'MSFT']


class MyTradingParams(TradingSystemParameters):
    '''
    Returns an instance of class DataParser. Source of data for instruments
    '''

    def getDataParser(self):
        startDateStr = '2007/12/31'
        endDateStr = '2017/12/31'
        return YahooStockDataSource(cachedFolderName='yahooData/',
                                     dataSetId='testPairsTrading',
                                     instrumentIds=instrumentIds,
                                     startDateStr=startDateStr,
                                     endDateStr=endDateStr)

    '''
    This is a way to use any custom features you might have made.
    Returns a dictionary where
    key: featureId to access this feature (Make sure this doesnt conflict with any of the pre defined feature Ids)
    value: Your custom Class which computes this feature. The class should be an instance of Feature
    Eg. if your custom class is MyCustomFeature, and you want to access this via featureId='my_custom_feature',
    you will import that class, and return this function as {'my_custom_feature': MyCustomFeature}
    '''

    def getBenchmark(self):
        return None

    def getCustomFeatures(self):
        return {'my_custom_feature': MyCustomFeature,
                'pairvalue_prediction': PairValuePredictionFeature}

    def getTimeRuleForUpdates(self):
        return USTimeRule(startDate = '2007/12/31',
                          endDate = '2017/12/31')

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
        ma1Dict = {'featureKey': 'ma_90',
                   'featureId': 'moving_average',
                   'params': {'period': 90,
                              'featureName': 'adjClose'}}
        ma2Dict = {'featureKey': 'ma_15',
                   'featureId': 'moving_average',
                   'params': {'period': 15,
                              'featureName': 'adjClose'}}
        sdevDict = {'featureKey': 'ma_15',
                    'featureId': 'moving_average',
                    'params': {'period': 15,
                              'featureName': 'adjClose'}}

        pairValuePrediction = {'featureKey': 'prediction',
                               'featureId': 'pairvalue_prediction',
                               'params': {}}
        return {INSTRUMENT_TYPE_STOCK: [pairValuePrediction]}

    '''
    Returns an array of market feature config dictionaries
        market feature config Dictionary has the following keys:
        featureId: a string representing the type of feature you want to use
        featureKey: a string representing the key you will use to access the value of this feature.this
        params: A dictionary with which contains other optional params if needed by the feature
    '''

    def getMarketFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE

        ratio1Dict = {'featureKey': 'ratio1',
                     'featureId': 'ratio',
                     'params': {'instrumentId1': PAIRIDS[1][0],
                                'instrumentId2': PAIRIDS[1][1],
                                'featureName': 'adjClose'}}
        ratio2Dict = {'featureKey': 'ratio2',
                     'featureId': 'ratio',
                     'params': {'instrumentId1': PAIRIDS[2][0],
                                'instrumentId2': PAIRIDS[2][1],
                                'featureName': 'adjClose'}}
        ma11Dict = {'featureKey': 'ma_r1_90',
                   'featureId': 'moving_average',
                   'params': {'period': 90,
                              'featureName': 'ratio1'}}
        ma21Dict = {'featureKey': 'ma_r1_10',
                   'featureId': 'moving_average',
                   'params': {'period': 10,
                              'featureName': 'ratio1'}}
        sdev1Dict = {'featureKey': 'sdev_r1_90',
                    'featureId': 'moving_sdev',
                    'params': {'period': 90,
                               'featureName': 'ratio1'}}
        ma12Dict = {'featureKey': 'ma_r2_90',
                   'featureId': 'moving_average',
                   'params': {'period': 90,
                              'featureName': 'ratio2'}}
        ma22Dict = {'featureKey': 'ma_r2_10',
                   'featureId': 'moving_average',
                   'params': {'period': 10,
                              'featureName': 'ratio2'}}
        sdev2Dict = {'featureKey': 'sdev_r2_90',
                    'featureId': 'moving_sdev',
                    'params': {'period': 90,
                               'featureName': 'ratio2'}}
        correl1Dict = {'featureKey': 'correl_r1_90',
                    'featureId': 'cross_instrument_correlation',
                    'params': {'period': 90,
                               'instrumentId1': PAIRIDS[1][0],
                                'instrumentId2': PAIRIDS[1][1],
                                'featureName': 'adjClose'}}
        correl2Dict = {'featureKey': 'correl_r2_90',
                    'featureId': 'cross_instrument_correlation',
                    'params': {'period': 90,
                               'instrumentId1': PAIRIDS[2][0],
                                'instrumentId2': PAIRIDS[2][1],
                                'featureName': 'adjClose'}}

        # customFeatureDict = {'featureKey': 'custom_mrkt_feature',
        #                      'featureId': 'my_custom_mrkt_feature',
        #                      'params': {'param1': 'value1'}}
        return [ratio1Dict, ma11Dict, ma21Dict, sdev1Dict, correl1Dict,
                ratio2Dict, ma12Dict, ma22Dict, sdev2Dict, correl2Dict]

    '''
    Returns the type of execution system we want to use. Its an implementation of the class ExecutionSystem
    It converts prediction to intended positions for different instruments.
    '''

    def getExecutionSystem(self):
        # return PairExecutionSystem(pair=[instrumentIds[0], instrumentIds[1]],
        #                            pairRatio=0.3,
        #                            pairEnter_threshold=0.7,
        #                            pairExit_threshold=0.55,
        #                            pairLongLimit=20000,
        #                            pairShortLimit=20000,
        #                            pairCapitalUsageLimit = 0.10*self.getStartingCapital(),
        #                            pairLotSize=200)
        return SimpleExecutionSystem(enter_threshold=0.7, exit_threshold=0.55,
                                    longLimit=10000,shortLimit=10000, capitalUsageLimit=.85,
                                    enterlotSize=10000, exitlotSize = 10000, limitType='D', price='adjClose')


            # enter_threshold=0.7,
            #                          exit_threshold=0.55,
            #                          longLimit={'ADANIPOWER.BO': 100,'RPOWER.BO': 100 * ratio},
            #                          shortLimit={'ADANIPOWER.BO': -100,'RPOWER.BO': -100 * ratio},
            #                          lotSize={'ADANIPOWER.BO': 10,'RPOWER.BO': 10 * ratio})

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


class PairValuePredictionFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
    # def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackMarketFeatures = instrumentManager.getDataDf()

        prediction = pd.Series(0.5, index = instrumentManager.getAllInstrumentsByInstrumentId())
        if len(lookbackMarketFeatures)>0:
            currentMarketFeatures = lookbackMarketFeatures.iloc[-1]
            # IMPLEMENT THIS
            z_score = pd.Series(index = PAIRIDS.keys())
            for i in PAIRIDS.keys():
                if currentMarketFeatures['sdev_r%s_90'%i] != 0:
                  z_score[i] = (currentMarketFeatures['ma_r%s_10'%i] - currentMarketFeatures['ma_r%s_90'%i]) / currentMarketFeatures['sdev_r%s_90'%i]
                else:
                  z_score[i] = 0
                instrument = instrumentManager.getInstrument(instrumentIds[0])
                #z_score = z_score + instrument.getDataDf()['position']/20000

                if currentMarketFeatures['correl_r%s_90'%i] < 0.5:
                  z_score[i] = 0


                if z_score[i] > 1:
                    prediction[PAIRIDS[i][0]] = 0
                    prediction[PAIRIDS[i][1]] = 1
                elif z_score[i] < -1:
                    prediction[PAIRIDS[i][0]] = 1
                    prediction[PAIRIDS[i][1]] = 0
                elif (z_score[i] > 0.5) or (z_score[i] < -0.5) :
                    prediction[PAIRIDS[i][0]] = 0.75
                    prediction[PAIRIDS[i][1]] = 0.25
                else:
                    prediction[PAIRIDS[i][0]] = 0.5
                    prediction[PAIRIDS[i][1]] = 0.5

        return prediction


if __name__ == "__main__":
    tsParams = MyTradingParams()
    tradingSystem = TradingSystem(tsParams)
    tradingSystem.startTrading(onlyAnalyze=False)
