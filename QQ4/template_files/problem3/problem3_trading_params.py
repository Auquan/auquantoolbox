import sys
import os
sys.path.append(os.getcwd())
from backtester.trading_system_parameters import TradingSystemParameters
from backtester.features.feature import Feature
from datetime import timedelta
from backtester.dataSource.csv_data_source import CsvDataSource
from backtester.timeRule.nse_time_rule import NSETimeRule
from problem3_execution_system import SimpleExecutionSystem
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.trading_system import TradingSystem
from backtester.version import updateCheck
from backtester.constants import *
import pandas as pd
import numpy as np
from datetime import datetime


SYMBOLS_IN_BASKET = 10

class MyTradingParams(TradingSystemParameters):
    '''
    initialize class
    place any global variables here
    '''
    def __init__(self, tradingFunctions):
        self.__tradingFunctions = tradingFunctions
        self.__priceKey = 'F5'
        self.__additionalInstrumentFeatureConfigDicts = []
        self.__additionalMarketFeatureConfigDicts = []
        self.__fees = {'brokerage': 0.0001,'spread': 0.05}
        self.__startDate = '2010/06/02'
        self.__endDate = '2010/09/02'
        super(MyTradingParams, self).__init__()
        self.__dataSetId = 'QQ3DataDownSampled'
        self.__instrumentIds = ['SIZ', 'MLQ','DFY', 'OAX']


    '''
    Returns an instance of class DataParser. Source of data for instruments
    '''

    def getDataParser(self):
        instrumentIds = self.__instrumentIds
        return CsvDataSource(cachedFolderName='historicalData/',
                             dataSetId=self.__dataSetId,
                             instrumentIds=self.__instrumentIds,
                             downloadUrl = 'https://raw.githubusercontent.com/Auquan/qq3Data/master',
                             timeKey = 'datetime',
                             timeStringFormat = '%Y-%m-%d %H:%M:%S',
                             startDateStr=self.__startDate,
                             endDateStr=self.__endDate)

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
        return NSETimeRule(startDate=self.__startDate, endDate=self.__endDate, startTime='15:30', frequency='M', sample='1440')

    '''
    Returns a timedetla object to indicate frequency of updates to features
    Any updates within this frequncy to instruments do not trigger feature updates.
    Consequently any trading decisions that need to take place happen with the same
    frequency
    '''

    def getFrequencyOfFeatureUpdates(self):
        return timedelta(60, 0)  # minutes, seconds

    def getStartingCapital(self):
        return 2*1.15*10000*SYMBOLS_IN_BASKET

    '''
    This is a way to use any custom features you might have made.
    Returns a dictionary where
    key: featureId to access this feature (Make sure this doesnt conflict with any of the pre defined feature Ids)
    value: Your custom Class which computes this feature. The class should be an instance of Feature
    Eg. if your custom class is MyCustomFeature, and you want to access this via featureId='my_custom_feature',
    you will import that class, and return this function as {'my_custom_feature': MyCustomFeature}
    '''

    def getCustomFeatures(self):
        customFeatures = {'prediction': TrainingPredictionFeature,
                'fees_and_spread': FeesCalculator,
                'benchmark_PnL': BuyHoldPnL,
                'ScoreCalculator' : ScoreCalculator}
        customFeatures.update(self.__tradingFunctions.getCustomFeatures())


        return customFeatures


    def getInstrumentFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE

        predictionDict = {'featureKey': 'prediction',
                                'featureId': 'prediction',
                                'params': {'tradingFunctions':self.__tradingFunctions}}
        feesConfigDict = {'featureKey': 'fees',
                          'featureId': 'fees_and_spread',
                          'params': {'feeDict': self.__fees,
                                    'price': self.getPriceFeatureKey(),
                                    'position' : 'position'}}
        profitlossConfigDict = {'featureKey': 'pnl',
                                'featureId': 'pnl',
                                'params': {'price': self.getPriceFeatureKey(),
                                           'fees': 'fees'}}
        capitalConfigDict = {'featureKey': 'capital',
                             'featureId': 'capital',
                             'params': {'price': self.getPriceFeatureKey(),
                                        'fees': 'fees',
                                        'capitalReqPercent': 0.95}}
        benchmarkDict = {'featureKey': 'benchmark',
                     'featureId': 'benchmark_PnL',
                     'params': {'pnlKey': 'pnl',
                                'price': self.getPriceFeatureKey()}}

        scoreDict = {'featureKey': 'score',
                     'featureId': 'ScoreCalculator',
                     'params': {'predictionKey': 'prediction',
                                'tradingFunctions': self.__tradingFunctions,
                                'price': self.getPriceFeatureKey()}}


        stockFeatureConfigs = self.__tradingFunctions.getInstrumentFeatureConfigDicts()


        return {INSTRUMENT_TYPE_STOCK: stockFeatureConfigs + [predictionDict,
                feesConfigDict,profitlossConfigDict,capitalConfigDict,benchmarkDict, scoreDict]
                + self.__additionalInstrumentFeatureConfigDicts}

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
                     'featureId': 'ScoreCalculator',
                     'params': {'instrument_score_feature': 'score'}}

        marketFeatureConfigs = self.__tradingFunctions.getMarketFeatureConfigDicts()
        return marketFeatureConfigs + [scoreDict] +self.__additionalMarketFeatureConfigDicts

    '''
    Returns the type of execution system we want to use. Its an implementation of the class ExecutionSystem
    It converts prediction to intended positions for different instruments.
    '''

    def getExecutionSystem(self):
        return SimpleExecutionSystem(logFileName = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'),
                                    enter_threshold=0.99,
                                    exit_threshold=0.55,
                                    longLimit=10000,
                                    shortLimit=10000,
                                    capitalUsageLimit=0.10 * self.getStartingCapital(),
                                    enterlotSize = 10000, exitlotSize = 10000,
                                    limitType='D', price=self.getPriceFeatureKey())

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

    def getSymbolsInBasket(self):
        return 10

    def getLookbackSize(self):
        return max(720, self.__tradingFunctions.getLookbackSize())

    def getPriceFeatureKey(self):
        return self.__priceKey

    def setPriceFeatureKey(self, priceKey='Adj_Close'):
        self.__priceKey = priceKey

    def getDataSetId(self):
        return self.__dataSetId

    def setDataSetId(self, dataSetId):
        self.__dataSetId = dataSetId

    def getInstrumentsIds(self):
        return self.__instrumentIds

    def setInstrumentsIds(self, instrumentIds):
        self.__instrumentIds = instrumentIds

    def getDates(self):
        return {'startDate':self.__startDate,
                'endDate':self.__endDate}

    def setDates(self, dateDict):
        self.__startDate = dateDict['startDate']
        self.__endDate = dateDict['endDate']

    def setFees(self, feeDict={'brokerage': 0.0001,'spread': 0.05}):
        self.__fees = feeDict

    def setAdditionalInstrumentFeatureConfigDicts(self, dicts = []):
        self.__additionalInstrumentFeatureConfigDicts = dicts

    def setAdditionalMarketFeatureConfigDicts(self, dicts = []):
        self.__additionalMarketFeatureConfigDicts = dicts

class TrainingPredictionFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        predictions = pd.Series(index = instrumentManager.getAllInstrumentsByInstrumentId())
        tf = featureParams['tradingFunctions']
        factorValues =  tf.createRankingFeature(time, updateNum, instrumentManager)

        factorValues.iloc[-1].sort_values(0, inplace=True)

        #Derive rank from factor values
        ranks = factorValues.iloc[-1].rank(0)

        # Put stocks with no rank in the middle
        ranks.fillna(len(predictions.index)/2, inplace=True)

        if len(factorValues.index) > 1:
            oldFactorValues = factorValues.iloc[-2]
            oldranks = oldFactorValues.rank(0)
            oldranks.fillna(len(predictions.index)/2, inplace=True)
        else:
            oldranks = pd.Series(len(predictions.index)/2, index = ranks.index)

        # Short position in the lowest ranked stocks
        predictions[ranks<=SYMBOLS_IN_BASKET] = 0
        # we are already short stocks that ranked lowest previous time, don't sell again them
        predictions[(oldranks<=SYMBOLS_IN_BASKET) & (ranks<=SYMBOLS_IN_BASKET)] = 0.25
        predictions[ranks>SYMBOLS_IN_BASKET] = 0.5

        # Long position in the highest ranked stocks
        predictions[ranks>(len(predictions.index)-SYMBOLS_IN_BASKET)] = 1
        # we are already long stocks that ranked highest previous time, don't buy again them
        predictions[(oldranks>(len(predictions.index)-SYMBOLS_IN_BASKET)) &\
                 (ranks>(len(predictions.index)-SYMBOLS_IN_BASKET))] = 0.75


        return predictions

class FeesCalculator(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()

        priceData = instrumentLookbackData.getFeatureDf(featureParams['price'])
        positionData = instrumentLookbackData.getFeatureDf(featureParams['position'])
        currentPosition = positionData.iloc[-1]
        previousPosition = 0 if updateNum < 2 else positionData.iloc[-2]
        changeInPosition = currentPosition - previousPosition
        fees = pd.Series(np.abs(changeInPosition)*featureParams['feeDict']['brokerage'],index = instrumentManager.getAllInstrumentsByInstrumentId())
        if len(priceData)>1:
            currentPrice = priceData.iloc[-1]
        else:
            currentPrice = 0

        fees = fees*currentPrice + np.abs(changeInPosition)*featureParams['feeDict']['spread']

        return fees



class BuyHoldPnL(Feature):
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()

        priceData = instrumentLookbackData.getFeatureDf(featureParams['price'])
        bhpnl = pd.Series(0,index = instrumentManager.getAllInstrumentsByInstrumentId())
        if len(priceData)>1:
            bhpnl += priceData.iloc[-1] - priceData.iloc[-2]

        return bhpnl

class ScoreCalculator(Feature):
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()

        priceData = instrumentLookbackData.getFeatureDf(featureParams['price'])

        tf = featureParams['tradingFunctions']
        factorValues =  tf.createRankingFeature(time, updateNum, instrumentManager)
        score = pd.Series(0,index = instrumentManager.getAllInstrumentsByInstrumentId())

        if updateNum>75:

            factorValues.iloc[-76].sort_values(0, inplace=True)

            #Derive rank from factor values
            ranks = factorValues.iloc[-76].rank(0)

            # Put stocks with no rank in the middle
            ranks.fillna(len(score.index)/2, inplace=True)
            changeInPrice = priceData.iloc[-1] / priceData.iloc[-76]
            #Derive rank from change in price
            ranks2 = changeInPrice.rank(0)

            # Put stocks with no rank in the middle
            ranks2.fillna(len(changeInPrice.index)/2, inplace=True)
            scoreDict = instrumentLookbackData.getFeatureDf(featureKey)
            oldscore = scoreDict.iloc[-1]
            newscore = ranks2.corr(ranks)

            score = (oldscore*(updateNum-1)+newscore)/(updateNum)
        return score

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        score = 0
        scoreDict = instrumentManager.getDataDf()[featureKey]
        scoreKey = 'score'
        if 'instrument_score_feature' in featureParams:
            scoreKey = featureParams['instrument_score_feature']
        if len(scoreDict) < 1:
            return 0
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        score = instrumentLookbackData.getFeatureDf(scoreKey).iloc[-1].mean()
        allInstruments = instrumentManager.getAllInstrumentsByInstrumentId()
        return score


class RankPnL(Feature):
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()

        priceData = instrumentLookbackData.getFeatureDf(featureParams['price'])
        score = pd.Series(0,index = instrumentManager.getAllInstrumentsByInstrumentId())
        if updateNum>75:
            changeInPrice = priceData.iloc[-1] - priceData.iloc[-76]
            ranks = changeInPrice.rank(0)

            # Put stocks with no rank in the middle
            ranks.fillna(len(changeInPrice.index)/2, inplace=True)
            scoreDict = instrumentLookbackData.getFeatureDf(featureKey)
            score = scoreDict.iloc[-1]
            score[ranks<=6] = scoreDict.iloc[-1] + 1
            score[ranks>(len(ranks)-6)] = scoreDict.iloc[-1] - 1
        return score
