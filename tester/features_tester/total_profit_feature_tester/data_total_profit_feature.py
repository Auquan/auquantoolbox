import pandas as pd
import numpy as np
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
        ##############################################
        parameters["pnlKey"]="pnlKey"
        ##############################################
        results["total_profit_Instrument"]=pd.Series()
        results["total_profit_Market"]=0.0
#### data includes nans and infs
    if(c==1):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30'),pd.tslib.Timestamp('2017-01-03 10:30:30'),pd.tslib.Timestamp('2017-01-03 11:30:30')]
        dataSet["pnlKey"] = pd.DataFrame({'a':[1,np.nan,np.nan],'b':[np.inf, 2, 0]},index =indexlist)
        dataSet["featureKey"] = pd.DataFrame({'a':[1,np.nan,3],'b':[np.inf, 2, np. nan]},index =indexlist)
        dataSet["getDataDf"] = pd.DataFrame({'featureKey':[1,3.0,np.inf],'pnlKey':[np.inf, 2, np.inf]},index =indexlist)
        ##############################################
        parameters["pnlKey"]="pnlKey"
        ##############################################
        results["total_profit_Instrument"]=pd.Series({'a':3.0,'b':0.0})
        results["total_profit_Market"]=3.0
#### sample data
    if(c==2):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30')]
        dataSet["pnlKey"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        dataSet["featureKey"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        dataSet["getDataDf"]=pd.DataFrame({'featureKey':[3.14],'pnlKey':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        ##############################################
        parameters["pnlKey"]="pnlKey"
        ##############################################
        results["total_profit_Instrument"]=pd.Series({'a':3.14,'b':2.04,'c':1.02,'d':0.98,'e':0.0})
        results["total_profit_Market"]=2.04
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
        dataSet["pnlKey"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        dataSet["featureKey"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["getDataDf"]=pd.DataFrame({'featureKey':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'pnlKey':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        ##############################################
        parameters["pnlKey"]="pnlKey"
        ##############################################
        results["total_profit_Instrument"]=pd.Series({'a':2.35,'b':0.65})
        results["total_profit_Market"]=5.02
    return {"dataSet":dataSet, "parameters":parameters, "results":results}
