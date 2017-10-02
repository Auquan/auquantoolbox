from backtester.features.feature import Feature
from backtester.trading_system import TradingSystem
from backtester.sample_scripts.feature_prediction_params import FeaturePredictionTradingParams
from backtester.version import updateCheck
import numpy as np
import scipy.stats as st
import os
import cPickle as pickle

def writeToFile(resultDict,full_path):
  with open(full_path, 'wb') as f:
    f.write(pickle.dumps(resultDict))

def readFromFile(full_path):
  with open(full_path, mode='rb') as infile:
    resultDict = pickle.load(infile)
  return resultDict

def equals(l1, l2):
    if len(l1)-len(l2):
      return False
    for u in range(len(l1)):
        if l1[u] != l2[u]:
          return False
    return True

# content of test_class.py
class TestProblem2(object):
    def test_problem2(self):
        solver = Solver()

        script_dir = os.path.dirname(__file__)  # Script directory
        full_path = os.path.join(script_dir, 'historicalData/testDataP2/correct.pkl')
        
        tsParams = FeaturePredictionTradingParams(solver)
        tradingSystem = TradingSystem(tsParams)
        # Set onlyAnalyze to True to quickly generate csv files with all the features
        # Set onlyAnalyze to False to run a full backtest
        self.resultDict = tradingSystem.startTrading(onlyAnalyze=False, shouldPlot=False, makeInstrumentCsvs=True)
        # import pdb; pdb.set_trace()
        assert self.resultDict != None
        # function to write data to correct.csv
        # writeToFile(self.resultDict,full_path)
        
        resultDictKeys = self.resultDict.keys()

        assert 'metrics' in resultDictKeys
        assert 'metrics_values' in resultDictKeys
        assert 'instrument_names' in resultDictKeys
        assert 'instrument_stats' in resultDictKeys
        assert 'total_pnl' in resultDictKeys
        assert 'dates' in resultDictKeys
        assert 'score' in resultDictKeys

        self.correct = readFromFile(full_path)
        self.verify_metrics()
        self.verify_pnl()
        self.verify_dates()
        self.verify_scores()
        self.verify_instrument_stats()
        

    def verify_metrics(self):
        assert equals(self.correct['metrics'],self.resultDict['metrics'])
        assert equals(self.correct['metrics_values'],self.resultDict['metrics_values'])

    def verify_pnl(self):
        assert equals(self.correct['total_pnl'],self.resultDict['total_pnl'])
        
    def verify_dates(self):    
        assert equals(self.correct['dates'],self.resultDict['dates'])
        
    def verify_scores(self):    
        assert self.correct['score']==self.resultDict['score']

    def verify_instrument_stats(self):
        assert equals(self.correct['instrument_names'],self.resultDict['instrument_names'])
        assert equals(self.correct['instrument_stats'],self.resultDict['instrument_stats'])

class Solver():
    def getTrainingDataSet(self):
        return "testDataP2"

    def getCustomFeatures(self):
        return {'my_custom_feature': None}

    def getSymbolsToTrade(self):
        return ['AIO']

    def getFeatureConfigDicts(self):
        moving_avg = {'featureKey': 'ma_5',
                  'featureId': 'moving_average',
                  'params': {'period': 5,
                             'featureName': 'stockTopAskPrice'}}
        ma_30 = {'featureKey': 'ma_30',
                  'featureId': 'moving_average',
                  'params': {'period': 30,
                             'featureName': 'stockTopAskPrice'}}
        moving_max = {'featureKey': 'moving_max',
                          'featureId': 'moving_max',
                          'params': {'period': 5,
                                     'featureName': 'stockTopAskPrice'}}
        moving_min = {'featureKey': 'moving_min',
                          'featureId': 'moving_min',
                          'params': {'period': 5,
                                     'featureName': 'stockVWAP'}}
        moving_sdev = {'featureKey': 'moving_sdev',
                          'featureId': 'moving_sdev',
                          'params': {'period': 30,
                                     'featureName': 'stockVWAP'}}
        moving_sum = {'featureKey': 'moving_sum',
                          'featureId': 'moving_sum',
                          'params': {'period': 5,
                                     'featureName': 'stockVWAP'}}
        ema = {'featureKey': 'exponential_moving_average',
                          'featureId': 'exponential_moving_average',
                          'params': {'period': 5,
                                     'featureName': 'stockVWAP'}}
        diff = {'featureKey': 'difference',
                          'featureId': 'difference',
                          'params': {'period': 5,
                                     'featureName': 'stockVWAP'}}
        # mmt = {'featureKey': 'momentum',
        #                   'featureId': 'momentum',
        #                   'params': {'period': 5,
        #                              'featureName': 'basis'}}
        argmax = {'featureKey': 'argmax',
                          'featureId': 'argmax',
                          'params': {'period': 5,
                                     'featureName': 'stockVWAP'}}
        argmin = {'featureKey': 'argmin',
                          'featureId': 'argmin',
                          'params': {'period': 5,
                                     'featureName': 'stockVWAP'}}
        delay = {'featureKey': 'delay',
                          'featureId': 'delay',
                          'params': {'period': 5,
                                     'featureName': 'stockVWAP'}}
        rank = {'featureKey': 'rank',
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
        # scale = {'featureKey': 'scale',
        #                   'featureId': 'scale',
        #                   'params': {'period': 5,
        #                              'featureName': 'basis', 'scale': 3}}
        rsi = {'featureKey': 'rsi',
                          'featureId': 'rsi',
                          'params': {'period': 5,
                                     'featureName': 'stockVWAP'}}
        capital = {'featureKey': 'capital',
                          'featureId': 'capital',
                          'params': {'price': 'basis'}}
        portfolio_value = {'featureKey': 'portfolio_value',
                          'featureId': 'portfolio_value'}
        csm = {'featureKey': 'cross_sectional_momentum',
                          'featureId': 'cross_sectional_momentum',
                          'params': {'period': 5,
                                     'featureName': 'stockVWAP'}}
        ratio = {'featureKey': 'ratio',
                          'featureId': 'ratio',
                          'params': {'instrumentId1': "AGW", 'instumentId2': "AIO",
                                     'featureName1': 'stockVWAP', 'featureName2': 'ma_5'}}

        return [moving_avg, ma_30, moving_max, moving_min, moving_sdev, moving_sum, ema, diff, rsi, argmax, argmin, delay, rank, ratio]

    def getClassifierProbability(self, updateNum, time, instrumentManager):
        # holder for all the instrument features
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()

        # dataframe for a historical instrument feature (exponential_moving_average in this case). The index is the timestamps
        # atmost upto lookback data points. The columns of this dataframe are the stocks/instrumentIds.
        sdevDf = lookbackInstrumentFeatures.getFeatureDf('moving_sdev')
        mavg30Df = lookbackInstrumentFeatures.getFeatureDf('ma_30')
        mavg5Df = lookbackInstrumentFeatures.getFeatureDf('ma_5')

        z_score = (mavg30Df.iloc[-1] - mavg5Df.iloc[-1]) / sdevDf.iloc[-1]
        z_score.fillna(0, inplace=True)
        return st.norm.cdf(z_score)