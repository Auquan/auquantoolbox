import pandas as pd
import numpy as np
import time
import os
from datetime import datetime, time, timedelta
from pandas.tseries.holiday import Holiday, AbstractHolidayCalendar
from backtester.instrumentUpdates import *

def data_auquan_data_source(c):
    dataSet={}
    parameters={}
    results={}

    if c==0:
######## testing for checkDate
        parameters["lineItem"]="2018/01/01"
        results["checkDate"]=True
######## testing for checkTimestamp
        results["checkTimestamp"]=True
######## testing for validateLineItem
        parameters["lineItems"]=["2018/01/01"]
        results["validateLineItem"]=0
######## testing for parseBookDataOptionLine
        results["parseBookDataOptionLine"]=None
######## testing for get_exp_date
        parameters["trade_date"]=datetime.strptime("1/1/2018","%m/%d/%Y")
        results["get_exp_date"]=datetime(2018, 1, 25, 15, 30)
######## testing for InstrumentFromFile Class
        parameters["fileName"]="Folder1/text.txt"
        parameters["instrumentId"]="AAE"
        parameters["expiryTime"]=datetime.strptime("1/9/2018","%m/%d/%Y")
######## testing for processLine
        parameters["line"]=""
        results["countforprocessLine"]=1
######## testing for processLinesIntoInstruments
        results["countforprocessLinesIntoInstruments"]=0
######## testing for AuquanDataSource Class
        parameters["folderName"]="Folder1/"
        parameters["instrumentIdsByType"]={'a':["AAE","AGG"],'b':["BBA","BPM"]}
        parameters["startDateStr"]="2018/01/01"
        parameters["endDateStr"]="2018/01/02"
        parameters["liveUpdates"]=True
######## testing for getFileName
        parameters["instrumentType"]='a'
        parameters["instrumentId"]='GOOG'
        parameters["date"]=datetime.strptime("1/1/2018","%m/%d/%Y")
        results["getFileName"]="Folder1//a/GOOG/GOOG_20180101.txt"
######## testing for emitInstrumentUpdates
        results["emitInstrumentUpdates"]=[datetime(2016, 1, 1, 9, 30), datetime(2017, 1, 1, 9, 30), datetime(2018, 1, 1, 9, 30)]
        results["countforemitInstrumentUpdates"]=3
        results["listFutureInstrumentId"]=['BPM', 'BBA', 'BBA']
        results["listTypeOfInstrument"]=['future', 'future', 'future']
        results["listExpiryTime"]=[datetime(2018, 1, 25, 15, 30), datetime(2018, 1, 25, 15, 30), datetime(2018, 1, 25, 15, 30)]
        results["listUnderlyingInstrumentId"]=['NA', 'NA', 'NA']

    if c==1:
######## testing for checkDate
        parameters["lineItem"]="2018/01/"
        results["checkDate"]=False
######## testing for checkTimestamp
        results["checkTimestamp"]=True
######## testing for validateLineItem
        parameters["lineItems"]=["2018/01/01","09:30:00","Book",100,"AAA"]
        results["validateLineItem"]=1
######## testing for parseBookDataOptionLine
        results["parseBookDataOptionLine"]=None
######## testing for get_exp_date
        parameters["trade_date"]=datetime.strptime("12/15/2018","%m/%d/%Y")
        results["get_exp_date"]=datetime(2018, 12, 27, 15, 30)
######## testing for InstrumentFromFile Class
        parameters["fileName"]="Folder1/text.txt"
        parameters["instrumentId"]="AAE"
        parameters["expiryTime"]=datetime.strptime("1/9/2018","%m/%d/%Y")
######## testing for processLine
        parameters["line"]="2017/01/01 09:30:00:000000 Book 100 AAA\n2018/01/01 09:30:00:000000 Book 100 AAA\n2019/01/01 09:30:00:000000 Book 100 AAA"
        results["countforprocessLine"]=3
######## testing for processLinesIntoInstruments
        results["countforprocessLinesIntoInstruments"]=3
######## testing for AuquanDataSource Class
        parameters["folderName"]="Folder1/"
        parameters["instrumentIdsByType"]={'a':["AAE","AGG"],'b':["BBA","BPM"]}
        parameters["startDateStr"]="2018/01/01"
        parameters["endDateStr"]="2018/01/02"
        parameters["liveUpdates"]=False
######## testing for getFileName
        parameters["instrumentType"]='a'
        parameters["instrumentId"]='GOOG'
        parameters["date"]=datetime.strptime("1/1/2018","%m/%d/%Y")
        results["getFileName"]="Folder1//a/GOOG/GOOG_20180101.txt"
######## testing for emitInstrumentUpdates
        results["emitInstrumentUpdates"]=[]
        results["countforemitInstrumentUpdates"]=0
        results["listFutureInstrumentId"]=[]
        results["listTypeOfInstrument"]=[]
        results["listExpiryTime"]=[]
        results["listUnderlyingInstrumentId"]=[]

    if c==2:
######## testing for validateLineItem
        parameters["lineItems"]=["2018/01/01","09:30:00","Greek:",100,100]
        results["validateLineItem"]=2
######## testing for parseBookDataOptionLine
        results["parseBookDataOptionLine"]=None
######## testing for get_exp_date
        parameters["trade_date"]=datetime.strptime("12/31/2018","%m/%d/%Y")
        results["get_exp_date"]=datetime(2019, 1, 31, 15, 30)
######## testing for InstrumentFromFile Class
        parameters["fileName"]="Folder1/text.txt"
        parameters["instrumentId"]="AAE"
        parameters["expiryTime"]=datetime.strptime("1/9/2018","%m/%d/%Y")
######## testing for processLine
        parameters["line"]="2018/01/01 100 50 | 200 100 ABC"
        results["countforprocessLine"]=1
        results["currentBookData"]={'bidVolume': 100.0, 'askPrice': 200.0, 'bidPrice': 50.0, 'askVolume': 100.0}
######## testing for processLinesIntoInstruments
        results["countforprocessLinesIntoInstruments"]=0
        parameters["folderName"]="Folder1/"

    if c==3:
######## testing for validateLineItem
        parameters["lineItems"]=["2018/01/01",100,50,"|",200,100,"ABC"]
        results["validateLineItem"]=3
######## testing for parseBookDataOptionLine
        results["parseBookDataOptionLine"]={'bidVolume': 100.0, 'askPrice': 200.0, 'bidPrice': 50.0, 'askVolume': 100.0}
######## testing for get_exp_date
        parameters["trade_date"]=datetime.strptime("10/06/2016","%m/%d/%Y")
        results["get_exp_date"]=datetime(2016, 10, 27, 15, 30)

    if c==4:
######## testing for validateLineItem
        parameters["lineItems"]=["2018/01/01",100,50,"&",200,100]
        results["validateLineItem"]=0
######## testing for parseBookDataOptionLine
        results["parseBookDataOptionLine"]=None
######## testing for get_exp_date
        parameters["trade_date"]=datetime.strptime("09/13/2016","%m/%d/%Y")
        results["get_exp_date"]=datetime(2016, 9, 29, 15, 30)

    return {"dataSet":dataSet,"parameters":parameters,"results":results}
