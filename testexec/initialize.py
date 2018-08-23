import pandas as pd
import numpy as np
import time
from collections import OrderedDict
from datetime import datetime, time, timedelta

class Initialize(object):

    def getDataSet(self,c):
            dict=OrderedDict()
            if c==0:
                dataSet = {"position":pd.DataFrame(),
                          "prediction":pd.DataFrame(),
                          "df":pd.DataFrame(),
                          "price":pd.DataFrame(),
                          "stockTopBidPrice":pd.DataFrame(),
                          "stockTopAskPrice":pd.DataFrame(),
                          "futureTopBidPrice":pd.DataFrame(),
                          "futureTopAskPrice":pd.DataFrame(),
                          "stockVWAP":pd.DataFrame(),
                          "enter_price":pd.DataFrame(),
                          "sdev":pd.DataFrame()
                          }

                parameters = {#"""*************** PARAMETERS FOR SimpleExecutionSystem ***********************""""
                              "enter_threshold":0.7, "exit_threshold":0.55, "longLimit":10, "shortLimit":10,
                              "capitalUsageLimit":0, "enterlotSize":1, "exitlotSize":1, "limitType":'L', "priceforSimpleExec" : "close",
                              #"""*************** PARAMETERS FOR BasisExecutionSystem ***********************""""
                              "basisEnter_thresholdforBasisExec":0.5,"basisExit_thresholdforBasisExec":0.1,"basisLongLimit":5000,
                              "basisShortLimit":5000,"basisCapitalUsageLimit":0.05,"basisLotSize":100,"basisLimitType":'L',"basis_thresholdParam":'sdev',
                              "feeDict":0.0001,"feesRatio":1.5,"spreadLimit":0.1,"hackTime":time(15,25,0),
                              #"""*************** PARAMETERS FOR PairExecutionSystem ***********************""""
                              "pair":[], "pairRatio":0.3, "pairEnter_threshold":0.7, "pairExit_threshold":0.55, "pairLongLimit":10,
                              "pairShortLimit":10, "pairCapitalUsageLimit":0, "pairLotSize":1, "priceforPairExec":None,
                              #"""*************** PARAMETERS FOR QQExecutionSystem ***********************""""
                              "basisEnter_thresholdforQQExec":0.1,"basisExit_thresholdforQQExec":0.05,"priceforQQExec":'',"feeDictforQQExec":0.05,
                              #"""*************** PARAMETERS FOR SimpleFairvalue ***********************""""
                              "enter_threshold_deviation":0.07, "exit_threshold_deviation":0.05,
                              #"""*************** PARAMETERS FOR Ramdom ***********************"""
                              "count":0,"currentPrediction":0.7,"capital":0.0,"closeAllPositions":False,"countforpairvalue":0
                              }

                results = { #"""****** RESULTS FOR SimpleExecutionSystem*************"""
                            'getPriceSeriesforSimpleExec'                       :   [0.0],
                            'getLongLimitforSimpleExec'                         :   [0.0],
                            'getShortLimitforSimpleExec'                        :   [0.0],
                            'getEnterLotSizeforSimpleExec'                      :   [0.0],
                            'getExitLotSizeforSimpleExec'                       :   [0.0],
                            'convertLimitforSimpleExec'                         :   [0.0],
                            'exitPositionforSimpleExec'                         :   [0.0],
                            'enterPositionforSimpleExec'                        :   [0.0],
                            'getBuySellforSimpleExec'                           :   [0.0],
                            'enterConditionforSimpleExec'                       :   [0.0],
                            'atPositionLimitforSimpleExec'                      :   [0.0],
                            'exitConditionforSimpleExec'                        :   [0.0],
                            'hackConditionforSimpleExec'                        :   [0.0],
                            #"""****** RESULTS FOR BasisExecutionSystem*************"""
                            'getDeviationFromPredictionforBasisExec'            :   [0.0],
                            'getSpreadforBasisExec'                             :   [0.0],
                            'getFeesforBasisExec'                               :   [0.0],
                            'getBuySellforBasisExec'                            :   [0.0],
                            'enterConditionforBasisExec'                        :   [0.0],
                            'exitConditionforBasisExec'                         :   [0.0],
                            'hackConditionforBasisExec'                         :   [0.0],
                            #"""****** RESULTS FOR QQExecutionSystem*************"""
                            'getDeviationFromPredictionforQQExec'               :   [0.0],
                            'getBuySellforQQExec'                               :   [0.0],
                            'enterConditionforQQExec'                           :   [0.0],
                            'exitConditionforQQExec'                            :   [0.0],
                            #"""****** RESULTS FOR SimpleExecutionSystemWithFairValue*************"""
                            'getDeviationFromPredictionforSimpleFairValueExec'  :   [0.0],
                            'getBuySellforforSimpleFairValueExec'               :   [0.0],
                            'enterConditionforSimpleFairValueExec'              :   [0.0],
                            'exitConditionforSimpleFairValueExec'               :   [0.0],
                            'hackConditionforSimpleFairValueExec'               :   [0.0]}

                return {"dataSet":dataSet, "results":results, "parameters":parameters, "dict":dict}

            if c==1:

                dict["a"]=1
                dict["b"]=2
                dict["c"]=3
                dict["d"]=4
                dict["e"]=5

                dataSet = {"position":          pd.DataFrame({'a':[1],'b':[2],'c':[3],'d':[4],'e':[5]},index =[pd.tslib.Timestamp('2017-01-03 09:30:30')]),
                          "prediction":         pd.DataFrame({'a':[0.5],'b':[0.2],'c':[0.8],'d':[1.0],'e':[0.0]}),
                          "df":                 pd.DataFrame({'a':[2.04],'b':[1.04],'c':[5.60],'d':[3.12],'e':[1.00]}),
                          "price":              pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]}),
                          "d":                  pd.DataFrame({'a':[1],'b':[2],'c':[3],'d':[4],'e':[5]}),
                          "stockTopAskPrice":   pd.DataFrame({'a':[1.24],'b':[2.02],'c':[3.14],'d':[4.24],'e':[5.96]}),
                          "stockTopBidPrice":   pd.DataFrame({'a':[-1.24],'b':[-2.02],'c':[-3.14],'d':[-4.24],'e':[-5.96]}),
                          "futureTopAskPrice":  pd.DataFrame({'a':[1.24],'b':[2.02],'c':[3.14],'d':[4.24],'e':[5.96]}),
                          "futureTopBidPrice":  pd.DataFrame({'a':[-1.24],'b':[-2.02],'c':[-3.14],'d':[-4.24],'e':[-5.96]}),
                          "stockVWAP":          pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]}),
                          "enter_price":        pd.DataFrame({'a':[1.24],'b':[2.02],'c':[3.14],'d':[4.24],'e':[5.96]}),
                          "sdev":               pd.DataFrame({'a':[3.14],'b':[2.04],'c':[0.02],'d':[0.98],'e':[-1.05]})
                          }

                parameters = {#"""*************** PARAMETERS FOR SimpleExecutionSystem ***********************""""
                              "enter_threshold":0.7, "exit_threshold":0.55, "longLimit":10, "shortLimit":10,
                              "capitalUsageLimit":0, "enterlotSize":1, "exitlotSize":1, "limitType":'R', "priceforSimpleExec" : "close",
                              #"""*************** PARAMETERS FOR BasisExecutionSystem ***********************""""
                              "basisEnter_thresholdforBasisExec":0.5,"basisExit_thresholdforBasisExec":0.1,"basisLongLimit":5000,
                              "basisShortLimit":5000,"basisCapitalUsageLimit":0.05,"basisLotSize":100,"basisLimitType":'L',
                              "basis_thresholdParam":'sdev',"feeDict":0.0001,"feesRatio":1.5,"spreadLimit":0.1,"hackTime":time(15,25,0),
                              #"""*************** PARAMETERS FOR PairExecutionSystem ***********************""""
                              "pair":['a','b'], "pairRatio":10, "pairEnter_threshold":0.7, "pairExit_threshold":0.55, "pairLongLimit":10,
                              "pairShortLimit":10, "pairCapitalUsageLimit":0, "pairLotSize":1, "priceforPairExec":None,
                              #"""*************** PARAMETERS FOR QQExecutionSystem ***********************""""
                              "basisEnter_thresholdforQQExec":0.1,"basisExit_thresholdforQQExec":0.05,"priceforQQExec":'',"feeDictforQQExec":0.05,
                              #"""*************** PARAMETERS FOR SimpleFairvalue ***********************""""
                              "enter_threshold_deviation":0.07, "exit_threshold_deviation":0.05,
                              #"""*************** PARAMETERS FOR Ramdom ***********************"""
                              "count":1,"currentPrediction":0.2,"capital":0.5,"closeAllPositions":True,"countforpairvalue":2
                              }

                results = { #"""****** RESULTS FOR SimpleExecutionSystem*************"""
                            'getPriceSeriesforSimpleExec'                       :   [3.14, 2.04, 1.02, 0.98, -1.05],
                            'getLongLimitforSimpleExec'                         :   [3.0, 4.0, 9.0, 10.0, -10.0],
                            'getShortLimitforSimpleExec'                        :   [3.0, 4.0, 9.0, 10.0, -10.0],
                            'getEnterLotSizeforSimpleExec'                      :   [0.0, 0.0, 0.0, 1.0, -1.0],
                            'getExitLotSizeforSimpleExec'                       :   [0.0, 0.0, 0.0, 1.0, -1.0],
                            'convertLimitforSimpleExec'                         :   [[0.0], [0.0], [5.0], [3.0], [-1.0]],
                            'exitPositionforSimpleExec'                         :   [-1, -2, -3, -4, -5],
                            'enterPositionforSimpleExec'                        :   [0, 0, 0, 1, 0],
                            'getBuySellforSimpleExec'                           :   [0.0, -1.0, 1.0, 1.0, -1.0],
                            'enterConditionforSimpleExec'                       :   [False, True, True, True, True],
                            'atPositionLimitforSimpleExec'                      :   [False, False, False, False, True],
                            'exitConditionforSimpleExec'                        :   [True, False, False, False, False],
                            'hackConditionforSimpleExec'                        :   [False,False,False,False,False],
                            #"""****** RESULTS FOR BasisExecutionSystem*************"""
                            'getDeviationFromPredictionforBasisExec'            :   [2.64, 1.84, 0.22, -0.02, -1.05],
                            'getSpreadforBasisExec'                             :   [1.24, 2.02, 3.14, 4.24, 5.96],
                            'getFeesforBasisExec'                               :   [0.000314, 0.000204, 0.000102, 9.8e-05, -0.000105],
                            'getBuySellforBasisExec'                            :   [-1.0, -1.0, -1.0, 1.0, 1.0],
                            'enterConditionforBasisExec'                        :   [True, True, False, False, True],
                            'exitConditionforBasisExec'                         :   [True, False, False, False, False],
                            'hackConditionforBasisExec'                         :   [True, True, False, True, False],
                            #"""****** RESULTS FOR QQExecutionSystem*************"""
                            'getDeviationFromPredictionforQQExec'               :   [2.64, 1.84, 0.22, -0.02, -1.05],
                            'getBuySellforQQExec'                               :   [-1.0, -1.0, -1.0, 1.0, 1.0],
                            'enterConditionforQQExec'                           :   [True, True, True, False, True],
                            'exitConditionforQQExec'                            :   [True, True, True, True, False],
                            #"""****** RESULTS FOR SimpleExecutionSystemWithFairValue*************"""                dict=dataSet["dict"]

                            'getDeviationFromPredictionforSimpleFairValueExec'  :   [0.16, 0.1, 0.78, 1.02, -0.0],
                            'getBuySellforforSimpleFairValueExec'               :   [-1.0, -1.0, -1.0, -1.0, -0.0],
                            'enterConditionforSimpleFairValueExec'              :   [True, True, True, True, False],
                            'exitConditionforSimpleFairValueExec'               :   [False, False, False, False, True],
                            'hackConditionforSimpleFairValueExec'               :   [False, False, False, False, False]}

                return {"dataSet":dataSet, "results":results, "parameters":parameters, "dict":dict}

            if c==2:
                dict["a"]=1
                dict["b"]=2
                dataSet = {"position":pd.DataFrame({'a':[1,2,3,4,5,6,7,8,9],'b':[9,8,7,6,5,4,3,2,1]},index =[pd.tslib.Timestamp('2017-01-03 09:30:30'),
                                                                                                             pd.tslib.Timestamp('2017-01-03 10:00:30'),
                                                                                                             pd.tslib.Timestamp('2017-01-03 10:30:30'),
                                                                                                             pd.tslib.Timestamp('2017-01-03 11:00:30'),
                                                                                                             pd.tslib.Timestamp('2017-01-03 11:30:30'),
                                                                                                             pd.tslib.Timestamp('2017-01-03 12:00:30'),
                                                                                                             pd.tslib.Timestamp('2017-01-03 12:30:30'),
                                                                                                             pd.tslib.Timestamp('2017-01-03 13:00:30'),
                                                                                                             pd.tslib.Timestamp('2017-01-03 13:30:30')]),
                          "prediction":         pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]}),
                          "df":                 pd.DataFrame({'a':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25],'b':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35]}),
                          "price":              pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]}),
                          "stockTopBidPrice":   pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]}),
                          "stockTopAskPrice":   pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]}),
                          "futureTopBidPrice":  pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]}),
                          "futureTopAskPrice":  pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]}),
                          "stockVWAP":          pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]}),
                          "enter_price":        pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]}),
                          "sdev":               pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]})
                          }

                parameters = {#"""*************** PARAMETERS FOR SimpleExecutionSystem ***********************""""
                              "enter_threshold":0.7, "exit_threshold":0.55, "longLimit":{'a':9,'b':9}, "shortLimit":{'a':9,'b':9},
                              "capitalUsageLimit":0, "enterlotSize":{'a':2,'b':2}, "exitlotSize":{'a':2,'b':2}, "limitType":'R', "priceforSimpleExec" : "close",
                              #"""*************** PARAMETERS FOR BasisExecutionSystem ***********************""""
                              "basisEnter_thresholdforBasisExec":0.5,"basisExit_thresholdforBasisExec":0.1,"basisLongLimit":5000,
                              "basisShortLimit":5000,"basisCapitalUsageLimit":0.05,"basisLotSize":100,"basisLimitType":'L',"basis_thresholdParam":'sdev',
                              "feeDict":0.0001,"feesRatio":1.5,"spreadLimit":0.1,"hackTime":time(15,25,0),
                              #"""*************** PARAMETERS FOR PairExecutionSystem ***********************""""
                              "pair":['a','b'], "pairRatio":0.3, "pairEnter_threshold":0.7, "pairExit_threshold":0.55, "pairLongLimit":10,
                              "pairShortLimit":10, "pairCapitalUsageLimit":0, "pairLotSize":1, "priceforPairExec":None,
                              #"""*************** PARAMETERS FOR QQExecutionSystem ***********************""""
                              "basisEnter_thresholdforQQExec":0.1,"basisExit_thresholdforQQExec":0.05,"priceforQQExec":'',"feeDictforQQExec":0.05,
                              #"""*************** PARAMETERS FOR SimpleFairvalue ***********************""""
                              "enter_threshold_deviation":0.07, "exit_threshold_deviation":0.05,
                              #"""*************** PARAMETERS FOR Ramdom ***********************"""
                              "count":1,"currentPrediction":0.0,"capital":-0.5,"closeAllPositions":False,"countforpairvalue":1
                              }

                results = { #"""****** RESULTS FOR SimpleExecutionSystem*************"""
                            'getPriceSeriesforSimpleExec'                       :   [2.35, 0.25],
                            'getLongLimitforSimpleExec'                         :   [3.0, 36.0],
                            'getShortLimitforSimpleExec'                        :   [3.0, 36.0],
                            'getEnterLotSizeforSimpleExec'                      :   [0.0, 8.0],
                            'getExitLotSizeforSimpleExec'                       :   [0.0, 8.0],
                            'convertLimitforSimpleExec'                         :   [[0.0, 0.0, 2.0, -2.0, 2.0, -3.0, 2.0, 0.0, 0.0], [12.0, 8.0, -21.0, 4.0, 34.0, -6.0, 0.0, 20.0, 9.0]],
                            'exitPositionforSimpleExec'                         :   [0, -1],
                            'enterPositionforSimpleExec'                        :   [0, 0],
                            'getBuySellforSimpleExec'                           :   [-1.0, 0.0],
                            'enterConditionforSimpleExec'                       :   [True, False],
                            'atPositionLimitforSimpleExec'                      :   [True, True],
                            'exitConditionforSimpleExec'                        :   [False, True],
                            'hackConditionforSimpleExec'                        :   [False,False],
                            #"""****** RESULTS FOR BasisExecutionSystem*************"""
                            'getDeviationFromPredictionforBasisExec'            :   [2.05, -0.25],
                            'getSpreadforBasisExec'                             :   [0.05, 0.05],
                            'getFeesforBasisExec'                               :   [0.000235, 2.5e-05],
                            'getBuySellforBasisExec'                            :   [-1.0, 1.0],
                            'enterConditionforBasisExec'                        :   [True, True],
                            'exitConditionforBasisExec'                         :   [False, False],
                            'hackConditionforBasisExec'                         :   [True, False],
                            #"""****** RESULTS FOR QQExecutionSystem*************"""
                            'getDeviationFromPredictionforQQExec'               :   [2.05, -0.25],
                            'getBuySellforQQExec'                               :   [-1.0, 1.0],
                            'enterConditionforQQExec'                           :   [True, True],
                            'exitConditionforQQExec'                            :   [True, False],
                            #"""****** RESULTS FOR SimpleExecutionSystemWithFairValue*************"""
                            'getDeviationFromPredictionforSimpleFairValueExec'  :   [0.13, 2.0],
                            'getBuySellforforSimpleFairValueExec'               :   [-1.0, -1.0],
                            'enterConditionforSimpleFairValueExec'              :   [True, True],
                            'exitConditionforSimpleFairValueExec'               :   [False, False],
                            'hackConditionforSimpleFairValueExec'               :   [False, False]}

                return {"dataSet":dataSet, "results":results, "parameters":parameters, "dict":dict}

            if c==3:

                dict["a"]=1

                dataSet = {"position":          pd.DataFrame({'a':[1,2,3,4,5]},index =[pd.tslib.Timestamp('2017-01-03 09:30:30'),
                                                                                       pd.tslib.Timestamp('2017-01-03 11:30:30'),
                                                                                       pd.tslib.Timestamp('2017-01-03 13:30:30'),
                                                                                       pd.tslib.Timestamp('2017-01-03 15:30:30'),
                                                                                       pd.tslib.Timestamp('2017-01-03 17:30:30')]),
                          "prediction":         pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5]}),
                          "df":                 pd.DataFrame({'a':[1.08,1.04,-3.03,-1.02,0.25]}),
                          "price":              pd.DataFrame({'a':[1.24,-2.05,-0.02,4.25,1.02]}),
                          "stockTopBidPrice":   pd.DataFrame({'a':[1.08,1.04,5.24,-3.03,5.12]}),
                          "stockTopAskPrice":   pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56]}),
                          "futureTopBidPrice":  pd.DataFrame({'a':[-3.04,-2.98,5.54,-1.82,-8.36]}),
                          "futureTopAskPrice":  pd.DataFrame({'a':[-1.68,-1.24,-6.24,3.33,-5.52]}),
                          "stockVWAP":          pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56]}),
                          "enter_price":        pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56]}),
                          "sdev":               pd.DataFrame({'a':[1.08,1.04,5.24,-3.03,5.12]})
                          }

                parameters = {#"""*************** PARAMETERS FOR SimpleExecutionSystem ***********************""""
                              "enter_threshold":0.7, "exit_threshold":0.55, "longLimit":10, "shortLimit":10,
                              "capitalUsageLimit":0, "enterlotSize":1.5, "exitlotSize":1.5, "limitType":'L', "priceforSimpleExec" : "close",
                              #"""*************** PARAMETERS FOR BasisExecutionSystem ***********************""""
                              "basisEnter_thresholdforBasisExec":0.5,"basisExit_thresholdforBasisExec":0.1,"basisLongLimit":5000,
                              "basisShortLimit":5000,"basisCapitalUsageLimit":0.05,"basisLotSize":100,"basisLimitType":'L',"basis_thresholdParam":'sdev',
                              "feeDict":0.0001,"feesRatio":1.5,"spreadLimit":0.1,"hackTime":time(15,25,0),
                              #"""*************** PARAMETERS FOR PairExecutionSystem ***********************""""
                              "pair":['a','b'], "pairRatio":20, "pairEnter_threshold":0.7, "pairExit_threshold":0.55, "pairLongLimit":10,
                              "pairShortLimit":10, "pairCapitalUsageLimit":0, "pairLotSize":1, "priceforPairExec":None,
                              #"""*************** PARAMETERS FOR QQExecutionSystem ***********************""""
                              "basisEnter_thresholdforQQExec":0.1,"basisExit_thresholdforQQExec":0.05,"priceforQQExec":'',"feeDictforQQExec":0.05,
                              #"""*************** PARAMETERS FOR SimpleFairvalue ***********************""""
                              "enter_threshold_deviation":0.07, "exit_threshold_deviation":0.05,
                              #"""*************** PARAMETERS FOR Ramdom ***********************"""
                              "count":1,"currentPrediction":1.0,"capital":0.5,"closeAllPositions":True,"countforpairvalue":0
                              }

                results = { #"""****** RESULTS FOR SimpleExecutionSystem*************"""
                            'getPriceSeriesforSimpleExec'                       :   [1.02],
                            'getLongLimitforSimpleExec'                         :   [10.0],
                            'getShortLimitforSimpleExec'                        :   [10.0],
                            'getEnterLotSizeforSimpleExec'                      :   [1.5],
                            'getExitLotSizeforSimpleExec'                       :   [1.5],
                            'convertLimitforSimpleExec'                         :   [[1.08, 1.04, -3.03, -1.02, 0.25]],
                            'exitPositionforSimpleExec'                         :   [-5],
                            'enterPositionforSimpleExec'                        :   [0],
                            'getBuySellforSimpleExec'                           :   [0.0],
                            'enterConditionforSimpleExec'                       :   [False],
                            'atPositionLimitforSimpleExec'                      :   [False],
                            'exitConditionforSimpleExec'                        :   [True],
                            'hackConditionforSimpleExec'                        :   [False],
                            #"""****** RESULTS FOR BasisExecutionSystem*************"""
                            'getDeviationFromPredictionforBasisExec'            :   [0.52],
                            'getSpreadforBasisExec'                             :   [1.57],
                            'getFeesforBasisExec'                               :   [0.000856],
                            'getBuySellforBasisExec'                            :   [-1.0],
                            'enterConditionforBasisExec'                        :   [False],
                            'exitConditionforBasisExec'                         :   [False],
                            'hackConditionforBasisExec'                         :   [True],
                            #"""****** RESULTS FOR QQExecutionSystem*************"""
                            'getDeviationFromPredictionforQQExec'               :   [0.52],
                            'getBuySellforQQExec'                               :   [-1.0],
                            'enterConditionforQQExec'                           :   [False],
                            'exitConditionforQQExec'                            :   [True],
                            #"""****** RESULTS FOR SimpleExecutionSystemWithFairValue*************"""
                            'getDeviationFromPredictionforSimpleFairValueExec'  :   [0.49],
                            'getBuySellforforSimpleFairValueExec'               :   [-1.0],
                            'enterConditionforSimpleFairValueExec'              :   [True],
                            'exitConditionforSimpleFairValueExec'               :   [False],
                            'hackConditionforSimpleFairValueExec'               :   [False]}

                return {"dataSet":dataSet, "results":results, "parameters":parameters, "dict":dict}

            if c==4:

                dict["a"]=1
                dict["b"]=2
                dict["c"]=3

                dataSet = {"position":          pd.DataFrame({'a':[1,2,3,4,5],'b':[1,2,3,4,5],'c':[1,2,3,4,5]},index =[pd.tslib.Timestamp('2017-01-03 09:30:30'),
                                                                                                                       pd.tslib.Timestamp('2017-01-03 10:00:30'),
                                                                                                                       pd.tslib.Timestamp('2017-01-03 10:30:30'),
                                                                                                                       pd.tslib.Timestamp('2017-01-03 11:00:30'),
                                                                                                                       pd.tslib.Timestamp('2017-01-03 11:30:30')]),
                          "prediction":         pd.DataFrame({'a':[0.5,0.55,0.6,0.7,0.3],'b':[0.7,0.9,0.9,0.1,0.5],'c':[0.2,0.5,1.0,0.7,0.6]}),
                          "df":                 pd.DataFrame({'a':[1.08,1.04,-3.03,-1.02,0.25],'b':[1.24,-2.05,-0.02,4.25,1.02],'c':[3.14,2.02,-1.02,3.21,0.82]}),
                          "price":              pd.DataFrame({'a':[1.24,-2.05,-0.02,4.25,1.02],'b':[1.08,1.04,-3.03,-1.02,0.25],'c':[2.14,-1.46,2.56,-4.03,1.02]}),
                          "stockTopBidPrice":   pd.DataFrame({'a':[0.5,0.55,0.6,0.7,0.3],'b':[1.08,1.04,-3.03,-1.02,0.25],'c':[2.14,-1.46,2.56,-4.03,1.02]}),
                          "stockTopAskPrice":   pd.DataFrame({'a':[1.5,-2.55,1.6,1.7,-1.3],'b':[-1.08,-1.04,3.03,1.02,-0.25],'c':[-2.14,1.46,-2.56,4.03,-0.02]}),
                          "futureTopBidPrice":  pd.DataFrame({'a':[0.5,0.55,0.6,0.7,0.3],'b':[1.08,1.04,-3.03,-1.02,0.25],'c':[2.14,-1.46,2.56,-4.03,1.02]}),
                          "futureTopAskPrice":  pd.DataFrame({'a':[1.5,-2.55,1.6,1.7,-1.3],'b':[-1.08,-1.04,3.03,1.02,-0.25],'c':[-2.14,1.46,-2.56,4.03,-0.02]}),
                          "stockVWAP":          pd.DataFrame({'a':[0.5,0.55,0.6,0.7,0.3],'b':[1.08,1.04,-3.03,-1.02,0.25],'c':[2.14,-1.46,2.56,-4.03,1.02]}),
                          "enter_price":        pd.DataFrame({'a':[0.5,0.55,0.6,0.7,0.3],'b':[1.5,-2.55,1.6,1.7,-1.3],'c':[1.08,1.04,-3.03,-1.02,0.25]}),
                          "sdev":               pd.DataFrame({'a':[1.5,-2.55,1.6,1.7,-1.3],'b':[-1.08,-1.04,3.03,1.02,-0.60],'c':[-2.14,1.46,-2.56,4.03,-1.20]})
                          }

                parameters = {#"""*************** PARAMETERS FOR SimpleExecutionSystem ***********************""""
                              "enter_threshold":0.7, "exit_threshold":0.55, "longLimit":9.5, "shortLimit":9.5,
                              "capitalUsageLimit":0, "enterlotSize":0.9, "exitlotSize":0.9, "limitType":'R', "priceforSimpleExec" : "close",
                              #"""*************** PARAMETERS FOR BasisExecutionSystem ***********************""""
                              "basisEnter_thresholdforBasisExec":0.5,"basisExit_thresholdforBasisExec":0.1,"basisLongLimit":5000,
                              "basisShortLimit":5000,"basisCapitalUsageLimit":0.05,"basisLotSize":100,"basisLimitType":'L',"basis_thresholdParam":'sdev',
                              "feeDict":0.0001,"feesRatio":1.5,"spreadLimit":0.1,"hackTime":time(15,25,0),
                              #"""*************** PARAMETERS FOR PairExecutionSystem ***********************""""
                              "pair":['a','b'], "pairRatio":10, "pairEnter_threshold":0.7, "pairExit_threshold":0.55, "pairLongLimit":10,
                              "pairShortLimit":10, "pairCapitalUsageLimit":0, "pairLotSize":1, "priceforPairExec":None,
                              #"""*************** PARAMETERS FOR QQExecutionSystem ***********************""""
                              "basisEnter_thresholdforQQExec":0.1,"basisExit_thresholdforQQExec":0.05,"priceforQQExec":'',"feeDictforQQExec":0.05,
                              #"""*************** PARAMETERS FOR SimpleFairvalue ***********************""""
                              "enter_threshold_deviation":0.07, "exit_threshold_deviation":0.05,
                              #"""*************** PARAMETERS FOR Ramdom ***********************"""
                              "count":1,"currentPrediction":1.0,"capital":0.6,"closeAllPositions":False,"countforpairvalue":2
                              }

                results = { #"""****** RESULTS FOR SimpleExecutionSystem*************"""
                            'getPriceSeriesforSimpleExec'                       :   [1.02, 0.25, 1.02],
                            'getLongLimitforSimpleExec'                         :   [9.0, 38.0, 9.0],
                            'getShortLimitforSimpleExec'                        :   [9.0, 38.0, 9.0],
                            'getEnterLotSizeforSimpleExec'                      :   [0.0, 3.0, 0.0],
                            'getExitLotSizeforSimpleExec'                       :   [0.0, 3.0, 0.0],
                            'convertLimitforSimpleExec'                         :   [[1.0, 1.0, -3.0, -1.0, 0.0], [4.0, -9.0, -1.0, 17.0, 4.0], [3.0, 1.0, -1.0, 3.0, 0.0]],
                            'exitPositionforSimpleExec'                         :   [0, -3, 0],
                            'enterPositionforSimpleExec'                        :   [0, 0, 0],
                            'getBuySellforSimpleExec'                           :   [-1.0, 0.0, 1.0],
                            'enterConditionforSimpleExec'                       :   [True, False, False],
                            'atPositionLimitforSimpleExec'                      :   [False, False, False],
                            'exitConditionforSimpleExec'                        :   [False, True, False],
                            'hackConditionforSimpleExec'                        :   [False,False,False],
                            #"""****** RESULTS FOR BasisExecutionSystem*************"""
                            'getDeviationFromPredictionforBasisExec'            :   [0.72, -0.25, 0.42],
                            'getSpreadforBasisExec'                             :   [0.05, 0.05, 0.05],
                            'getFeesforBasisExec'                               :   [3e-05, 2.5e-05, 0.000102],
                            'getBuySellforBasisExec'                            :   [-1.0, 1.0, -1.0],
                            'enterConditionforBasisExec'                        :   [True, False, False],
                            'exitConditionforBasisExec'                         :   [True, True, False],
                            'hackConditionforBasisExec'                         :   [False, False, False],
                            #"""****** RESULTS FOR QQExecutionSystem*************"""
                            'getDeviationFromPredictionforQQExec'               :   [0.72, -0.25, 0.42],
                            'getBuySellforQQExec'                               :   [-1.0, 1.0, -1.0],
                            'enterConditionforQQExec'                           :   [True, True, True],
                            'exitConditionforQQExec'                            :   [True, False, True],
                            #"""****** RESULTS FOR SimpleExecutionSystemWithFairValue*************"""
                            'getDeviationFromPredictionforSimpleFairValueExec'  :   [0.29, 2.0, 0.59],
                            'getBuySellforforSimpleFairValueExec'               :   [-1.0, -1.0, -1.0],
                            'enterConditionforSimpleFairValueExec'              :   [True, True, True],
                            'exitConditionforSimpleFairValueExec'               :   [False, False, False],
                            'hackConditionforSimpleFairValueExec'               :   [False, False, False]}

                return {"dataSet":dataSet, "results":results, "parameters":parameters, "dict":dict}

            if c==5:

                dict["a"]=1
                dict["b"]=2

                dataSet = {"position":          pd.DataFrame({'a':[1,2,3,4],'b':[1,2,3,4]},index =[pd.tslib.Timestamp('2017-01-03 09:30:30'),
                                                                                                              pd.tslib.Timestamp('2017-01-03 10:00:30'),
                                                                                                              pd.tslib.Timestamp('2017-01-03 10:30:30'),
                                                                                                              pd.tslib.Timestamp('2017-01-03 11:30:30')]),
                          "prediction":         pd.DataFrame({'a':[0.2,0.01,0.8,0.9],'b':[0.1,0.8,0.6,0.4]}),
                          "df":                 pd.DataFrame({'a':[1.02,2.05,4.02,0.09],'b':[1.08,1.04,5.24,-3.03]}),
                          "price":              pd.DataFrame({'a':[1.02,2.05,4.02,0.09],'b':[1.08,1.04,5.24,-3.03]}),
                          "stockTopBidPrice":   pd.DataFrame({'a':[1.02,2.05,4.02,0.09],'b':[1.08,1.04,5.24,-3.03]}),
                          "stockTopAskPrice":   pd.DataFrame({'a':[1.02,2.05,4.02,0.09],'b':[1.08,1.04,5.24,-3.03]}),
                          "futureTopBidPrice":  pd.DataFrame({'a':[1.02,2.05,4.02,0.09],'b':[1.08,1.04,5.24,-3.03]}),
                          "futureTopAskPrice":  pd.DataFrame({'a':[1.02,2.05,4.02,0.09],'b':[1.08,1.04,5.24,-3.03]}),
                          "stockVWAP":          pd.DataFrame({'a':[1.02,2.05,4.02,0.09],'b':[1.08,1.04,5.24,-3.03]}),
                          "enter_price":        pd.DataFrame({'a':[1.08,1.04,5.24,-3.03],'b':[1.02,2.05,4.02,0.09]}),
                          "sdev":               pd.DataFrame({'a':[1.02,2.05,4.02,0.09],'b':[1.08,1.04,5.24,-3.03]})
                          }

                parameters = {#"""*************** PARAMETERS FOR SimpleExecutionSystem ***********************""""
                              "enter_threshold":0.7, "exit_threshold":0.55, "longLimit":pd.DataFrame({'a':[9.9],'b':[9.9]}), "shortLimit":pd.DataFrame({0:[9.9,9.9]},index=['a','b']),
                              "capitalUsageLimit":0, "enterlotSize":pd.DataFrame({'a':[0],'b':[0]}), "exitlotSize":pd.DataFrame({0:[0,0]},index=['a','b']), "limitType":'R', "priceforSimpleExec" : "close",
                              #"""*************** PARAMETERS FOR BasisExecutionSystem ***********************""""
                              "basisEnter_thresholdforBasisExec":0.5,"basisExit_thresholdforBasisExec":0.1,"basisLongLimit":5000,
                              "basisShortLimit":5000,"basisCapitalUsageLimit":0.05,"basisLotSize":100,"basisLimitType":'L',"basis_thresholdParam":'sdev',
                              "feeDict":0.0001,"feesRatio":1.5,"spreadLimit":0.1,"hackTime":time(15,25,0),
                              #"""*************** PARAMETERS FOR PairExecutionSystem ***********************""""
                              "pair":['a','b'], "pairRatio":0.3, "pairEnter_threshold":0.7, "pairExit_threshold":0.55, "pairLongLimit":10,
                              "pairShortLimit":10, "pairCapitalUsageLimit":0, "pairLotSize":1, "priceforPairExec":None,
                              #"""*************** PARAMETERS FOR QQExecutionSystem ***********************""""
                              "basisEnter_thresholdforQQExec":0.1,"basisExit_thresholdforQQExec":0.05,"priceforQQExec":'',"feeDictforQQExec":0.05,
                              #"""*************** PARAMETERS FOR SimpleFairvalue ***********************""""
                              "enter_threshold_deviation":0.07, "exit_threshold_deviation":0.05,
                              #"""*************** PARAMETERS FOR Ramdom ***********************"""
                              "count":0,"currentPrediction":0.5,"capital":0.5,"closeAllPositions":True,"countforpairvalue":1
                              }

                results = { #"""****** RESULTS FOR SimpleExecutionSystem*************"""
                            'getPriceSeriesforSimpleExec'                       :   [0.09, -3.03],
                            'getLongLimitforSimpleExec'                         :   [110.0, -4.0],
                            'getShortLimitforSimpleExec'                        :   [110.0, -4.0],
                            'getEnterLotSizeforSimpleExec'                      :   [0.0, -0.0],
                            'getExitLotSizeforSimpleExec'                       :   [0.0, -0.0],
                            'convertLimitforSimpleExec'                         :   [[11.0, 22.0, 44.0, 1.0], [-1.0, -1.0, -2.0, 1.0]],
                            'exitPositionforSimpleExec'                         :   [-4, -4],
                            'enterPositionforSimpleExec'                        :   [0, 0],
                            'getBuySellforSimpleExec'                           :   [1.0, -1.0],
                            'enterConditionforSimpleExec'                       :   [True, False],
                            'atPositionLimitforSimpleExec'                      :   [False, True],
                            'exitConditionforSimpleExec'                        :   [False, False],
                            'hackConditionforSimpleExec'                        :   [False,False],
                            #"""****** RESULTS FOR BasisExecutionSystem*************"""
                            'getDeviationFromPredictionforBasisExec'            :   [-0.81, -3.43],
                            'getSpreadforBasisExec'                             :   [0.05, 0.05],
                            'getFeesforBasisExec'                               :   [9e-06, -0.000303],
                            'getBuySellforBasisExec'                            :   [1.0, 1.0],
                            'enterConditionforBasisExec'                        :   [True, True],
                            'exitConditionforBasisExec'                         :   [True, False],
                            'hackConditionforBasisExec'                         :   [False, False],
                            #"""****** RESULTS FOR QQExecutionSystem*************"""
                            'getDeviationFromPredictionforQQExec'               :   [-0.81, -3.43],
                            'getBuySellforQQExec'                               :   [1.0, 1.0],
                            'enterConditionforQQExec'                           :   [True, True],
                            'exitConditionforQQExec'                            :   [False, False],
                            #"""****** RESULTS FOR SimpleExecutionSystemWithFairValue*************"""
                            'getDeviationFromPredictionforSimpleFairValueExec'  :   [10.0, -0.13],
                            'getBuySellforforSimpleFairValueExec'               :   [-1.0, 1.0],
                            'enterConditionforSimpleFairValueExec'              :   [True, True],
                            'exitConditionforSimpleFairValueExec'               :   [False, False],
                            'hackConditionforSimpleFairValueExec'               :   [False, False]}

                return {"dataSet":dataSet, "results":results, "parameters":parameters, "dict":dict}
