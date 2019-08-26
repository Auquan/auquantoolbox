import pandas as pd
from datetime import datetime, time, timedelta
from backtester.instrumentUpdates import *

def data_logfile_data_source(c):
    dataSet={}
    parameters={}
    results={}

    if c==0:
######## testing for LogFileDataSource Class
        parameters["fileName"]="Folder1/text.txt"
        parameters["liveUpdates"]=True
######## testing for processLineIntoInstrumentUpdates
        parameters["line"]="ABC"
        results["line"]="ABC"
######## testing for processLine
        results["getFutureInstrumentId"]="AAG"
        results["getTypeOfInstrument"]="future"
        results["getExpiryTime"]=datetime(2018, 2, 1, 0, 0)
        results["getUnderlyingInstrumentId"]='NA'
        parameters["folderName"]='Folder1/'

    if c==1:
######## testing for LogFileDataSource Class
        parameters["fileName"]="Folder1/text.txt"
        parameters["liveUpdates"]=False
######## testing for processLineIntoInstrumentUpdates
        parameters["line"]="DEF"
        results["line"]="DEF"
        parameters["folderName"]='Folder1/'

    return {"dataSet":dataSet,"parameters":parameters,"results":results}
