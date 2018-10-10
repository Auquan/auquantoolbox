import pandas as pd
import numpy as np
def getDataSet(c):
    dataSet={}
    parameters={}
    results={}
#### empty datasets
#### logging IndexErrors
    if(c==0):
        dataSet["predictionKey"] = pd.DataFrame()
        dataSet["target"] = pd.DataFrame()
        dataSet["score"] = pd.DataFrame()
        dataSet["featureKey"] = pd.DataFrame()
        dataSet["getDataDf"] = pd.DataFrame({"featureKey":[]})
        dataSet["dict"]={}
        ##############################################
        parameters["predictionKey"]="predictionKey"
        parameters["target"]="target"
        parameters["instrument_score_feature"]="score"
        ##############################################
        results["score_logless_Instrument"]=None
        results["score_logless_Market"]=0
#### data has nans and infs
    if(c==1):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30'),pd.tslib.Timestamp('2017-01-03 10:30:30'),pd.tslib.Timestamp('2017-01-03 11:30:30')]
        dataSet["predictionKey"] = pd.DataFrame({'a':[-np.inf,np.nan,np.inf],'b':[np.inf, 0.2, -np.inf]},index =indexlist)
        dataSet["target"] = pd.DataFrame({'a':[1,np.nan,3],'b':[0, 2, np.nan]},index =indexlist)
        dataSet["score"] = pd.DataFrame({'a':[1,np.nan,np.nan],'b':[np.inf, 2, 0]},index =indexlist)
        dataSet["featureKey"] = pd.DataFrame({'a':[1,np.nan,3],'b':[np.inf, 2, np. nan]},index =indexlist)
        dataSet["getDataDf"] = pd.DataFrame({'featureKey':[1,3.0,np.inf],'b':[np.inf, 2, np.inf]},index =indexlist)
        dataSet["dict"]={'a':0,'b':1}
        ##############################################
        parameters["predictionKey"] = "predictionKey"
        parameters["target"]="target"
        parameters["instrument_score_feature"]="score"
        ##############################################
        results["score_logless_Instrument"]=pd.Series({'a':0.0,'b':0.0})
        results["score_logless_Market"]=0.0
#### sample data
    if(c==2):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30')]
        dataSet["predictionKey"]=pd.DataFrame({'a':[1],'b':[0.2],'c':[0.8],'d':[0.0],'e':[0.5]},index =indexlist)
        dataSet["target"]=pd.DataFrame({'a':[1],'b':[2],'c':[3],'d':[4],'e':[5]},index =indexlist)
        dataSet["score"]=pd.DataFrame({'a':[0.5],'b':[0.2],'c':[0.8],'d':[1.0],'e':[0.0]},index =indexlist)
        dataSet["featureKey"]=pd.DataFrame({'a':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        dataSet["getDataDf"]=pd.DataFrame({'featureKey':[3.14],'b':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        dataSet["dict"]={'a':0,'b':1,'c':2,'d':3,'e':4}
        ##############################################
        parameters["predictionKey"] = "predictionKey"
        parameters["target"]="target"
        parameters["instrument_score_feature"]="score"
        ##############################################
        results["score_logless_Instrument"]=pd.Series({'a':1.570,'b':2.518,'c':-0.765,'d':0.490,'e':-0.178})
        results["score_logless_Market"]=0.5
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
        dataSet["predictionKey"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        dataSet["target"]=pd.DataFrame({'a':[1,2,3,4,5,6,7,8,9],'b':[9,8,7,6,5,4,3,2,1]},index=indexlist)
        dataSet["score"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        dataSet["featureKey"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["getDataDf"]=pd.DataFrame({'featureKey':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["dict"]={'a':0,'b':1}
        ##############################################
        parameters["predictionKey"] = "predictionKey"
        parameters["target"]="target"
        parameters["instrument_score_feature"]="score"
        ##############################################
        results["score_logless_Instrument"]=pd.Series({'a':4.227,'b':0.398})
        results["score_logless_Market"]=0.4
#### updateNum is zero
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
        dataSet["predictionKey"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        dataSet["target"]=pd.DataFrame({'a':[1,2,3,4,5,6,7,8,9],'b':[9,8,7,6,5,4,3,2,1]},index=indexlist)
        dataSet["score"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        dataSet["featureKey"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["getDataDf"]=pd.DataFrame({'featureKey':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["dict"]={'a':0,'b':1}
        ##############################################
        parameters["predictionKey"] = "predictionKey"
        parameters["target"]="target"
        parameters["instrument_score_feature"]="score"
        ##############################################
        results["score_logless_Instrument"]=pd.Series({'a':0,'b':0})
        results["score_logless_Market"]=0.4
#### dict dataSet is empty
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
        dataSet["predictionKey"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        dataSet["target"]=pd.DataFrame({'a':[1,2,3,4,5,6,7,8,9],'b':[9,8,7,6,5,4,3,2,1]},index=indexlist)
        dataSet["score"]=pd.DataFrame({'a':[0.2,0.01,0.8,0.9,0.5,0.55,0.6,0.7,0.3],'b':[0.1,0.8,0.6,0.4,0.7,0.9,0.9,0.1,0.5]},index=indexlist)
        dataSet["featureKey"]=pd.DataFrame({'a':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
        dataSet["getDataDf"]=pd.DataFrame({'featureKey':[3.14,2.08,-5.24,1.02,8.56,-1.42,0.24,5.02,2.35],'b':[1.08,1.04,5.24,-3.03,5.12,-7.00,5.01,1.02,0.25]},index=indexlist)
######## dict is empty
        dataSet["dict"]={}
        ##############################################
        parameters["predictionKey"] = "predictionKey"
        parameters["target"]="target"
        parameters["instrument_score_feature"]="score"
        ##############################################
        results["score_logless_Instrument"]=pd.Series({'a':3.476,'b':0.339})
        results["score_logless_Market"]=0.8

    return {"dataSet":dataSet, "parameters":parameters, "results":results}
