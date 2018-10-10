import pandas as pd
import numpy as np
def getDataSet(c):
    dataSet={}
    parameters={}
    results={}
#### dataSet are empty
#### logging IndexError
    if(c==0):
        dataSet["position"] = pd.DataFrame()
        dataSet["price"] = pd.DataFrame()
        dataSet["fees"] = pd.DataFrame()
        dataSet["capital"] = pd.DataFrame()
        dataSet["featureKey"] = pd.DataFrame()
        dataSet["getDataDf"] = pd.DataFrame({"featureKey":[],"pnlKey":[]})
        ##############################################
        parameters["price"] = "price"
        parameters["fees"] = "fees"
        parameters["initial_capital"] = 0.0
        ##############################################
        results["capital_Instrument"]=None
        results["capital_Market"]=0.0
#### data has nans and infs
    if(c==1):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30'),pd.tslib.Timestamp('2017-01-03 10:30:30'),pd.tslib.Timestamp('2017-01-03 11:30:30')]
        dataSet["position"] = pd.DataFrame({'a':[-np.inf,np.nan,np.inf],'b':[np.inf, 2, -np.inf]},index =indexlist)
        dataSet["price"] = pd.DataFrame({'a':[1,np.nan,3],'b':[0, 2, np.nan]},index =indexlist)
        dataSet["fees"] = pd.DataFrame({'a':[1,np.nan,np.nan],'b':[np.inf, 2, 0]},index =indexlist)
        dataSet["capital"] = pd.DataFrame({'a':[1,np.nan,3],'b':[np.inf, 2, np. nan]},index =indexlist)
        dataSet["featureKey"] = pd.DataFrame({'a':[1,3.0,np.inf],'b':[np.inf, 2, np.inf]},index =indexlist)
        dataSet["getDataDf"] = pd.DataFrame({'featureKey':[1,3.0,np.inf],'pnlKey':[np.inf, 2, np.inf]},index =indexlist)
        ##############################################
        parameters["price"] = "price"
        parameters["fees"] = "fees"
        parameters["initial_capital"] = 0.0
        ##############################################
        results["capital_Instrument"]=pd.Series({'a':0.0,'b':0.0})
        results["capital_Market"]=3.0
#### data has one element for each column
#### logging IndexError
    if(c==2):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1],'b':[2],'c':[3],'d':[4],'e':[5]},index =indexlist)
        dataSet["fees"]=pd.DataFrame({'a':[0.5],'b':[0.2],'c':[0.8],'d':[1.0],'e':[0.0]},index =indexlist)
        dataSet["price"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        dataSet["capital"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        dataSet["featureKey"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        dataSet["getDataDf"]=pd.DataFrame({'featureKey':[3.14],'pnlKey':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        ##############################################
        parameters["price"] = "price"
        parameters["fees"] = "fees"
        parameters["initial_capital"]=1.0
        ##############################################
        results["capital_Instrument"]=None
        results["capital_Market"]=1.0
#### testing for sample data
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
        dataSet["position"]=pd.DataFrame({'a':[1,2,3,4,5,6,7,8,9],'b':[9,8,7,6,5,4,3,2,1]},index=indexlist)
        dataSet["price"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["fees"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        dataSet["capital"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["featureKey"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["getDataDf"]=pd.DataFrame({'featureKey':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'pnlKey':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        ##############################################
        parameters["price"] = "price"
        parameters["fees"] = "fees"
        parameters["initial_capital"] = 0.0
        ##############################################
        results["capital_Instrument"]=pd.Series({'a':-18.71,'b':-1.29})
        results["capital_Market"]=2.4199999999999995
    return {"dataSet":dataSet, "parameters":parameters, "results":results}
