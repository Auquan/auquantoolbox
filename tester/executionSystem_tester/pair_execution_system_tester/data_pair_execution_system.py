import pandas as pd
import numpy as np
from collections import OrderedDict
from datetime import datetime, time, timedelta

def data_pair_execution_system(c):
    dataSet={}
    parameters={}
    results={}

    if c==0:
######## providing empty DataFrames as the mock data
######## logging IndexErrors
        dataSet["position"]=pd.DataFrame()
        dataSet["price"]=pd.DataFrame()
        dataSet["prediction"]=pd.DataFrame()
        #################################################
        parameters["pair"]=[]
        parameters["pairRatio"]=0.3
        parameters["pairEnter_threshold"]=0.7
        parameters["pairExit_threshold"]=0.55
        parameters["pairLongLimit"]=10
        parameters["pairShortLimit"]=10
        parameters["pairCapitalUsageLimit"]=0
        parameters["pairLotSize"]=1
        parameters["price"]="close"
        #################################################
        parameters["time"]=datetime(2018, 6, 1)
        parameters["capital"]=0.0
        results["count"]=0
        #################################################
        results["getExecutions"]=None

#### Error displayed for DataFrames having any different than 2 columns
    if c==1:
        indexlist=index = [pd.tslib.Timestamp('2017-01-03 09:30:30'),
                           pd.tslib.Timestamp('2017-01-03 10:00:30'),
                           pd.tslib.Timestamp('2017-01-03 10:30:30'),
                           pd.tslib.Timestamp('2017-01-03 11:00:30'),
                           pd.tslib.Timestamp('2017-01-03 11:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1,2,3,4,5],'b':[1,2,3,4,5],'c':[1,2,3,4,5]},index =indexlist)
        dataSet["price"]=pd.DataFrame({'a':[1.24,-2.05,-0.02,4.25,1.02],'b':[1.08,1.04,-3.03,-1.02,0.25],'c':[2.14,-1.46,2.56,-4.03,1.02]},index =indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.5,0.55,0.6,0.7,0.3],'b':[0.7,0.9,0.9,0.1,0.5],'c':[0.2,0.5,1.0,0.7,0.6]},index =indexlist)
        #################################################
        parameters["pair"]=['a','b']
        parameters["pairRatio"]=10
        parameters["pairEnter_threshold"]=0.7
        parameters["pairExit_threshold"]=0.55
        parameters["pairLongLimit"]=10
        parameters["pairShortLimit"]=10
        parameters["pairCapitalUsageLimit"]=0
        parameters["pairLotSize"]=1
        parameters["price"]="close"
        #################################################
        parameters["time"]=datetime(2018, 6, 1)
        parameters["capital"]=0.6
        results["count"]=1
        #################################################
        results["getExecutions"]=None

#### testing for sample data for c=2 & 3
    if c==2:
        indexlist=index =[pd.tslib.Timestamp('2017-01-03 09:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1],'b':[2]},index =indexlist)
        dataSet["price"]=pd.DataFrame({'a':[3.14],'b':[2.04]},index =indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.5],'b':[0.2]},index =indexlist)
        #################################################
        parameters["pair"]=['a','b']
        parameters["pairRatio"]=10
        parameters["pairEnter_threshold"]=0.7
        parameters["pairExit_threshold"]=0.55
        parameters["pairLongLimit"]=10
        parameters["pairShortLimit"]=10
        parameters["pairCapitalUsageLimit"]=0
        parameters["pairLotSize"]=1
        parameters["price"]="close"
        #################################################
        parameters["time"]=datetime(2018, 6, 1)
        parameters["capital"]=0.5
        results["count"]=2
        #################################################
        results["listVolume"]=[1, 10]
        results["listInstrumentId"]=['a', 'b']
        results["listExecutionType"]=[-1, -1]
        results["listTimeOfExecution"]=[datetime(2018, 6, 1, 0, 0), datetime(2018, 6, 1, 0, 0)]

    if c==3:
        indexlist=index = [pd.tslib.Timestamp('2017-01-03 09:30:30'),
                           pd.tslib.Timestamp('2017-01-03 10:00:30'),
                           pd.tslib.Timestamp('2017-01-03 10:30:30'),
                           pd.tslib.Timestamp('2017-01-03 11:00:30'),
                           pd.tslib.Timestamp('2017-01-03 11:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1,2,3,4,5],'b':[1,2,3,4,5]},index =indexlist)
        dataSet["price"]=pd.DataFrame({'a':[1.24,-2.05,-0.02,4.25,1.02],'b':[1.08,1.04,-3.03,-1.02,0.25]},index =indexlist)
        dataSet["prediction"]=pd.DataFrame({'a':[0.5,0.55,0.6,0.7,0.3],'b':[0.7,0.9,0.9,0.1,0.5]},index =indexlist)
        #################################################
        parameters["pair"]=['a','b']
        parameters["pairRatio"]=10
        parameters["pairEnter_threshold"]=0.7
        parameters["pairExit_threshold"]=0.55
        parameters["pairLongLimit"]=10
        parameters["pairShortLimit"]=10
        parameters["pairCapitalUsageLimit"]=0
        parameters["pairLotSize"]=1
        parameters["price"]="close"
        #################################################
        parameters["time"]=datetime(2018, 6, 1)
        parameters["capital"]=0.6
        results["count"]=2
        #################################################
        results["listVolume"]=[1, 5]
        results["listInstrumentId"]=['a', 'b']
        results["listExecutionType"]=[-1, -1]
        results["listTimeOfExecution"]=[datetime(2018, 6, 1, 0, 0), datetime(2018, 6, 1, 0, 0)]

    return {"dataSet":dataSet,"parameters":parameters,"results":results}
