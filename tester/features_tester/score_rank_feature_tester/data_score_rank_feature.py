import pandas as pd
import numpy as np
def getDataSet(c):
    dataSet={}
    parameters={}
    results={}
#### empty datasets
#### logging IndexErrors
    if(c==0):
        dataSet["getDataDf"]=pd.DataFrame({"featureKey":[],"predictionKey":[]})
        dataSet["df1"]=pd.DataFrame({'price':[]})
        dataSet["df2"]=pd.DataFrame({'price':[]})
        dataSet["df3"]=pd.DataFrame({'price':[]})
        ##############################################
        parameters["price"] = "price"
        parameters["predictionKey"] = "predictionKey"
        ##############################################
        results["score_rank_Market"]=0.0
#### data includes nans and infs
    if(c==1):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30'),pd.tslib.Timestamp('2017-01-03 10:30:30'),pd.tslib.Timestamp('2017-01-03 11:30:30'),pd.tslib.Timestamp('2017-01-03 12:30:30')]
        dataSet["getDataDf"] = pd.DataFrame({'featureKey':[1,3.0,np.inf,np.nan],'predictionKey':[np.inf, 2, np.inf,1.0]},index =indexlist)
        dataSet["df1"]=pd.DataFrame({'price':[np.inf,-np.inf,5.12,8.00]},index =indexlist)
        dataSet["df2"]=pd.DataFrame({'price':[7.89,7.02,np.inf,5.02]},index =indexlist)
        dataSet["df3"]=pd.DataFrame({'price':[0.00,0.00,0.00,0.00]},index =indexlist)
        ##############################################
        parameters["price"] = "price"
        parameters["predictionKey"] = "predictionKey"
        ##############################################
        results["score_rank_Market"]=0.5
#### sample data
    if(c==2):
        indexlist=[pd.tslib.Timestamp('2017-01-03 09:30:30')]
        dataSet["getDataDf"]=pd.DataFrame({'featureKey':[3.14],'predictionKey':[2.04],'c':[1.02],'d':[0.98],'e':[-1.05]},index =indexlist)
        dataSet["df1"]=pd.DataFrame({'price':[3.0]},index=indexlist)
        dataSet["df2"]=pd.DataFrame({'price':[4.56]},index=indexlist)
        dataSet["df3"]=pd.DataFrame({'price':[1.23]},index=indexlist)
        ##############################################
        parameters["price"] = "price"
        parameters["predictionKey"] = "predictionKey"
        ##############################################
        results["score_rank_Market"]=0.0
    if(c==3):
        indexlist=  [pd.tslib.Timestamp('2017-01-03 09:30:30'),
                     pd.tslib.Timestamp('2017-01-03 10:00:30'),
                     pd.tslib.Timestamp('2017-01-03 10:30:30'),
                     pd.tslib.Timestamp('2017-01-03 11:00:30'),
                     pd.tslib.Timestamp('2017-01-03 11:30:30'),
                     pd.tslib.Timestamp('2017-01-03 12:00:30')]
        dataSet["getDataDf"]=pd.DataFrame({'featureKey':[3.14,2.08,-5.24,1.02,8.56,-1.42],'predictionKey':[1.08,1.04,5.24,-3.03,5.12,-7.00]},index=indexlist)
        dataSet["df1"]=pd.DataFrame({'price':[7.12,4.15,7.85,9.63,4.56,1.32]},index=indexlist)
        dataSet["df2"]=pd.DataFrame({'price':[7.19,8.88,4.14,7.99,9.99,1.11]},index=indexlist)
        dataSet["df3"]=pd.DataFrame({'price':[4.16,7.89,7.77,7.25,3.33,1.00]},index=indexlist)
        ##############################################
        parameters["price"] = "price"
        parameters["predictionKey"] = "predictionKey"
        ##############################################
        results["score_rank_Market"]=18.0
#### the data is same for df1, df2, df3, rank will be 0
    if(c==4):
        indexlist=  [pd.tslib.Timestamp('2017-01-03 09:30:30'),
                     pd.tslib.Timestamp('2017-01-03 10:00:30'),
                     pd.tslib.Timestamp('2017-01-03 10:30:30'),
                     pd.tslib.Timestamp('2017-01-03 11:00:30'),
                     pd.tslib.Timestamp('2017-01-03 11:30:30'),
                     pd.tslib.Timestamp('2017-01-03 12:00:30')]
        dataSet["getDataDf"]=pd.DataFrame({'featureKey':[3.14,2.08,-5.24,1.02,8.56,-1.42],'predictionKey':[1.08,1.04,5.24,-3.03,5.12,-7.00]},index=indexlist)
        dataSet["df1"]=pd.DataFrame({'price':[4.16,7.89,7.77,7.25,3.33,1.00]},index=indexlist)
        dataSet["df2"]=pd.DataFrame({'price':[4.16,7.89,7.77,7.25,3.33,1.00]},index=indexlist)
        dataSet["df3"]=pd.DataFrame({'price':[4.16,7.89,7.77,7.25,3.33,1.00]},index=indexlist)
        ##############################################
        parameters["price"] = "price"
        parameters["predictionKey"] = "predictionKey"
        ##############################################
        results["score_rank_Market"]=0.0
    if(c==5):
        indexlist=  [pd.tslib.Timestamp('2017-01-03 09:30:30'),
                     pd.tslib.Timestamp('2017-01-03 10:00:30'),
                     pd.tslib.Timestamp('2017-01-03 10:30:30'),
                     pd.tslib.Timestamp('2017-01-03 11:00:30'),
                     pd.tslib.Timestamp('2017-01-03 11:30:30'),
                     pd.tslib.Timestamp('2017-01-03 12:00:30')]
        dataSet["getDataDf"]=pd.DataFrame({'featureKey':[3.14,2.08,-5.24,1.02,8.56,-1.42],'predictionKey':[1.08,1.04,5.24,-3.03,5.12,-7.00]},index=indexlist)
        dataSet["df1"]=pd.DataFrame({'price':[7.12,4.15,7.85,9.63,4.56,1.32]},index=indexlist)
        dataSet["df2"]=pd.DataFrame({'price':[7.19,8.88,4.14,7.99,9.99,1.11]},index=indexlist)
        dataSet["df3"]=pd.DataFrame({'price':[4.16,7.89,7.77,7.25,3.33,1.00]},index=indexlist)
        ##############################################
        parameters["price"] = "price"
        parameters["predictionKey"] = "predictionKey"
        ##############################################
        results["score_rank_Market"]=0.0

    return {"dataSet":dataSet, "parameters":parameters, "results":results}
