import pandas as pd
import datetime
def data_quant_quest_time_rule(c):
    parameters={}
    results={}
    if c==0:
        parameters["cachedFolderName"]='Folder1/'
######## downloading data from github repository
        parameters["dataSetId"]='trainingW5_trainingData'
######## for ensureDirectoryExists
        parameters["testcachedFolderName"]='test_folder1/'
        parameters["testdataSetId"]='test_folder2'
######## for getFileName
        results["getFileName"]="Folder1/trainingW5_trainingData/date_list.txt"
######## for downloadFile
        parameters["dataSetIdfordownloadFile"]='trainingW5_trainingData'
        parameters["downloadLocation"]='Folder1/trainingW5_trainingData/data.txt'
        results["downloadFile"]=True
######## for emitTimeToTrade
        parameters["fileName"]="Folder1/trainingW5_trainingData/date_list.txt"
######## random time points from a list of lenght 373
######## the list contains all the time points of date 2017-09-15
        results["emitTimeToTrade"]=[datetime.datetime(2017, 9, 15, 9, 17),
                                    datetime.datetime(2017, 9, 15, 9, 27),
                                    datetime.datetime(2017, 9, 15, 10, 7),
                                    datetime.datetime(2017, 9, 15, 10, 57),
                                    datetime.datetime(2017, 9, 15, 12, 37),
                                    datetime.datetime(2017, 9, 15, 13, 27),
                                    datetime.datetime(2017, 9, 15, 14, 17),
                                    datetime.datetime(2017, 9, 15, 15, 7),
                                    datetime.datetime(2017, 9, 15, 15, 29)]
    if c==1:
        parameters["cachedFolderName"]='Folder1/'
######## downloading data from github repository
        parameters["dataSetId"]='trainingW5_trainingData'
######## for ensureDirectoryExists
        parameters["testcachedFolderName"]='test_folder1/'
        parameters["testdataSetId"]='test_folder2'
######## for getFileName
        results["getFileName"]="Folder1/trainingW5_trainingData/date_list.txt"
######## for downloadFile
######## wrong file name to test downloadFile
        parameters["dataSetIdfordownloadFile"]='abc'
        parameters["downloadLocation"]='Folder1/trainingW5_trainingData/data.txt'
        results["downloadFile"]=False
######## for emitTimeToTrade
######## if the url is not right it will yield an empty generator
        results["emitTimeToTrade"]=[]
    return {"parameters":parameters,"results":results}
