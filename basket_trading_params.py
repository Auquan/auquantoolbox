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
import pandas as pd
from backtester.logger import *
instrumentIds = ['FEDERALBNK', 'ICICIBANK', 'CANBK', 
                 'SBIN', 'YESBANK', 'PNB', 
                 'KOTAKBANK', 'BANKBARODA', 'HDFCBANK', 
                 'AXISBANK', 'INDUSINDBK']

class MyTradingParams(TradingSystemParameters):
    '''
    Returns an instance of class DataParser. Source of data for instruments
    '''

    def getDataParser(self):
        instrumentsToGet = list(set(instrumentIds + [self.getBenchmark()]))
        startDateStr = '2010/01/01'
        endDateStr = '2017/06/30'
        return NSEStockDataSource(cachedFolderName='nseData',
                                     instrumentIds=instrumentsToGet,
                                     startDateStr=startDateStr,
                                     endDateStr=endDateStr)

    def getBenchmark(self):
        return 'BANKBEES'

    def getCustomFeatures(self):
        return {'my_custom_feature': MyCustomFeature}

    def getInstrumentFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE
        momDict = {'featureKey': 'mom_5',
                   'featureId': 'momentum',
                   'params': {'period': 5,
                              'featureName': 'close'}}
        ma1Dict = {'featureKey': 'ma_30',
                   'featureId': 'moving_average',
                   'params': {'period': 30,
                              'featureName': 'close'}}
        ma2Dict = {'featureKey': 'ma_5',
                   'featureId': 'moving_average',
                   'params': {'period': 5,
                              'featureName': 'close'}}
        sdevDict = {'featureKey': 'sdev_30',
                    'featureId': 'moving_sdev',
                    'params': {'period': 30,
                               'featureName': 'close'}}
        rsiDict = {'featureKey': 'rsi_14',
                   'featureId': 'rsi',
                   'params': {'period': 14,
                              'featureName': 'close'}}
        return {INSTRUMENT_TYPE_STOCK: [momDict, ma1Dict, ma2Dict, sdevDict, rsiDict]}

    def getMarketFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE
        return []

    def getPrediction(self, time, currentMarketFeatures, instrumentManager):
        # IMPLEMENT THIS

        ### Getting all instrument ids
        #instrumentIds = instrumentManager.getAllInstrumentsByInstrumentId()
        predictions = {ids: 0.5 for ids in instrumentIds}
        score = pd.Series(0, index = instrumentIds)

        ### Calculating Score for each instrument
        for ids in instrumentIds:
            instrument = instrumentManager.getInstrument(ids)

            if instrument is None:
                predictions[ids] = 0.5

            else:
                lookbackInstrumentFeatures = instrument.getDataDf().iloc[-1]
                if lookbackInstrumentFeatures['sdev_30'] != 0:
                    z_score = (lookbackInstrumentFeatures['ma_5'] - lookbackInstrumentFeatures['ma_30']) / lookbackInstrumentFeatures['sdev_30']
                else:
                    z_score = 0

                score[ids] = 10* lookbackInstrumentFeatures['mom_5'] + \
                                lookbackInstrumentFeatures['rsi_14'] - \
                                5 * z_score
        
        ### Sort based on score
        score.dropna(inplace=True)
        score.sort_values(inplace=True)

        if len(score.index) > 0 :
            ### Buy the top two and sell the bottom two
            predictions[score.index[0]] = 0.8
            predictions[score.index[1]] = 0.8
            predictions[score.index[2]] = 0.6
            predictions[score.index[-3]] = 0.4
            predictions[score.index[-2]] = 0.2
            predictions[score.index[-1]] = 0.2

        return predictions

    def getExecutionSystem(self):
        longLimit = {}
        shortLimit = {}
        lotSize = {}
        for i in instrumentIds:
            longLimit[i] = 5000000
            shortLimit[i] = 5000000
            lotSize[i] = 500000

        return SimpleExecutionSystem(enter_threshold=0.7, 
                                     exit_threshold=0.55, 
                                     longLimit=longLimit, 
                                     shortLimit=shortLimit,
                                     capitalUsageLimit = 0.10*self.getStartingCapital(), 
                                     lotSize=lotSize, limitType='D',price=self.getPriceFeatureKey())

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
        return 35


if __name__ == "__main__":
    tsParams = MyTradingParams()
    tradingSystem = TradingSystem(tsParams)
    tradingSystem.startTrading(onlyAnalyze=False, shouldPlot=True)
