import pandas as pd
import numpy as np
def getDataSet(c):
    dataSet={}
    parameters={}
    results={}
#### empty datasets
#### logging IndexErrors
    if(c==0):
        dataSet["getDataDf"] = pd.DataFrame({"capital":[],"featureKey":[]})
        ##############################################
        parameters["capitalKey"]="capital",
        parameters["initial_capital"] = 0.0
        ##############################################
        results["maxcapitalusage_Market"]=0
#### capitalKey is wrong
#### gives KeyError
    if(c==1):
        indexlist=  [pd.tslib.Timestamp('2017-01-03 09:30:30'),
                     pd.tslib.Timestamp('2017-01-03 10:00:30'),
                     pd.tslib.Timestamp('2017-01-03 10:30:30'),
                     pd.tslib.Timestamp('2017-01-03 11:00:30'),
                     pd.tslib.Timestamp('2017-01-03 11:30:30'),
                     pd.tslib.Timestamp('2017-01-03 12:00:30'),
                     pd.tslib.Timestamp('2017-01-03 12:30:30'),
                     pd.tslib.Timestamp('2017-01-03 13:00:30'),
                     pd.tslib.Timestamp('2017-01-03 13:30:30')]
        dataSet["getDataDf"]=pd.DataFrame({'capitalKey':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'featureKey':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        ##############################################
        parameters["capitalKey"] = "capital"
        parameters["initial_capital"] = 0.0
        ##############################################
        results["maxcapitalusage_Market"]=0
#### data has nans and infs
    if(c==2):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30'),pd.tslib.Timestamp('2017-01-03 10:30:30'),pd.tslib.Timestamp('2017-01-03 11:30:30')]
        dataSet["getDataDf"] = pd.DataFrame({'capital':[1,3.0,np.inf],'featureKey':[np.inf, 2, np.inf]},index =indexlist)
        ##############################################
        parameters["capitalKey"] = "capital"
        parameters["initial_capital"] = 0.0
        ##############################################
        results["maxcapitalusage_Market"]=2.0
#### testing for dataSet with len 1
#### will give IndexError
    if(c==3):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30')]
        dataSet["getDataDf"]=pd.DataFrame({'capital':[3.14],'featureKey':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        ##############################################
        parameters["capitalKey"] = "capital"
        parameters["initial_capital"] = 0.0
        ##############################################
        results["maxcapitalusage_Market"]=0
#### sample data
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
        dataSet["getDataDf"]=pd.DataFrame({'capital':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'featureKey':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        ##############################################
        parameters["capitalKey"] = "capital"
        parameters["initial_capital"]=0.0
        ##############################################
        results["maxcapitalusage_Market"]=1.02
    return {"dataSet":dataSet, "parameters":parameters, "results":results}
