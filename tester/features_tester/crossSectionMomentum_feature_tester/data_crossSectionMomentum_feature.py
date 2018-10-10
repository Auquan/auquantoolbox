import pandas as pd
import numpy as np
def getDataSet(c):
    dataSet={}
    parameters={}
    results={}
#### empty datasets
#### logging IndexErrors
    if(c==0):
        dataSet["df1"]=pd.DataFrame({'featureName':[]})
        dataSet["df2"]=pd.DataFrame({'featureName':[]})
        dataSet["df3"]=pd.DataFrame({'featureName':[]})
        dataSet["df4"]=pd.DataFrame({'featureName':[]})
        dataSet["df5"]=pd.DataFrame({'featureName':[]})
        dataSet["df6"]=pd.DataFrame({'featureName':[]})
        ##############################################
        parameters["featureName"]="featureName"
        parameters["period"]=1
        ##############################################
        results["crossSectionMomentum"]= pd.Series({'one':0.0,'two':0.0,'three':0.0,'four':0.0,'five':0.0,'six':0.0})
#### data has nans and infs
    if(c==1):
        dataSet["df1"]=pd.DataFrame({'featureName':[1.0,np.nan,np.inf,-np.inf]})
        dataSet["df2"]=pd.DataFrame({'featureName':[1.0,3.0,np.inf,7.0]})
        dataSet["df3"]=pd.DataFrame({'featureName':[-np.inf,5.0,np.nan,6.0]})
        dataSet["df4"]=pd.DataFrame({'featureName':[np.nan,np.inf,1.0,-np.inf]})
        dataSet["df5"]=pd.DataFrame({'featureName':[18.0,16.0,14.0,12.0]})
        dataSet["df6"]=pd.DataFrame({'featureName':[11.0,14.0,np.inf,3.0]})
        ##############################################
        parameters["featureName"]="featureName"
        parameters["period"]=1
        ##############################################
        results["crossSectionMomentum"]= pd.Series({'one':-0.287,'two':0.463,'three':-0.287,'four':-0.287,'five':0.368,'six':0.031})
#### testing for dataSet with len 1
#### logging IndexError
    if(c==2):
        dataSet["df1"]=pd.DataFrame({'featureName':[1.0]})
        dataSet["df2"]=pd.DataFrame({'featureName':[1.0]})
        dataSet["df3"]=pd.DataFrame({'featureName':[8.0]})
        dataSet["df4"]=pd.DataFrame({'featureName':[9.0]})
        dataSet["df5"]=pd.DataFrame({'featureName':[18.0]})
        dataSet["df6"]=pd.DataFrame({'featureName':[11.0]})
        ##############################################
        parameters["featureName"]="featureName"
        parameters["period"]=1
        ##############################################
        results["crossSectionMomentum"]= pd.Series({'one':0.0,'two':0.0,'three':0.0,'four':0.0,'five':0.0,'six':0.0})
#### period is 0, converts the series to nans, returning 0 back
    if(c==3):
        dataSet["df1"]=pd.DataFrame({'featureName':[1,2,3,4,5,6,7,8,9]})
        dataSet["df2"]=pd.DataFrame({'featureName':[1,3,5,7,9,11,13,15,17]})
        dataSet["df3"]=pd.DataFrame({'featureName':[8,5,2,6,5,4,7,9,0]})
        dataSet["df4"]=pd.DataFrame({'featureName':[9,5,1,7,5,3,8,4,2]})
        dataSet["df5"]=pd.DataFrame({'featureName':[18,16,14,12,10,8,6,4,2]})
        dataSet["df6"]=pd.DataFrame({'featureName':[11,14,17,3,6,9,2,5,8]})
        ##############################################
        parameters["featureName"]="featureName"
        parameters["period"]=0
        ##############################################
        results["crossSectionMomentum"]= pd.Series({'one':0.019,'two':0.019,'three':-0.093,'four':0.019,'five':0.019,'six':0.019})
#### sample test
    if(c==4):
        dataSet["df1"]=pd.DataFrame({'featureName':[1,2,3,4,5,6,7,8,9]})
        dataSet["df2"]=pd.DataFrame({'featureName':[1,3,5,7,9,11,13,15,17]})
        dataSet["df3"]=pd.DataFrame({'featureName':[8,5,2,6,5,4,7,9,0]})
        dataSet["df4"]=pd.DataFrame({'featureName':[9,5,1,7,5,3,8,4,2]})
        dataSet["df5"]=pd.DataFrame({'featureName':[18,16,14,12,10,8,6,4,2]})
        dataSet["df6"]=pd.DataFrame({'featureName':[11,14,17,3,6,9,2,5,8]})
        ##############################################
        parameters["featureName"]="featureName"
        parameters["period"]=1
        ##############################################
        results["crossSectionMomentum"]= pd.Series({'one':0.064,'two':0.211,'three':-0.161,'four':0.288,'five':-0.441,'six':0.038})
#### period is 11, more than the length of the series, converts the series to nans, returning 0 back
    if(c==5):
        dataSet["df1"]=pd.DataFrame({'featureName':[1,2,3,4,5,6,7,8,9]})
        dataSet["df2"]=pd.DataFrame({'featureName':[1,3,5,7,9,11,13,15,17]})
        dataSet["df3"]=pd.DataFrame({'featureName':[8,5,2,6,5,4,7,9,0]})
        dataSet["df4"]=pd.DataFrame({'featureName':[9,5,1,7,5,3,8,4,2]})
        dataSet["df5"]=pd.DataFrame({'featureName':[18,16,14,12,10,8,6,4,2]})
        dataSet["df6"]=pd.DataFrame({'featureName':[11,14,17,3,6,9,2,5,8]})
        ##############################################
        parameters["featureName"]="featureName"
        parameters["period"]=3
        ##############################################
        results["crossSectionMomentum"]= pd.Series({'one':0.532,'two':0.968,'three':-0.205,'four':-0.130,'five':-0.616,'six':-0.549})
    return {"dataSet":dataSet, "parameters":parameters, "results":results}
