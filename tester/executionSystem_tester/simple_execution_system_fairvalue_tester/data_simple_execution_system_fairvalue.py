import pandas as pd
import numpy as np
from collections import OrderedDict
from datetime import datetime, time, timedelta

def data_simple_execution_system_fairvalue(c):
    dataSet={}
    parameters={}
    results={}

    if c==0:
######## providing empty DataFrames as the mock data
######## logging IndexErrors
        dataSet["price"]=pd.DataFrame()
        dataSet["prediction"]=pd.DataFrame()
        ###################################################
        parameters["enter_threshold_deviation"]=0.07
        parameters["exit_threshold_deviation"]=0.05
        parameters["longLimit"]=10
        parameters["shortLimit"]=10
        parameters["capitalUsageLimit"]=0
        parameters["enterlotSize"]=1
        parameters["exitlotSize"]=1
        parameters["limitType"]='L'
        parameters["price"]="close"
        ###################################################
        results["getDeviationFromPrediction"]=None
        results["getBuySell"]=None
        results["enterCondition"]=None
        results["exitCondition"]=None
        results["hackCondition"]=pd.Series()
        results["hackCondition"]=results["hackCondition"].astype('bool')

    if c==1:
######## the feature keys are wrong for c==1
######## logging KeyErrors
        dataSet["priced"]=pd.DataFrame()
        dataSet["prediction"]=pd.DataFrame()
        ###################################################
        parameters["enter_threshold_deviation"]=0.07
        parameters["exit_threshold_deviation"]=0.05
        parameters["longLimit"]=10
        parameters["shortLimit"]=10
        parameters["capitalUsageLimit"]=0
        parameters["enterlotSize"]=1
        parameters["exitlotSize"]=1
        parameters["limitType"]='L'
        parameters["price"]="close"
        ###################################################
        results["getDeviationFromPrediction"]=None
        results["getBuySell"]=None
        results["enterCondition"]=None
        results["exitCondition"]=None
        results["hackCondition"]=pd.Series()
        results["hackCondition"]=results["hackCondition"].astype('bool')

#### testing sample data for c==2 and c==3
    if c==2:
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30')]
        dataSet["price"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.5],'b':[0.2],'c':[0.8],'d':[1.0],'e':[0.0]},index =indexlist)
        ###################################################
        parameters["enter_threshold_deviation"]=0.07
        parameters["exit_threshold_deviation"]=0.05
        parameters["longLimit"]=10
        parameters["shortLimit"]=10
        parameters["capitalUsageLimit"]=0
        parameters["enterlotSize"]=1
        parameters["exitlotSize"]=1
        parameters["limitType"]='L'
        parameters["price"]="close"
        ###################################################
        seriesname=pd.tslib.Timestamp('2017-01-03 09:30:30')
        results["getDeviationFromPrediction"]=pd.Series({'a':0.16,'b':0.1,'c':0.78,'d':1.02,'e':-0.0},name=seriesname)
        results["getBuySell"]=pd.Series({'a':-1.0, 'b':-1.0, 'c':-1.0, 'd':-1.0, 'e':-0.0},name=seriesname)
        results["enterCondition"]=pd.Series({'a':True, 'b':True, 'c':True, 'd':True, 'e':False},name=seriesname)
        results["exitCondition"]=pd.Series({'a':False, 'b':False, 'c':False, 'd':False, 'e':True},name=seriesname)
        results["hackCondition"]=pd.Series({'a':False, 'b':False, 'c':False, 'd':False, 'e':False},name=seriesname)

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
        dataSet["price"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        ###################################################
        parameters["enter_threshold_deviation"]=0.07
        parameters["exit_threshold_deviation"]=0.05
        parameters["longLimit"]=10
        parameters["shortLimit"]=10
        parameters["capitalUsageLimit"]=0
        parameters["enterlotSize"]=1
        parameters["exitlotSize"]=1
        parameters["limitType"]='L'
        parameters["price"]="close"
        ###################################################
        seriesname=pd.tslib.Timestamp('2017-01-03 13:30:30')
        results["getDeviationFromPrediction"]=pd.Series({'a':0.13,'b':2.0},name=seriesname)
        results["getBuySell"]=pd.Series({'a':-1.0, 'b':-1.0},name=seriesname)
        results["enterCondition"]=pd.Series({'a':True, 'b':True},name=seriesname)
        results["exitCondition"]=pd.Series({'a':False, 'b':False},name=seriesname)
        results["hackCondition"]=pd.Series({'a':False, 'b':False},name=seriesname)

    return {"dataSet":dataSet,"parameters":parameters,"results":results}
