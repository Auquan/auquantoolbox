import pandas as pd
import numpy as np
def getDataSet(c):
    dataSet={}
    parameters={}
    results={}
#### empty datasets
#### logging IndexErrors
    if(c==0):
        dataSet["position"] = pd.DataFrame()
        dataSet["price"] = pd.DataFrame()
        ##############################################
        parameters["price"]="price"
        parameters["feesDict"]={0:0, -1:-1, 1:1}
        ##############################################
        results["fees_Instrument"]=None
#### data has 1 element in each column but updateNum is 1, so it does not give IndexError
    if(c==1):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1],'b':[2],'c':[3],'d':[4],'e':[5]},index =indexlist)
        dataSet["price"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        ##############################################
        parameters["price"]="price"
        parameters["feesDict"]={0:0, -1:-1, 1:1}
        ##############################################
        results["fees_Instrument"]= pd.Series({'a':3.14,'b':4.08,'c':3.06,'d':3.92,'e':-5.25})
#### data has nans and infs
    if(c==2):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30'),pd.tslib.Timestamp('2017-01-03 10:30:30'),pd.tslib.Timestamp('2017-01-03 11:30:30')]
        dataSet["position"] = pd.DataFrame({'a':[-np.inf,np.nan,np.inf],'b':[np.inf, 2, -np.inf]},index =indexlist)
        dataSet["price"] = pd.DataFrame({'a':[1,np.nan,3],'b':[0, 2, np.nan]},index =indexlist)
        ##############################################
        parameters["price"]="price"
        parameters["feesDict"]={0:0, -1:-1, 1:1}
        ##############################################
        results["fees_Instrument"]= pd.Series({'a':0.0,'b':-0.0})
#### sample data
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
        ##############################################
        parameters["price"]="price"
        parameters["feesDict"]={0:0, -1:-1, 1:1}
        ##############################################
        results["fees_Instrument"]= pd.Series({'a':2.35,'b':-0.25})
#### data has 1 element in each column but updateNum is 4, so it gives IndexError
    if(c==4):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30')]
        dataSet["position"]=pd.DataFrame({'a':[1],'b':[2],'c':[3],'d':[4],'e':[5]},index =indexlist)
        dataSet["price"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        ##############################################
        parameters["price"]="price"
        parameters["feesDict"]={0:0, -1:-1, 1:1}
        ##############################################
        results["fees_Instrument"]=None
    return {"dataSet":dataSet, "parameters":parameters, "results":results}
