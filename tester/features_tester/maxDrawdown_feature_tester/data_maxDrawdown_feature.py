import pandas as pd
import numpy as np
def getDataSet(c):
    dataSet={}
    parameters={}
    results={}
#### no element in the dataSet, will return 0
    if(c==0):
        parameters["portfolioValueKey"] = "portfolio_value"
        ##############################################
        results["maxDrawdown_Market"]=0
#### empty dataSet, will return 0
    if(c==1):
        dataSet["featureKey"]=pd.Series()
        dataSet["portfolio_value"]=pd.Series()
        ##############################################
        parameters["portfolioValueKey"] = "portfolio_value"
        ##############################################
        results["maxDrawdown_Market"]={'maxPortfolioValue': 0, 'maxDrawdown': 0}
#### only one element in portfolio_value, will return dict with 0s
    if(c==2):
        dataSet["featureKey"]=pd.Series()
        dataSet["portfolio_value"]=pd.Series([1])
        ##############################################
        parameters["portfolioValueKey"] = "portfolio_value"
        ##############################################
        results["maxDrawdown_Market"]={'maxPortfolioValue': 0, 'maxDrawdown': 0}
#### no element in featureKey, will return dict with 0s
    if(c==3):
        dataSet["featureKey"]=pd.Series()
        dataSet["portfolio_value"]=pd.Series([1,2,3,4])
        ##############################################
        parameters["portfolioValueKey"] = "portfolio_value"
        ##############################################
        results["maxDrawdown_Market"]={'maxPortfolioValue': 0, 'maxDrawdown': 0}
#### wrong key used, will return dict with 0s
    if(c==4):
        dataSet["featureKey"]=pd.Series({0:{'wrongmaxPortfolioValue': 5.85 , 'maxDrawdown': 10.01},1:{'wrongmaxPortfolioValue': 0.95 , 'wrongmaxDrawdown': 1.56}})
        dataSet["portfolio_value"]=pd.Series([1,2,3,4])
        ##############################################
        parameters["portfolioValueKey"] = "portfolio_value"
        ##############################################
        results["maxDrawdown_Market"]={'maxPortfolioValue': 0, 'maxDrawdown': 0}
#### wrong key used, will return dict with 0s
    if(c==5):
        dataSet["featureKey"]=pd.Series({0:{'maxPortfolioValue': 5.85 , 'wrongmaxDrawdown': 10.01},1:{'maxPortfolioValue': 0.95 , 'wrongmaxDrawdown': 1.56}})
        dataSet["portfolio_value"]=pd.Series([1,2,3,4])
        ##############################################
        parameters["portfolioValueKey"] = "portfolio_value"
        ##############################################
        results["maxDrawdown_Market"]={'maxPortfolioValue': 0, 'maxDrawdown': 0}
#### sample data
    if(c==6):
        dataSet["featureKey"]=pd.Series({0:{'maxPortfolioValue': 5.85,'maxDrawdown': 10.01}, 1:{'maxPortfolioValue':0.95,'maxDrawdown': 1.56}})
        dataSet["portfolio_value"]=pd.Series([1,2,3,4])
        ##############################################
        parameters["portfolioValueKey"] = "portfolio_value"
        ##############################################
        results["maxDrawdown_Market"]={'maxPortfolioValue': 5.85, 'maxDrawdown': 10.01}
#### sample data
    if(c==7):
        dataSet["featureKey"]=pd.Series({0:{'maxPortfolioValue': 2.02,'maxDrawdown': -1.25}, 1:{'maxPortfolioValue':0.95,'maxDrawdown': 1.56}})
        dataSet["portfolio_value"]=pd.Series([1,2,3,4])
        ##############################################
        parameters["portfolioValueKey"] = "portfolio_value"
        ##############################################
        results["maxDrawdown_Market"]={'maxPortfolioValue': 4, 'maxDrawdown': 0}
    return {"dataSet":dataSet, "parameters":parameters, "results":results}
