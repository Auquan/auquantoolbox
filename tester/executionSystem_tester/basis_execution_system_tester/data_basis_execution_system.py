import pandas as pd
import numpy as np
from collections import OrderedDict
from datetime import datetime, time, timedelta

def data_basis_execution_system(c):
    dataSet={}
    parameters={}
    results={}

    if c==0:
######## providing empty DataFrames as the mock data
######## logging IndexErrors
        dataSet["position"]=pd.DataFrame()
        dataSet["prediction"]=pd.DataFrame()
        dataSet["price"]=pd.DataFrame()
        dataSet["stockTopBidPrice"]=pd.DataFrame()
        dataSet["stockTopAskPrice"]=pd.DataFrame()
        dataSet["futureTopBidPrice"]=pd.DataFrame()
        dataSet["futureTopAskPrice"]=pd.DataFrame()
        dataSet["stockVWAP"]=pd.DataFrame()
        dataSet["enter_price"]=pd.DataFrame()
        dataSet["sdev"]=pd.DataFrame()
        ###################################################
        parameters["basisEnter_threshold"]=0.5
        parameters["basisExit_threshold"]=0.1
        parameters["basisLongLimit"]=5000
        parameters["basisShortLimit"]=5000
        parameters["basisCapitalUsageLimit"]=0.05
        parameters["basisLotSize"]=100
        parameters["basisLimitType"]='L'
        parameters["basis_thresholdParam"]='sdev'
        parameters["price"]="close"
        parameters["feeDict"]=0.0001
        parameters["feesRatio"]=1.5
        parameters["spreadLimit"]=0.1
        parameters["hackTime"]=time(15,25,0)
        ###################################################
        # extra parameters
        parameters["getCurrentPosition"]=[]
        ###################################################
######### results are None as the dataSets are empty
######### logError displayed
        results["getDeviationFromPrediction"]=None
        results["getSpread"]=None
        results["getFees"]=None
        results["getBuySell"]=None
        results["enterCondition"]=None
        results["exitCondition"]=None
        results["hackCondition"]=None
        ###################################################
        # extra dataSets
        dict=OrderedDict()
        dataSet["dict"]=dict

    if c==1:
        dataSet["position"]=pd.DataFrame()
        dataSet["prediction"]=pd.DataFrame()
        dataSet["enter_price"]=pd.DataFrame()
######## the feature keys are wrong for c==2
######## logging KeyErrors
        dataSet["priced"]=pd.DataFrame()
        dataSet["stockTopBidPriced"]=pd.DataFrame()
        dataSet["stockTopAskPriced"]=pd.DataFrame()
        dataSet["futureTopBidPriced"]=pd.DataFrame()
        dataSet["futureTopAskPriced"]=pd.DataFrame()
        dataSet["stockVWAPed"]=pd.DataFrame()
        dataSet["sdeved"]=pd.DataFrame()
        ###################################################
        parameters["basisEnter_threshold"]=0.5
        parameters["basisExit_threshold"]=0.1
        parameters["basisLongLimit"]=5000
        parameters["basisShortLimit"]=5000
        parameters["basisCapitalUsageLimit"]=0.05
        parameters["basisLotSize"]=100
        parameters["basisLimitType"]='L'
        parameters["basis_thresholdParam"]='sdev'
        parameters["price"]="close"
        parameters["feeDict"]=0.0001
        parameters["feesRatio"]=1.5
        parameters["spreadLimit"]=0.1
        parameters["hackTime"]=time(15,25,0)
        ###################################################
        parameters["getCurrentPosition"]=[]
        ###################################################
######### results are None as the dataSets are empty
######### logError displayed
        results["getDeviationFromPrediction"]=None
        results["getSpread"]=None
        results["getFees"]=None
        results["getBuySell"]=None
        results["enterCondition"]=None
        results["exitCondition"]=None
        results["hackCondition"]=None
        ###################################################
        dict=OrderedDict()
        dataSet["dict"]=dict

#### testing sample data for c==2 and c==3

    if c==2:
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1],'b':[2],'c':[3],'d':[4],'e':[5]},index =indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.5],'b':[0.2],'c':[0.8],'d':[1.0],'e':[0.0]},index =indexlist)
        dataSet["price"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        dataSet["stockTopBidPrice"]=pd.DataFrame({'a':[-1.24],'b':[-2.02],'c':[-3.14],'d':[-4.24],'e':[-5.96]},index =indexlist)
        dataSet["stockTopAskPrice"]=pd.DataFrame({'a':[1.24],'b':[2.02],'c':[3.14],'d':[4.24],'e':[5.96]},index =indexlist)
        dataSet["futureTopAskPrice"]=pd.DataFrame({'a':[1.24],'b':[2.02],'c':[3.14],'d':[4.24],'e':[5.96]},index =indexlist)
        dataSet["futureTopBidPrice"]=pd.DataFrame({'a':[-1.24],'b':[-2.02],'c':[-3.14],'d':[-4.24],'e':[-5.96]},index =indexlist)
        dataSet["stockVWAP"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        dataSet["enter_price"]=pd.DataFrame({'a':[1.24],'b':[2.02],'c':[3.14],'d':[4.24],'e':[5.96]},index =indexlist)
        dataSet["sdev"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[0.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        ###################################################
        parameters["basisEnter_threshold"]=0.5
        parameters["basisExit_threshold"]=0.1
        parameters["basisLongLimit"]=5000
        parameters["basisShortLimit"]=5000
        parameters["basisCapitalUsageLimit"]=0.05
        parameters["basisLotSize"]=100
        parameters["basisLimitType"]='L'
        parameters["basis_thresholdParam"]='sdev'
        parameters["price"]="close"
        parameters["feeDict"]=0.0001
        parameters["feesRatio"]=1.5
        parameters["spreadLimit"]=0.1
        parameters["hackTime"]=time(15,25,0)
        ###################################################
        parameters["getCurrentPosition"]=[2,3,0,2,0]
        ###################################################
        seriesname=pd.tslib.Timestamp('2017-01-03 09:30:30')
        results["getDeviationFromPrediction"]=pd.Series({'a':2.64,'b':1.84,'c':0.22,'d':-0.02,'e':-1.05},name=seriesname)
        results["getSpread"]=pd.Series({'a':1.24,'b':2.02,'c':3.14,'d':4.24,'e':5.96},name=seriesname)
        results["getFees"]=pd.Series({'a':0.000314, 'b':0.000204, 'c':0.000102, 'd':9.8e-05, 'e':-0.000105},name=seriesname)
        results["getBuySell"]=pd.Series({'a':-1.0, 'b':-1.0, 'c':-1.0, 'd':1.0, 'e':1.0},name=seriesname)
        results["enterCondition"]=pd.Series({'a':True, 'b':True, 'c':False, 'd':False, 'e':True},name=seriesname)
        results["exitCondition"]=pd.Series({'a':True, 'b':False, 'c':False, 'd':False, 'e':False},name=seriesname)
        results["hackCondition"]=pd.Series({'a':True, 'b':True, 'c':False, 'd':True, 'e':False},name=seriesname)
        ###################################################
        dict=OrderedDict()
        dict["a"]=1
        dict["b"]=2
        dict["c"]=3
        dict["d"]=4
        dict["e"]=5
        dataSet["dict"]=dict

    if c==3:
        indexlist=  [pd.tslib.Timestamp('2017-01-03 09:30:30'),
                     pd.tslib.Timestamp('2017-01-03 10:00:30'),
                     pd.tslib.Timestamp('2017-01-03 10:30:30'),
                     pd.tslib.Timestamp('2017-01-03 11:00:30'),
                     pd.tslib.Timestamp('2017-01-03 11:30:30'),
                     pd.tslib.Timestamp('2017-01-03 12:00:30'),
                     pd.tslib.Timestamp('2017-01-03 12:30:30'),
                     pd.tslib.Timestamp('2017-01-03 13:00:30'),
                     pd.tslib.Timestamp('2017-01-03 13:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1,2,3,4,5,6,7,8,9],'b':[9,8,7,6,5,4,3,2,1]},index=indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        dataSet["price"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["stockTopBidPrice"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["stockTopAskPrice"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["futureTopBidPrice"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["futureTopAskPrice"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["stockVWAP"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["enter_price"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["sdev"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        ###################################################
        parameters["basisEnter_threshold"]=0.5
        parameters["basisExit_threshold"]=0.1
        parameters["basisLongLimit"]=5000
        parameters["basisShortLimit"]=5000
        parameters["basisCapitalUsageLimit"]=0.05
        parameters["basisLotSize"]=100
        parameters["basisLimitType"]='L'
        parameters["basis_thresholdParam"]='sdev'
        parameters["price"]="close"
        parameters["feeDict"]=0.0001
        parameters["feesRatio"]=1.5
        parameters["spreadLimit"]=0.1
        parameters["hackTime"]=time(15,25,0)
        ###################################################
        parameters["getCurrentPosition"]=[2,3,0,2,0]
        ###################################################
        seriesname=pd.tslib.Timestamp('2017-01-03 13:30:30')
        results["getDeviationFromPrediction"]=pd.Series({'a':2.05,'b':-0.25},name=seriesname)
        results["getSpread"]=pd.Series({'a':0.05,'b':0.05},name=seriesname)
        results["getFees"]=pd.Series({'a':0.000235, 'b':2.5e-05},name=seriesname)
        results["getBuySell"]=pd.Series({'a':-1.0, 'b':1.0},name=seriesname)
        results["enterCondition"]=pd.Series({'a':True, 'b':True},name=seriesname)
        results["exitCondition"]=pd.Series({'a':False, 'b':False},name=seriesname)
        results["hackCondition"]=pd.Series({'a':True, 'b':False},name=seriesname)
        ###################################################
        dict=OrderedDict()
        dict["a"]=1
        dict["b"]=2
        dataSet["dict"]=dict

    return {"dataSet":dataSet,"parameters":parameters,"results":results}
