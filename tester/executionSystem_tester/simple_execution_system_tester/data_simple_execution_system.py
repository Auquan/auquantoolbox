import pandas as pd
import numpy as np
from collections import OrderedDict
from datetime import datetime, time, timedelta

def data_simple_execution_system(c):
    dataSet={}
    parameters={}
    results={}

    if c==0:
######## providing empty DataFrames as the mock data
######## logging IndexErrors
        dataSet["position"]=pd.DataFrame()
        dataSet["prediction"]=pd.DataFrame()
        dataSet["price"]=pd.DataFrame()
        ###################################################
        parameters["enter_threshold"]=0.7
        parameters["exit_threshold"]=0.55
        parameters["longLimit"]=10
        parameters["shortLimit"]=10
        parameters["capitalUsageLimit"]=0
        parameters["enterlotSize"]=1
        parameters["exitlotSize"]=1
        parameters["limitType"]='L'
        parameters["price"]="close"
        ###################################################
        parameters["convertLimitdf"]=pd.Series()
        parameters["time"]="01/01/2010"
        parameters["executions"]=pd.Series()
        parameters["capital"]=0.1
        parameters["closeAllPositions"]=False
        parameters["priceSeries"]=pd.Series()
        ###################################################
        results["getPriceSeries"]=None
        results["getLongLimit"]=pd.Series()
        results["getLongLimit"]=results["getLongLimit"].astype('int64')
        results["getShortLimit"]=pd.Series()
        results["getShortLimit"]=results["getShortLimit"].astype('int64')
        results["getEnterLotSize"]=pd.Series()
        results["getEnterLotSize"]=results["getEnterLotSize"].astype('int64')
        results["getExitLotSize"]=pd.Series()
        results["getExitLotSize"]=results["getExitLotSize"].astype('int64')
        results["convertLimit"]=pd.Series()
        results["getInstrumentExecutionsFromExecutions"]=[]
        results["getExecutions"]=None
        results["getExecutionsAtClose"]=[]
        results["exitPosition"]=None
        results["enterPosition"]=None
        results["getBuySell"]=pd.Series()
        results["enterCondition"]=pd.Series()
        results["enterCondition"]=results["enterCondition"].astype('bool')
        results["atPositionLimit"]=None
        results["exitCondition"]=pd.Series()
        results["exitCondition"]=results["exitCondition"].astype('bool')
        results["hackCondition"]=pd.Series()
        results["hackCondition"]=results["hackCondition"].astype('bool')
        ###################################################
        dict=OrderedDict()
        dataSet["dict"]=dict

    if c==1:
        dataSet["position"]=pd.DataFrame()
        dataSet["prediction"]=pd.DataFrame()
######## the feature keys are wrong for c==1
######## logging KeyErrors
        dataSet["price"]=pd.DataFrame()
        ###################################################
        parameters["enter_threshold"]=0.7
        parameters["exit_threshold"]=0.55
        parameters["longLimit"]=10
        parameters["shortLimit"]=10
        parameters["capitalUsageLimit"]=0
        parameters["enterlotSize"]=1
        parameters["exitlotSize"]=1
        parameters["limitType"]='R'
        parameters["price"]="close"
        ###################################################
        parameters["convertLimitdf"]=pd.Series()
        parameters["time"]="01/01/2010"
        parameters["executions"]=pd.Series()
        parameters["capital"]=0.0
        ###################################################
        results["getPriceSeries"]=None
        results["getLongLimit"]=pd.Series()
        results["getShortLimit"]=pd.Series()
        results["getEnterLotSize"]=pd.Series()
        results["getExitLotSize"]=pd.Series()
        results["convertLimit"]=pd.Series()
        results["getInstrumentExecutionsFromExecutions"]=[]
        results["getExecutions"]=None
        results["getExecutionsAtClose"]=[]
        ###################################################
        dict=OrderedDict()
        dataSet["dict"]=dict

    if c==2:
        indexlist=[pd.Timestamp('2017-01-03 09:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1],'b':[2],'c':[3],'d':[4],'e':[5]},index =indexlist)
        dataSet["positionData"]=pd.DataFrame({'a':[4],'b':[10],'c':[15],'d':[-12],'e':[-5]},index =indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.5],'b':[0.2],'c':[0.8],'d':[1.0],'e':[0.0]},index =indexlist)
        dataSet["price"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        ###################################################
        parameters["enter_threshold"]=0.7
        parameters["exit_threshold"]=0.55
        parameters["longLimit"]=10
        parameters["shortLimit"]=10
        parameters["capitalUsageLimit"]=0
        parameters["enterlotSize"]=1
        parameters["exitlotSize"]=1
######## limit type is 'R' for c==2
        parameters["limitType"]='R'
        parameters["price"]="close"
        ###################################################
        parameters["getCurrentPosition"]=[2,0,1,3]
        parameters["getInstrumentId"]=['x','y','z']
        seriesname=pd.Timestamp('2017-01-03 09:30:30')
        parameters["priceSeries"]=pd.Series({'a':1.0,'b':1.0,'c':1.0,'d':1.0,'e':1.0},name=seriesname)
        parameters["convertLimitdf"]=pd.Series({'a':3.14,'b':2.04,'c':1.02,'d':0.98,'e':-1.05},name=seriesname)
        parameters["time"]="01/01/2010"
        parameters["executions"]=pd.Series({'a':1,'b':2,'c':0,'d':4,'e':0,'f':3})
        parameters["capital"]=0.5
        parameters["closeAllPositions"]=False
        ###################################################
        results["getPriceSeries"]=pd.Series({'a':3.14,'b':2.04,'c':1.02,'d':0.98,'e':-1.05},name=seriesname)
        results["getLongLimit"]=pd.Series({'a':10.0,'b':10.0,'c':10.0,'d':10.0,'e':10.0},name=seriesname)
        results["getShortLimit"]=pd.Series({'a':10.0,'b':10.0,'c':10.0,'d':10.0,'e':10.0},name=seriesname)
        results["getEnterLotSize"]=pd.Series({'a':1.0,'b':1.0,'c':1.0,'d':1.0,'e':1.0},name=seriesname)
        results["getExitLotSize"]=pd.Series({'a':1.0,'b':1.0,'c':1.0,'d':1.0,'e':1.0},name=seriesname)
        results["convertLimit"]=pd.Series({'a':3.0,'b':2.0,'c':1.0,'d':0.0,'e':-2.0},name=seriesname)
        results["countforgetinstrumentexecutionsfromexecutions"]=4
        results["countforgetexecutions"]=1
        results["countforgetexecutionsatclose"]=3
        results["listTimeOfExecution"]=['01/01/2010', '01/01/2010', '01/01/2010', '01/01/2010', '01/01/2010', '01/01/2010', '01/01/2010', '01/01/2010']
        results["listInstrumentId"]=['a', 'b', 'd', 'f', 'd', 'x', 'y', 'z']
        results["listVolume"]=[1, 2, 4, 3, 1, 2, 1, 3]
        results["listExecutionType"]=[1, 1, 1, 1, 1, -1, -1, -1]
        results["exitPosition"]=None
        results["enterPosition"]=None
        results["getBuySell"]=pd.Series()
        results["enterCondition"]=pd.Series()
        results["enterCondition"]=results["enterCondition"].astype('bool')
        results["atPositionLimit"]=pd.Series({'a':False,'b':True,'c':True,'d':True,'e':False},name=seriesname)
        results["exitCondition"]=pd.Series()
        results["exitCondition"]=results["exitCondition"].astype('bool')
        results["hackCondition"]=pd.Series()
        results["hackCondition"]=results["hackCondition"].astype('bool')
        ###################################################
        dict=OrderedDict()
        dict["a"]=1
        dict["b"]=2
        dict["c"]=3
        dict["d"]=4
        dict["e"]=5
        dataSet["dict"]=dict

    if c==3:
        indexlist=[pd.Timestamp('2017-01-03 09:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1],'b':[2],'c':[3],'d':[4],'e':[5]},index =indexlist)
        dataSet["positionData"]=pd.DataFrame({'a':[1],'b':[1],'c':[1],'d':[1],'e':[1]},index =indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.5],'b':[0.2],'c':[0.8],'d':[1.0],'e':[0.0]},index =indexlist)
        dataSet["price"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        ###################################################
        parameters["enter_threshold"]=0.7
        parameters["exit_threshold"]=0.55
        #the convertLimit affecting parameters are int
        parameters["longLimit"]=10
        parameters["shortLimit"]=10
        parameters["capitalUsageLimit"]=0
        parameters["enterlotSize"]=1
        parameters["exitlotSize"]=1
######## limit type is 'L' for c==3
        parameters["limitType"]='L'
        parameters["price"]="close"
        ###################################################
        parameters["getCurrentPosition"]=[2,0,1,3]
        seriesname=pd.Timestamp('2017-01-03 09:30:30')
        parameters["priceSeries"]=pd.Series({'a':1.0,'b':1.0,'c':1.0,'d':1.0,'e':1.0},name=seriesname)
        parameters["convertLimitdf"]=pd.Series({'a':3.14,'b':2.04,'c':1.02,'d':0.98,'e':-1.05},name=seriesname)
        parameters["time"]="01/01/2010"
        parameters["closeAllPositions"]=True
        parameters["capital"]=0.5
        ###################################################
        results["getPriceSeries"]=pd.Series({'a':3.14,'b':2.04,'c':1.02,'d':0.98,'e':-1.05},name=seriesname)
        results["getLongLimit"]=pd.Series({'a':10,'b':10,'c':10,'d':10,'e':10},name=seriesname)
        results["getShortLimit"]=pd.Series({'a':10,'b':10,'c':10,'d':10,'e':10},name=seriesname)
        results["getEnterLotSize"]=pd.Series({'a':1,'b':1,'c':1,'d':1,'e':1},name=seriesname)
        results["getExitLotSize"]=pd.Series({'a':1,'b':1,'c':1,'d':1,'e':1},name=seriesname)
        results["convertLimit"]=pd.Series({'a':3.14,'b':2.04,'c':1.02,'d':0.98,'e':-1.05},name=seriesname)
        results["exitPosition"]=pd.Series({'a':-1,'b':-2,'c':-3,'d':-4,'e':-5},name=seriesname)
        results["enterPosition"]=pd.Series({'a':0,'b':-1,'c':1,'d':1,'e':-1},name=seriesname)
        results["getBuySell"]=pd.Series({'a':0.0,'b':-1.0,'c':1.0,'d':1.0,'e':-1.0},name=seriesname)
        results["enterCondition"]=pd.Series({'a':False,'b':True,'c':True,'d':True,'e':True},name=seriesname)
        results["atPositionLimit"]=pd.Series({'a':False,'b':False,'c':False,'d':False,'e':False},name=seriesname)
        results["exitCondition"]=pd.Series({'a':True,'b':False,'c':False,'d':False,'e':False},name=seriesname)
        results["hackCondition"]=pd.Series({'a':False,'b':False,'c':False,'d':False,'e':False},name=seriesname)
        ###################################################
        dict=OrderedDict()
        dict["a"]=1
        dict["b"]=2
        dict["c"]=3
        dict["d"]=4
        dict["e"]=5
        dataSet["dict"]=dict


    if c==4:
        indexlist=  [pd.Timestamp('2017-01-03 09:30:30'),
                     pd.Timestamp('2017-01-03 10:00:30'),
                     pd.Timestamp('2017-01-03 10:30:30'),
                     pd.Timestamp('2017-01-03 11:00:30'),
                     pd.Timestamp('2017-01-03 11:30:30'),
                     pd.Timestamp('2017-01-03 12:00:30'),
                     pd.Timestamp('2017-01-03 12:30:30'),
                     pd.Timestamp('2017-01-03 13:00:30'),
                     pd.Timestamp('2017-01-03 13:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1,2,3,4,5,6,7,8,9],'b':[9,8,7,6,5,4,3,2,1]},index=indexlist)
        dataSet["positionData"]=pd.DataFrame({'a':[1,2,3,4,5,6,7,8,9],'b':[9,8,7,6,5,4,3,2,1]},index=indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        dataSet["price"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        ###################################################
        parameters["enter_threshold"]=0.7
        parameters["exit_threshold"]=0.55
######## the convertLimit affecting parameters are float
        parameters["longLimit"]=10.0
        parameters["shortLimit"]=10.0
        parameters["capitalUsageLimit"]=0
        parameters["enterlotSize"]=1.0
        parameters["exitlotSize"]=1.0
######## the limit type is 'R'
        parameters["limitType"]='R'
        parameters["price"]="close"
        ###################################################
        parameters["getCurrentPosition"]=[2,0,1,0]
        parameters["getInstrumentId"]=['y','z']
        seriesname=pd.Timestamp('2017-01-03 13:30:30')
        parameters["priceSeries"]=pd.Series({'a':1.0,'b':1.0},name=seriesname)
        parameters["convertLimitdf"]=pd.Series({'a':2.35,'b':0.25},name=seriesname)
        parameters["time"]="01/01/2010"
        parameters["executions"]=pd.Series({'a':1,'b':2,'c':0,'d':4})
        parameters["capital"]=-0.5
        parameters["closeAllPositions"]=False
        ###################################################
        results["getPriceSeries"]=pd.Series({'a':2.35,'b':0.25},name=seriesname)
        results["getLongLimit"]=pd.Series({'a':10.0,'b':10.0},name=seriesname)
        results["getShortLimit"]=pd.Series({'a':10.0,'b':10.0},name=seriesname)
        results["getEnterLotSize"]=pd.Series({'a':1.0,'b':1.0},name=seriesname)
        results["getExitLotSize"]=pd.Series({'a':1.0,'b':1.0},name=seriesname)
        results["convertLimit"]=pd.Series({'a':2.0,'b':0.0},name=seriesname)
        results["countforgetinstrumentexecutionsfromexecutions"]=3
        results["countforgetexecutions"]=1
        results["countforgetexecutionsatclose"]=2
        results["listTimeOfExecution"]=['01/01/2010', '01/01/2010', '01/01/2010', '01/01/2010', '01/01/2010', '01/01/2010']
        results["listInstrumentId"]=['a', 'b', 'd', 'b', 'y', 'z']
        results["listVolume"]=[1, 2, 4, 1, 2, 1]
        results["listExecutionType"]=[1, 1, 1, -1, -1, -1]
        results["exitPosition"]=pd.Series({'a':0,'b':-1},name=seriesname)
        results["enterPosition"]=pd.Series({'a':0,'b':0},name=seriesname)
        results["getBuySell"]=pd.Series({'a':-1.0,'b':0.0},name=seriesname)
        results["enterCondition"]=pd.Series({'a':True,'b':False},name=seriesname)
        results["atPositionLimit"]=pd.Series({'a':True,'b':True},name=seriesname)
        results["exitCondition"]=pd.Series({'a':False,'b':True},name=seriesname)
        results["hackCondition"]=pd.Series({'a':False,'b':False},name=seriesname)
        ###################################################
        dict=OrderedDict()
        dict["a"]=1
        dict["b"]=2
        dataSet["dict"]=dict

    if c==5:
        indexlist=  [pd.Timestamp('2017-01-03 09:30:30'),
                     pd.Timestamp('2017-01-03 10:00:30'),
                     pd.Timestamp('2017-01-03 10:30:30'),
                     pd.Timestamp('2017-01-03 11:00:30'),
                     pd.Timestamp('2017-01-03 11:30:30'),
                     pd.Timestamp('2017-01-03 12:00:30'),
                     pd.Timestamp('2017-01-03 12:30:30'),
                     pd.Timestamp('2017-01-03 13:00:30'),
                     pd.Timestamp('2017-01-03 13:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1,2,3,4,5,6,7,8,9],'b':[9,8,7,6,5,4,3,2,1]},index=indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        dataSet["price"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        ###################################################
        parameters["enter_threshold"]=0.7
        parameters["exit_threshold"]=0.55
######## the convertLimit affecting parameters are float
        parameters["longLimit"]=10.0
        parameters["shortLimit"]=10.0
        parameters["capitalUsageLimit"]=0
        parameters["enterlotSize"]=1.0
        parameters["exitlotSize"]=1.0
######## the limitType is 'L'
        parameters["limitType"]='L'
        parameters["price"]="close"
        ###################################################
        parameters["getCurrentPosition"]=[2,0,1,3]
        seriesname=pd.Timestamp('2017-01-03 13:30:30')
        parameters["priceSeries"]=pd.Series({'a':1.0,'b':1.0},name=seriesname)
        parameters["convertLimitdf"]=pd.Series({'a':2.35,'b':0.25},name=seriesname)
        ###################################################
        results["getPriceSeries"]=pd.Series({'a':2.35,'b':0.25},name=seriesname)
        results["getLongLimit"]=pd.Series({'a':10.0,'b':10.0},name=seriesname)
        results["getShortLimit"]=pd.Series({'a':10.0,'b':10.0},name=seriesname)
        results["getEnterLotSize"]=pd.Series({'a':1.0,'b':1.0},name=seriesname)
        results["getExitLotSize"]=pd.Series({'a':1.0,'b':1.0},name=seriesname)
        results["convertLimit"]=pd.Series({'a':2.35,'b':0.25},name=seriesname)
        ###################################################
        dict=OrderedDict()
        dict["a"]=1
        dict["b"]=2
        dataSet["dict"]=dict

    if c==6:
        indexlist=  [pd.Timestamp('2017-01-03 09:30:30'),
                     pd.Timestamp('2017-01-03 10:00:30'),
                     pd.Timestamp('2017-01-03 10:30:30'),
                     pd.Timestamp('2017-01-03 11:00:30'),
                     pd.Timestamp('2017-01-03 11:30:30'),
                     pd.Timestamp('2017-01-03 12:00:30'),
                     pd.Timestamp('2017-01-03 12:30:30'),
                     pd.Timestamp('2017-01-03 13:00:30'),
                     pd.Timestamp('2017-01-03 13:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1,2,3,4,5,6,7,8,9],'b':[9,8,7,6,5,4,3,2,1]},index=indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        dataSet["price"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        ###################################################
        parameters["enter_threshold"]=0.7
        parameters["exit_threshold"]=0.55
######## the convertLimit affecting parameters are float
        parameters["longLimit"]=10.0
        parameters["shortLimit"]=10.0
        parameters["capitalUsageLimit"]=0
        parameters["enterlotSize"]=1.0
        parameters["exitlotSize"]=1.0
######## the limitType is 'R'
        parameters["limitType"]='R'
        parameters["price"]="close"
        ###################################################
        parameters["getCurrentPosition"]=[2,0,1,3]
        seriesname=pd.Timestamp('2017-01-03 13:30:30')
        #the price Series is all zero
        parameters["priceSeries"]=pd.Series({'a':0.0,'b':0.0},name=seriesname)
        parameters["convertLimitdf"]=pd.Series({'a':2.35,'b':0.25},name=seriesname)
        ###################################################
        results["getPriceSeries"]=pd.Series({'a':2.35,'b':0.25},name=seriesname)
        results["getLongLimit"]=pd.Series({'a':np.inf,'b':np.inf},name=seriesname)
        results["getShortLimit"]=pd.Series({'a':np.inf,'b':np.inf},name=seriesname)
        results["getEnterLotSize"]=pd.Series({'a':np.inf,'b':np.inf},name=seriesname)
        results["getExitLotSize"]=pd.Series({'a':np.inf,'b':np.inf},name=seriesname)
        results["convertLimit"]=pd.Series({'a':np.inf,'b':np.inf},name=seriesname)
        ###################################################
        dict=OrderedDict()
        dict["a"]=1
        dict["b"]=2
        dataSet["dict"]=dict

    if c==7:
        indexlist=  [pd.Timestamp('2017-01-03 09:30:30'),
                     pd.Timestamp('2017-01-03 10:00:30'),
                     pd.Timestamp('2017-01-03 10:30:30'),
                     pd.Timestamp('2017-01-03 11:00:30'),
                     pd.Timestamp('2017-01-03 11:30:30'),
                     pd.Timestamp('2017-01-03 12:00:30'),
                     pd.Timestamp('2017-01-03 12:30:30'),
                     pd.Timestamp('2017-01-03 13:00:30'),
                     pd.Timestamp('2017-01-03 13:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1,2,3,4,5,6,7,8,9],'b':[9,8,7,6,5,4,3,2,1]},index=indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        dataSet["price"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        ###################################################
        parameters["enter_threshold"]=0.7
        parameters["exit_threshold"]=0.55
######## the convertLimit affecting parameters are dicts
        parameters["longLimit"]={'a':10.0,'b':10.0}
        parameters["shortLimit"]={'a':10.0,'b':10.0}
        parameters["capitalUsageLimit"]=0
        parameters["enterlotSize"]={'a':1.0,'b':1.0}
        parameters["exitlotSize"]={'a':1.0,'b':1.0}
        parameters["limitType"]='L'
        parameters["price"]="close"
        ###################################################
        parameters["getCurrentPosition"]=[2,0,1,3]
        seriesname=pd.Timestamp('2017-01-03 13:30:30')
        parameters["priceSeries"]=pd.Series({'a':1.0,'b':1.0},name=seriesname)
        parameters["convertLimitdf"]=pd.Series({'a':2.35,'b':0.25},name=seriesname)
        ###################################################
        results["getPriceSeries"]=pd.Series({'a':2.35,'b':0.25},name=seriesname)
        results["getLongLimit"]=pd.Series({'a':10.0,'b':10.0},name=seriesname)
        results["getShortLimit"]=pd.Series({'a':10.0,'b':10.0},name=seriesname)
        results["getEnterLotSize"]=pd.Series({'a':1.0,'b':1.0},name=seriesname)
        results["getExitLotSize"]=pd.Series({'a':1.0,'b':1.0},name=seriesname)
        results["convertLimit"]=pd.Series({'a':2.35,'b':0.25},name=seriesname)
        ###################################################
        dict=OrderedDict()
        dict["a"]=1
        dict["b"]=2
        dataSet["dict"]=dict

    if c==8:
        indexlist=  [pd.Timestamp('2017-01-03 09:30:30'),
                     pd.Timestamp('2017-01-03 10:00:30'),
                     pd.Timestamp('2017-01-03 10:30:30'),
                     pd.Timestamp('2017-01-03 11:00:30'),
                     pd.Timestamp('2017-01-03 11:30:30'),
                     pd.Timestamp('2017-01-03 12:00:30'),
                     pd.Timestamp('2017-01-03 12:30:30'),
                     pd.Timestamp('2017-01-03 13:00:30'),
                     pd.Timestamp('2017-01-03 13:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1,2,3,4,5,6,7,8,9],'b':[9,8,7,6,5,4,3,2,1]},index=indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        dataSet["price"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        ###################################################
        parameters["enter_threshold"]=0.7
        parameters["exit_threshold"]=0.55
######## the convertLimit affecting parameters are pandas DataFrame of size (1 X n)
        parameters["longLimit"]=pd.DataFrame({'a':[10.0],'b':[10.0]})
        parameters["shortLimit"]=pd.DataFrame({'a':[10.0],'b':[10.0]})
        parameters["capitalUsageLimit"]=0
        parameters["enterlotSize"]=pd.DataFrame({'a':[1.0],'b':[1.0]})
        parameters["exitlotSize"]=pd.DataFrame({'a':[1.0],'b':[1.0]})
        parameters["limitType"]='L'
        parameters["price"]="close"
        ###################################################
        parameters["getCurrentPosition"]=[2,0,1,3]
        seriesname=pd.Timestamp('2017-01-03 13:30:30')
        parameters["priceSeries"]=pd.Series({'a':1.0,'b':1.0},name=seriesname)
        parameters["convertLimitdf"]=pd.Series({'a':2.35,'b':0.25},name=seriesname)
        ###################################################
        results["getPriceSeries"]=pd.Series({'a':2.35,'b':0.25},name=seriesname)
        results["getLongLimit"]=pd.Series({'a':10.0,'b':10.0},name=seriesname)
        results["getShortLimit"]=pd.Series({'a':10.0,'b':10.0},name=seriesname)
        results["getEnterLotSize"]=pd.Series({'a':1.0,'b':1.0},name=seriesname)
        results["getExitLotSize"]=pd.Series({'a':1.0,'b':1.0},name=seriesname)
        results["convertLimit"]=pd.Series({'a':2.35,'b':0.25},name=seriesname)
        ###################################################
        dict=OrderedDict()
        dict["a"]=1
        dict["b"]=2
        dataSet["dict"]=dict

    if c==9:
        indexlist=  [pd.Timestamp('2017-01-03 09:30:30'),
                     pd.Timestamp('2017-01-03 10:00:30'),
                     pd.Timestamp('2017-01-03 10:30:30'),
                     pd.Timestamp('2017-01-03 11:00:30'),
                     pd.Timestamp('2017-01-03 11:30:30'),
                     pd.Timestamp('2017-01-03 12:00:30'),
                     pd.Timestamp('2017-01-03 12:30:30'),
                     pd.Timestamp('2017-01-03 13:00:30'),
                     pd.Timestamp('2017-01-03 13:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1,2,3,4,5,6,7,8,9],'b':[9,8,7,6,5,4,3,2,1]},index=indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        dataSet["price"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        ###################################################
        parameters["enter_threshold"]=0.7
        parameters["exit_threshold"]=0.55
######## the convertLimit affecting parameters are pandas DataFrame of size (n X 1)
        parameters["longLimit"]=pd.DataFrame({0:[10.0,10.0]},index=['a','b'])
        parameters["shortLimit"]=pd.DataFrame({0:[10.0,10.0]},index=['a','b'])
        parameters["capitalUsageLimit"]=0
        parameters["enterlotSize"]=pd.DataFrame({0:[1.0,1.0]},index=['a','b'])
        parameters["exitlotSize"]=pd.DataFrame({0:[1.0,1.0]},index=['a','b'])
        parameters["limitType"]='L'
        parameters["price"]="close"
        ###################################################
        parameters["getCurrentPosition"]=[2,0,1,3]
        seriesname=pd.Timestamp('2017-01-03 13:30:30')
        parameters["priceSeries"]=pd.Series({'a':1.0,'b':1.0},name=seriesname)
        parameters["convertLimitdf"]=pd.Series({'a':2.35,'b':0.25},name=seriesname)
        ###################################################
        results["getPriceSeries"]=pd.Series({'a':2.35,'b':0.25},name=seriesname)
        results["getLongLimit"]=pd.Series({'a':10.0,'b':10.0},name=seriesname)
        results["getShortLimit"]=pd.Series({'a':10.0,'b':10.0},name=seriesname)
        results["getEnterLotSize"]=pd.Series({'a':1.0,'b':1.0},name=seriesname)
        results["getExitLotSize"]=pd.Series({'a':1.0,'b':1.0},name=seriesname)
        results["convertLimit"]=pd.Series({'a':2.35,'b':0.25},name=seriesname)
        ###################################################
        dict=OrderedDict()
        dict["a"]=1
        dict["b"]=2
        dataSet["dict"]=dict

    return {"dataSet":dataSet,"parameters":parameters,"results":results}
