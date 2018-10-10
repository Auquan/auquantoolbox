import pandas as pd
import numpy as np
from collections import OrderedDict
def getDataSet(c):
    dataSet={}
    parameters={}
    results={}
#### empty datasets
#### logging IndexErrors
    if(c==0):
        dataSet["featureKey"] = pd.DataFrame()
        dataSet["pnlKey"] = pd.DataFrame()
        dataSet["getDataDf"] = pd.DataFrame({"featureKey":[],"pnlKey":[]})
        dataSet["dict"]=OrderedDict()
        ##############################################
        parameters["pnlKey"]="pnlKey"
        ##############################################
        results["variance_Instrument"]=pd.Series()
        results["variance_Market"]=0
#### updateNum==1
    if(c==1):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30'),pd.tslib.Timestamp('2017-01-03 10:30:30'),pd.tslib.Timestamp('2017-01-03 11:30:30')]
        dataSet["pnlKey"] = pd.DataFrame({'a':[1,np.nan,np.nan],'b':[np.inf, 2, 0]},index =indexlist)
        dataSet["featureKey"] = pd.DataFrame({'a':[1,np.nan,3],'b':[np.inf, 2, np. nan]},index =indexlist)
        dataSet["getDataDf"] = pd.DataFrame({'featureKey':[1,3.0,np.inf],'pnlKey':[np.inf, 2, np.inf]},index =indexlist)
        dataSet["dict"]=OrderedDict()
        dataSet["dict"]['a']=1
        dataSet["dict"]['b']=2
        ##############################################
        parameters["pnlKey"]="pnlKey"
        ##############################################
        results["variance_Instrument"]=pd.Series({'a':0,'b':0})
        results["variance_Market"]=0
#### data includes infs and nans
    if(c==2):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30'),pd.tslib.Timestamp('2017-01-03 10:30:30'),pd.tslib.Timestamp('2017-01-03 11:30:30')]
        dataSet["pnlKey"] = pd.DataFrame({'a':[1,np.nan,np.nan],'b':[np.inf, 2, 0]},index =indexlist)
        dataSet["featureKey"] = pd.DataFrame({'a':[1,np.nan,3],'b':[np.inf, 2, np. nan]},index =indexlist)
        dataSet["getDataDf"] = pd.DataFrame({'featureKey':[1,3.0,np.inf],'pnlKey':[np.inf, 2, np.inf]},index =indexlist)
        dataSet["dict"]=OrderedDict()
        dataSet["dict"]['a']=1
        dataSet["dict"]['b']=2
        ##############################################
        parameters["pnlKey"]="pnlKey"
        ##############################################
        results["variance_Instrument"]=pd.Series({'a':1.5,'b':4.0})
        results["variance_Market"]=5.5
#### data has only one element for each element, will give zero series
    if(c==3):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30')]
        dataSet["pnlKey"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        dataSet["featureKey"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        dataSet["getDataDf"]=pd.DataFrame({'featureKey':[3.14],'pnlKey':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        dataSet["dict"]=OrderedDict()
        dataSet["dict"]['a']=1
        dataSet["dict"]['b']=2
        dataSet["dict"]['c']=3
        dataSet["dict"]['d']=4
        dataSet["dict"]['e']=5
        ##############################################
        parameters["pnlKey"]="pnlKey"
        ##############################################
        results["variance_Instrument"]=pd.Series({'a':0,'b':0,'c':0,'d':0,'e':0})
        results["variance_Market"]=0
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
        dataSet["pnlKey"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        dataSet["featureKey"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["getDataDf"]=pd.DataFrame({'featureKey':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'pnlKey':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["dict"]=OrderedDict()
        dataSet["dict"]['a']=1
        dataSet["dict"]['b']=2
        ##############################################
        parameters["pnlKey"]="pnlKey"
        ##############################################
        results["variance_Instrument"]=pd.Series({'a':1.826,'b':0.246})
        results["variance_Market"]=3.974
    return {"dataSet":dataSet, "parameters":parameters, "results":results}
