import pandas as pd
import numpy as np
def getDataSet(c):
    dataSet={}
    parameters={}
    results={}
#### empty datasets
#### logging IndexErrors
    if(c==0):
        dataSet["featureName"] = pd.DataFrame({"instrumentId1":[],"instrumentId2":[]})
        ##############################################
        parameters["featureName"]="featureName"
        parameters["instrumentId1"]="instrumentId1"
        parameters["instrumentId2"]="instrumentId2"
        parameters["period"]=1
        ##############################################
        results["crossInstrument_correlation_Market"]=0
#### data has nans and infs
    if(c==1):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30'),pd.tslib.Timestamp('2017-01-03 10:30:30'),pd.tslib.Timestamp('2017-01-03 11:30:30')]
        dataSet["featureName"] = pd.DataFrame({'instrumentId1':[1,3.0,np.inf],'instrumentId2':[np.inf, 2, np.inf]},index =indexlist)
        ##############################################
        parameters["featureName"]="featureName"
        parameters["instrumentId1"]="instrumentId1"
        parameters["instrumentId2"]="instrumentId2"
        parameters["period"]=2
        ##############################################
        results["crossInstrument_correlation_Market"]=1.0
#### testing for dataSet with len 1
#### logging IndexError
    if(c==2):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30')]
        dataSet["featureName"]=pd.DataFrame({'instrumentId1':[3.14],'instrumentId2':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        ##############################################
        parameters["featureName"]="featureName"
        parameters["instrumentId1"]="instrumentId1"
        parameters["instrumentId2"]="instrumentId2"
        parameters["period"]=1
        ##############################################
        results["crossInstrument_correlation_Market"]=0
#### period is 0, converts the series to nans, returning 0 back
    if(c==3):
        indexlist=  [pd.tslib.Timestamp('2017-01-03 09:30:30'),
                     pd.tslib.Timestamp('2017-01-03 10:00:30'),
                     pd.tslib.Timestamp('2017-01-03 10:30:30'),
                     pd.tslib.Timestamp('2017-01-03 11:00:30'),
                     pd.tslib.Timestamp('2017-01-03 11:30:30'),
                     pd.tslib.Timestamp('2017-01-03 12:00:30'),
                     pd.tslib.Timestamp('2017-01-03 12:30:30'),
                     pd.tslib.Timestamp('2017-01-03 13:00:30'),
                     pd.tslib.Timestamp('2017-01-03 13:30:30')]
        dataSet["featureName"]=pd.DataFrame({'instrumentId1':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'instrumentId2':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        ##############################################
        parameters["featureName"]="featureName"
        parameters["instrumentId1"]="instrumentId1"
        parameters["instrumentId2"]="instrumentId2"
        parameters["period"]=0
        ##############################################
        results["crossInstrument_correlation_Market"]=0
#### sample test
    if(c==4):
        indexlist=  [pd.tslib.Timestamp('2017-01-03 09:30:30'),
                     pd.tslib.Timestamp('2017-01-03 10:00:30'),
                     pd.tslib.Timestamp('2017-01-03 10:30:30'),
                     pd.tslib.Timestamp('2017-01-03 11:00:30'),
                     pd.tslib.Timestamp('2017-01-03 11:30:30'),
                     pd.tslib.Timestamp('2017-01-03 12:00:30'),
                     pd.tslib.Timestamp('2017-01-03 12:30:30'),
                     pd.tslib.Timestamp('2017-01-03 13:00:30'),
                     pd.tslib.Timestamp('2017-01-03 13:30:30')]
        dataSet["featureName"]=pd.DataFrame({'instrumentId1':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'instrumentId2':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        ##############################################
        parameters["featureName"]="featureName"
        parameters["instrumentId1"]="instrumentId1"
        parameters["instrumentId2"]="instrumentId2"
        parameters["period"]=3
        ##############################################
        results["crossInstrument_correlation_Market"]=-0.74
#### period is 11, more than the length of the series, converts the series to nans, returning 0 back
    if(c==5):
        indexlist=  [pd.tslib.Timestamp('2017-01-03 09:30:30'),
                     pd.tslib.Timestamp('2017-01-03 10:00:30'),
                     pd.tslib.Timestamp('2017-01-03 10:30:30'),
                     pd.tslib.Timestamp('2017-01-03 11:00:30'),
                     pd.tslib.Timestamp('2017-01-03 11:30:30'),
                     pd.tslib.Timestamp('2017-01-03 12:00:30'),
                     pd.tslib.Timestamp('2017-01-03 12:30:30'),
                     pd.tslib.Timestamp('2017-01-03 13:00:30'),
                     pd.tslib.Timestamp('2017-01-03 13:30:30')]
        dataSet["featureName"]=pd.DataFrame({'instrumentId1':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'instrumentId2':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        ##############################################
        parameters["featureName"]="featureName"
        parameters["instrumentId1"]="instrumentId1"
        parameters["instrumentId2"]="instrumentId2"
        parameters["period"]=11
        ##############################################
        results["crossInstrument_correlation_Market"]=0
    return {"dataSet":dataSet, "parameters":parameters, "results":results}
