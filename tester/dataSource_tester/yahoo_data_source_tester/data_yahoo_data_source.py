import pandas as pd
import numpy as np
import time
import os
from datetime import datetime, time, timedelta
from backtester.instrumentUpdates import *

def data_yahoo_data_source(c):
    dataSet={}
    parameters={}
    results={}

    if c==0:
        parameters["lineItem"]="2018/01/01"
        results["checkDate"]=False
        parameters["lineItems"]=["2018/01/01"]
        results["validateLineItem"]=0
        results["parseDataLine"]=None
        parameters["s"]=9
        results["isFloat"]=9.0
        results["is_number"]=True
        parameters["cachedFolderName"]='yahooData/'
        parameters["dataSetId"]="testTrading"
        parameters["instrumentIds"]=['IBM', 'AAPL']
        parameters["startDateStr"]='2017/12/21'
        parameters["endDateStr"]='2018/01/31'
        parameters["event"]="history"
        parameters["adjustPrice"]=False
        parameters["downloadId"]=".SN"
        parameters["liveUpdates"]=True
        parameters["pad"]=True
        

    if c==1:
        parameters["lineItem"]="2018/01/"
        results["checkDate"]=False
        parameters["lineItems"]=["2018/01/01","09:30:00","Book",100,"AAA"]
        results["validateLineItem"]=0
        results["parseDataLine"]=None
        parameters["s"]="abc"
        results["isFloat"]=False
        results["is_number"]=False
        

    if c==2:
        parameters["lineItem"]="2018/01/01"
        results["checkDate"]=False
        parameters["lineItems"]=["2018/01/01","09:30:00","Greek:",100,100]
        results["validateLineItem"]=0
        results["parseDataLine"]=None
        parameters["s"]=90.00
        results["isFloat"]=90.0
        results["is_number"]=True
        
        
    if c==3:
        parameters["lineItem"]="2018/01/01"
        results["checkDate"]=False
        parameters["lineItems"]=["2018/01/01",100,50,"|",200,100,"ABC"]
        results["validateLineItem"]=0
        


    return {"dataSet":dataSet,"parameters":parameters,"results":results}

