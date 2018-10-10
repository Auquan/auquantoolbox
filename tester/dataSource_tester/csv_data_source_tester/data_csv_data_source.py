from backtester.instrumentUpdates import *

def data_csv_data_source(c):
    dataSet={}
    parameters={}
    results={}

    if c==0:
######## testing for is_number
        parameters["s"]=1
        results["is_number"]=True
######## testing for CSVDataSource Class
        parameters["cachedFolderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["instrumentIds"]=["AAE","AGG"]
        parameters["downloadUrl"]="https://raw.githubusercontent.com/Auquan/test_repo/master"
        parameters["timeKey"]='datetime'
        parameters["timeStringFormat"]="%Y-%m-%d %H:%M:%S"
        parameters["startDateStr"]="2018/01/01"
        parameters["endDateStr"]="2018/02/01"
        # liveUpdates is True
        parameters["liveUpdates"]=True
        # pad is True
        parameters["pad"]=True
######## testing for getFileName
        parameters["instrumentId"]="BYB"
        results["getFileName"]="Folder1/QQ3Data/BYB.csv"
######## testing for ensureAllInstrumentsFile
        results["ensureAllInstrumentsFile"]=True
######## testing for getAllInstrumentIds
        results["getAllInstrumentIds"]=['SIZ', 'MLQ', 'MAI', 'PVV', 'IPV', 'DHP', 'EKA', 'WTX', 'EYC', 'YSB', 'SEP', 'INS', 'IIZ', 'DFY', 'OAX', 'HIS',
                                        'QZO', 'ZSB', 'SXH', 'CUY', 'GYQ', 'ARD', 'YCY', 'FXQ', 'CJV', 'OJF', 'DDV', 'EEN', 'SSD', 'FWX', 'AWU', 'ONS',
                                        'KEH', 'ZHU', 'HNM', 'LTN', 'ZKF', 'SJB', 'WCJ', 'JBP', 'EGP', 'FVA', 'JHB', 'AKK', 'QON', 'URZ', 'CAW', 'OSF',
                                        'TDW', 'KMY', 'ATN', 'MLP', 'EMD', 'AGM', 'QCE', 'HRY', 'BPM', 'MPC', 'DIZ', 'GWI', 'FVB', 'DZU', 'GQX', 'WMN',
                                        'ENQ', 'DJV', 'WBM', 'ORH', 'YAE', 'BYZ', 'YXP', 'SLM', 'NMS', 'WJP', 'DGT', 'KCN', 'WWV', 'GOR', 'ZMP', 'QCM',
                                        'VML', 'XZC', 'AJM', 'NLF', 'NTG', 'NSN', 'CSI', 'PES', 'OIL', 'SJL', 'ZFC', 'BST', 'DLL', 'AAE', 'OLY', 'VIC',
                                        'QZU', 'DOE', 'GUY', 'BBA', 'YSL', 'ZGR', 'AGG', 'AQM', 'LUY', 'SNF', 'UNB', 'ZRN', 'VSV', 'SSL', 'VUV', 'ZQY',
                                        'RCL', 'EXR', 'BYB']
######## testing for downloadFile
        parameters["getFileName"]="Folder1/QQ3Data/BYB.csv"
        results["downloadFile"]=True
######## testing for downloadAndAdjustData
        results["downloadAndAdjustData"]=True
######## testing for getInstrumentUpdateFromRow
        dataSet["records"]=  [{'datetime': '2011-02-21 14:55:00'},
                              {'datetime': '2011-02-21 15:00:00'},
                              {'datetime': '2011-02-21 15:05:00'},
                              {'datetime': '2011-02-21 15:10:00'}]
        results["count"]=4
        results["listStockInstrumentId"]=['BYB', 'BYB', 'BYB', 'BYB']
        results["listTypeOfInstrument"]=['stock', 'stock', 'stock', 'stock']

    if c==1:
######## testing for is_number
        parameters["s"]=1.00
        results["is_number"]=True
######## testing for CSVDataSource Class
        parameters["cachedFolderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["instrumentIds"]=["AAE","AGG"]
        parameters["downloadUrl"]="https://raw.githubusercontent.com/Auquan/test_repo/master"
        parameters["timeKey"]='datetime'
        parameters["timeStringFormat"]="%Y-%m-%d %H:%M:%S"
        parameters["startDateStr"]="2018/01/01"
        parameters["endDateStr"]="2018/02/01"
        # liveUpdates is False
        parameters["liveUpdates"]=False
        # pad is True
        parameters["pad"]=True
        parameters["instrumentId"]="MAI"
######## testing for getFileName
        parameters["getFileName"]="Folder1/QQ3Data/MAI.csv"
######## testing for downloadFile
        results["downloadFile"]=True
######## testing for downloadAndAdjustData
        results["downloadAndAdjustData"]=True
######## testing for getInstrumentUpdateFromRow
        dataSet["records"]=[]
        results["count"]=0
        results["listStockInstrumentId"]=[]
        results["listTypeOfInstrument"]=[]

    if c==2:
######## testing for is_number
        parameters["s"]='a'
        results["is_number"]=False
######## testing for CSVDataSource Class
        parameters["cachedFolderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["instrumentIds"]=["AAE","AGG"]
        parameters["downloadUrl"]="https://raw.githubusercontent.com/Auquan/test_repo/master"
        parameters["timeKey"]='datetime'
        parameters["timeStringFormat"]="%Y-%m-%d %H:%M:%S"
        parameters["startDateStr"]="2018/01/01"
        parameters["endDateStr"]="2018/02/01"
        # liveUpdates is False
        parameters["liveUpdates"]=False
        # pad is False
        parameters["pad"]=False
        parameters["instrumentId"]="PVA"
######## testing for getFileName
        parameters["getFileName"]="Folder1/QQ3Data/PVA.csv"
######## testing for downloadFile
        results["downloadFile"]=False
######## testing for downloadAndAdjustData
        results["downloadAndAdjustData"]=False

    if c==3:
######## testing for is_number
        parameters["s"]='a'
        results["is_number"]=False
######## testing for CSVDataSource Class
        parameters["cachedFolderName"]="Folder1/"
        # dataSetId is wrong
        parameters["dataSetId"]="QQ3"
        parameters["instrumentIds"]=["AAE","AGG"]
        parameters["downloadUrl"]="https://raw.githubusercontent.com/Auquan/test_repo/master"
        parameters["timeKey"]='datetime'
        parameters["timeStringFormat"]="%Y-%m-%d %H:%M:%S"
        parameters["startDateStr"]="2018/01/01"
        parameters["endDateStr"]="2018/02/01"
        parameters["liveUpdates"]=True
        parameters["pad"]=True
        results["ensureAllInstrumentsFile"]=False
        results["getAllInstrumentIds"]=[]
        parameters["instrumentId"]="PVV"
######## testing for getFileName
        parameters["getFileName"]="Folder1/QQ3Data/PVV.csv"
######## testing for downloadFile
        results["downloadFile"]=False
######## testing for downloadAndAdjustData
        results["downloadAndAdjustData"]=False

    if c==4:
######## testing for CSVDataSource Class
        parameters["cachedFolderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["instrumentIds"]=["BBA","BST"]
        parameters["downloadUrl"]="https://raw.githubusercontent.com/Auquan/test_repo/master"
        parameters["timeKey"]='datetime'
        parameters["timeStringFormat"]="%Y-%m-%d %H:%M:%S"
        parameters["startDateStr"]="2018/01/01"
        parameters["endDateStr"]="2018/02/01"
        parameters["liveUpdates"]=True
        parameters["pad"]=True

    if c==5:
######## testing for CSVDataSource Class
        parameters["cachedFolderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["instrumentIds"]=["QZO","QZU"]
        parameters["downloadUrl"]="https://raw.githubusercontent.com/Auquan/test_repo/master"
        parameters["timeKey"]='datetime'
        parameters["timeStringFormat"]="%Y-%m-%d %H:%M:%S"
        parameters["startDateStr"]="2018/01/01"
        parameters["endDateStr"]="2018/02/01"
        parameters["liveUpdates"]=True
        parameters["pad"]=True

    if c==6:
######## testing for CSVDataSource Class
        parameters["cachedFolderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        # QQQ instrumentId is wrong
        parameters["instrumentIds"]=["QZO","QQQ"]
        parameters["downloadUrl"]="https://raw.githubusercontent.com/Auquan/test_repo/master"
        parameters["timeKey"]='datetime'
        parameters["timeStringFormat"]="%Y-%m-%d %H:%M:%S"
        parameters["startDateStr"]="2018/01/01"
        parameters["endDateStr"]="2018/02/01"
        parameters["liveUpdates"]=True
        parameters["pad"]=True

    return {"dataSet":dataSet,"parameters":parameters,"results":results}
