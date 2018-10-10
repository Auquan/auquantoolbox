import pandas as pd
import numpy as np
def getDataSet(c):
    dataSet={}
    parameters={}
    results={}
#### empty datasets
#### logging IndexErrors
    if(c==0):
        dataSet["currentMarketFeatures"] = {}
        ##############################################
        parameters["pnl"]="pnl"
        parameters["initial_capital"] = 0.0
        ##############################################
        results["portfoliovalue_Market"]=None
#### no pnl key defined, will give KeyError
    if(c==1):
        dataSet["currentMarketFeatures"]={'pnl':5}
        ##############################################
        parameters["initial_capital"] = 0.0
        ##############################################
        results["portfoliovalue_Market"]=None
#### sample data
    if(c==2):
        dataSet["currentMarketFeatures"]={'pnl':5}
        ##############################################
        parameters["pnl"]="pnl"
        parameters["initial_capital"] = 0.0
        ##############################################
        results["portfoliovalue_Market"]=5.0
#### sample data
    if(c==3):
        dataSet["currentMarketFeatures"] = {'pnl':5}
        ##############################################
        parameters["pnl"]="pnl"
        parameters["initial_capital"] =10
        ##############################################
        results["portfoliovalue_Market"]=15
    return {"dataSet":dataSet, "parameters":parameters, "results":results}
