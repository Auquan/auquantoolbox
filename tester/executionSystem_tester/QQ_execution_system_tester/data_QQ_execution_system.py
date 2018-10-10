import pandas as pd
import numpy as np
from collections import OrderedDict
from datetime import datetime, time, timedelta

def data_QQ_execution_system(c):
    dataSet={}
    parameters={}
    results={}
    if c==0:
######## providing empty DataFrames as the mock data
######## logging IndexErrors
        dataSet["position"]=pd.DataFrame()
        dataSet["price"]=pd.DataFrame()
        dataSet["sdev"]=pd.DataFrame()
        dataSet["prediction"]=pd.DataFrame()
        ###################################################
        parameters["basisEnter_threshold"]=0.1
        parameters["basisExit_threshold"]=0.05
        parameters["basisLongLimit"]=5000
        parameters["basisShortLimit"]=5000
        parameters["basisCapitalUsageLimit"]=0.05
        parameters["basisLotSize"]=100
        parameters["basisLimitType"]='L'
        parameters["basis_thresholdParam"]='sdev'
        parameters["price"]="close"
        parameters["feeDict"]=0.05
        ###################################################
        results["getDeviationFromPrediction"]=None
        results["getBuySell"]=None
        results["enterCondition"]=None
        results["exitCondition"]=None

    if c==1:
        dataSet["position"]=pd.DataFrame()
        dataSet["price"]=pd.DataFrame()
        dataSet["prediction"]=pd.DataFrame()
######## the feature keys are wrong for c==1
######## logging KeyErrors
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
        ###################################################
        results["getDeviationFromPrediction"]=None
        results["getBuySell"]=None
        results["enterCondition"]=None
        results["exitCondition"]=None

#### testing for sample data for c==2 and c==3
    if c==2:
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1],'b':[2],'c':[3],'d':[4],'e':[5]},index =indexlist)
        dataSet["price"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        dataSet["sdev"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[0.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.5],'b':[0.2],'c':[0.8],'d':[1.0],'e':[0.0]},index =indexlist)
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
        ###################################################
        seriesname=pd.tslib.Timestamp('2017-01-03 09:30:30')
        results["getDeviationFromPrediction"]=pd.Series({'a':2.64,'b':1.84,'c':0.22,'d':-0.02,'e':-1.05},name=seriesname)
        results["getBuySell"]=pd.Series({'a':-1.0, 'b':-1.0, 'c':-1.0, 'd':1.0, 'e':1.0},name=seriesname)
        results["enterCondition"]=pd.Series({'a':True, 'b':True, 'c':True, 'd':False, 'e':True},name=seriesname)
        results["exitCondition"]=pd.Series({'a':True, 'b':True, 'c':True, 'd':True, 'e':False},name=seriesname)

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
        dataSet["price"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["sdev"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
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
        ###################################################
        seriesname=pd.tslib.Timestamp('2017-01-03 13:30:30')
        results["getDeviationFromPrediction"]=pd.Series({'a':2.05,'b':-0.25},name=seriesname)
        results["getBuySell"]=pd.Series({'a':-1.0, 'b':1.0},name=seriesname)
        results["enterCondition"]=pd.Series({'a':True, 'b':True},name=seriesname)
        results["exitCondition"]=pd.Series({'a':True, 'b':False},name=seriesname)

    return {"dataSet":dataSet,"parameters":parameters,"results":results}
