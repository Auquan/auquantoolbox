import pandas as pd
from datetime import datetime, time, timedelta
from backtester.instrumentUpdates import *

def data_data_source_utils(c):
    dataSet={}
    parameters={}
    results={}

    if c==0:
######## testing for getCookieForYahoo
        parameters["instrumentId"]="GOOG"
######## testing for downloadFileFromYahoo
        parameters["fileName"]="Folder1/data.txt"
        parameters["startDate"]=datetime.strptime("1/1/2018","%m/%d/%Y")
        parameters["endDate"]=datetime.strptime("1/9/2018","%m/%d/%Y")
        parameters["event"]='history'
        results["downloadFileFromYahoo"]=True
        dataSet["str"]=['Date,Open,High,Low,Close,Adj Close,Volume\n',
                        '2018-01-02,1048.339966,1066.939941,1045.229980,1065.000000,1065.000000,1237600\n',
                        '2018-01-03,1064.310059,1086.290039,1063.209961,1082.479980,1082.479980,1430200\n',
                        '2018-01-04,1088.000000,1093.569946,1084.001953,1086.400024,1086.400024,1004600\n',
                        '2018-01-05,1094.000000,1104.250000,1092.000000,1102.229980,1102.229980,1279100\n',
                        '2018-01-08,1102.229980,1111.270020,1101.619995,1106.939941,1106.939941,1047600\n']
######## testing for groupAndSortByTimeUpdates
        parameters["datelist"]=[datetime.strptime("1/2/2018","%m/%d/%Y"),datetime.strptime("1/1/2018","%m/%d/%Y"),
                                datetime.strptime("1/4/2018","%m/%d/%Y"),datetime.strptime("1/3/2018","%m/%d/%Y"),
                                datetime.strptime("1/1/2018","%m/%d/%Y"),datetime.strptime("1/2/2018","%m/%d/%Y"),
                                datetime.strptime("1/3/2018","%m/%d/%Y"),datetime.strptime("1/4/2018","%m/%d/%Y")]
        parameters["InstrumentIdlist"]=["GOOG","APPL","IBM","DELL"]
        parameters["InstrumentTypelist"]=["stock","stock","stock","stock"]
        results["timeUpdates"]=[datetime(2018, 1, 1, 0, 0),
                                datetime(2018, 1, 2, 0, 0),
                                datetime(2018, 1, 3, 0, 0),
                                datetime(2018, 1, 4, 0, 0)]

        parameters["folderName"]="Folder1/"

    if c==1:
######## testing for getCookieForYahoo
        parameters["instrumentId"]="AAA"
######## testing for downloadFileFromYahoo
        parameters["fileName"]="Folder1/data.txt"
        parameters["startDate"]=datetime.strptime("1/1/2018","%m/%d/%Y")
        parameters["endDate"]=datetime.strptime("2/1/2018","%m/%d/%Y")
        parameters["event"]='history'
        results["downloadFileFromYahoo"]=True
        parameters["folderName"]="Folder1/"

    if c==2:
######## parameters for YahooStockDataSource used to test getMultipliers
        parameters["folderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["instrumentIds"]=['IBM', 'GOOG']
        parameters["startDateStr"]='2014/05/01'
        parameters["endDateStr"]='2014/11/30'
        parameters["event"]="history"
        parameters["liveUpdates"]=True
        parameters["startDate"]=datetime.strptime('2014/05/01',"%Y/%m/%d")
        parameters["endDate"]=datetime.strptime('2014/11/30',"%Y/%m/%d")
        parameters["instrumentId"]="GOOG"
        parameters["fileName"]="Folder1/data.txt"
        parameters["downloadId"]=".SN"
######## using random dates from the list and checking
        results['listmul']=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        results['listtemp']=[[0.0, 536.05249, 541.00525, 535.65668, 538.12109, 538.12109, 1794800.0],
                             [0.0, 562.81537, 573.43695, 561.92029, 567.97693, 567.97693, 1360400.0],
                             [0.0, 588.26538, 593.21814, 586.27637, 592.82037, 592.82037, 3746900.0],
                             [0.0, 554.94861, 556.8183, 551.98486, 555.784, 555.784, 1103100.0],
                             [0.0, 527.98682, 533.13849, 526.61438, 530.1748, 530.1748, 1657900.0],
                             [0.0, 541.38318, 541.90033, 532.86005, 536.82825, 536.82825, 1978500.0]]

    if c==3:
######## parameters for YahooStockDataSource used to test getMultipliers
        parameters["folderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["instrumentIds"]=['IBM', 'GOOG']
        parameters["startDateStr"]='2014/01/01'
        parameters["endDateStr"]='2014/01/30'
        parameters["event"]="history"
        parameters["liveUpdates"]=True
        parameters["startDate"]=datetime.strptime('2014/01/01',"%Y/%m/%d")
        parameters["endDate"]=datetime.strptime('2014/01/30',"%Y/%m/%d")
        parameters["instrumentId"]="GOOG"
        parameters["fileName"]="Folder1/data.txt"
        parameters["downloadId"]=".SN"

    if c==4:
######## parameters for YahooStockDataSource used to test getMultipliers
        parameters["folderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["instrumentIds"]=['IBM', 'GOOG']
        parameters["startDateStr"]='2014/05/01'
        parameters["endDateStr"]='2014/05/10'
        parameters["event"]="history"
        parameters["liveUpdates"]=True
        parameters["startDate"]=datetime.strptime('2014/05/01',"%Y/%m/%d")
        parameters["endDate"]=datetime.strptime('2014/05/10',"%Y/%m/%d")
        parameters["instrumentId"]="GOOG"
######## testing for getMultipliers
        parameters["fileName"]="Folder1/data.txt"
        parameters["divfileName"]="Folder1/div/GOOG_2014-05-01to2014-05-10.csv"
        parameters["splitfileName"]="Folder1/split/GOOG_2014-05-01to2014-05-10.csv"
        dataSet["divData"]="Date,Dividends\n2014-05-02,0.47\n2014-05-08,0.47\n"
        dataSet["splitData"]="Date,Stock Splits\n2014-05-05,7/1\n2014-05-07,7/1\n"
        dataSet["fileData"]=("Date,Open,High,Low,Close,Adj Close,Volume\n"
                             "2014-04-30,524.714844,525.112671,519.662598,523.779968,523.779968,1755900\n"
                             "2014-05-01,524.227539,530.015686,521.015198,528.444336,528.444336,1910700\n"
                             "2014-05-02,530.841125,531.079834,522.735718,525.043030,525.043030,1693100\n"
                             "2014-05-05,521.950012,526.007751,518.469177,524.923706,524.923706,1026900\n"
                             "2014-05-06,522.357788,523.929138,512.243408,512.322998,512.322998,1693600\n"
                             "2014-05-07,512.969421,513.854553,500.547729,507.171295,507.171295,3233200\n"
                             "2014-05-08,505.679504,514.401550,503.680481,508.205627,508.205627,2026800\n"
                             "2014-05-09,507.956970,517.056946,501.442810,515.893311,515.893311,2446100\n")
        parameters["downloadId"]=".SN"
        results["listTemp"]=[[0.0, 0.0, 0.47, 0.0, 0.0, 0.0, 0.47, 0.0],
                             [524.7148440000001, 524.227539, 530.841125, 521.950012, 522.357788, 512.969421, 505.679504, 507.95697],
                             [525.112671, 530.0156860000001, 531.079834, 526.007751, 523.929138, 513.854553, 514.40155, 517.056946],
                             [519.662598, 521.015198, 522.735718, 518.469177, 512.243408, 500.547729, 503.680481, 501.44280999999995],
                             [523.7799679999999, 528.444336, 525.0430299999999, 524.9237059999999, 512.3229980000001, 507.17129500000004, 508.20562699999994, 515.893311],
                             [523.7799679999999, 528.444336, 525.0430299999999, 524.9237059999999, 512.3229980000001, 507.17129500000004, 508.20562699999994, 515.893311],
                             [1755900, 1910700, 1693100, 1026900, 1693600, 3233200, 2026800, 2446100]]
        results["listMultiplier"]=[[0.9981808406396517, 0.9981808406396517, 0.9981808406396517, 0.9990751774970016, 0.9990751774970016, 0.9990751774970016, 0.9990751774970016, 1.0],
                                  [0.02040816326530612, 0.02040816326530612, 0.02040816326530612, 0.14285714285714285, 0.14285714285714285, 1.0, 1.0, 1.0]]


    if c==5:
######## parameters for YahooStockDataSource used to test getMultipliers
        parameters["folderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["instrumentIds"]=['IBM', 'GOOG']
        parameters["startDateStr"]='2014/05/01'
        parameters["endDateStr"]='2014/05/10'
        parameters["event"]="history"
        parameters["liveUpdates"]=True
        parameters["startDate"]=datetime.strptime('2014/05/01',"%Y/%m/%d")
        parameters["endDate"]=datetime.strptime('2014/05/10',"%Y/%m/%d")
        parameters["instrumentId"]="GOOG"
        parameters["fileName"]="Folder1/data.txt"
######## testing for getMultipliers
        parameters["divfileName"]="Folder1/div/GOOG_2014-05-01to2014-05-10.csv"
        parameters["splitfileName"]="Folder1/split/GOOG_2014-05-01to2014-05-10.csv"
        dataSet["divData"]="Date,Dividends\n2014-05-02,0.47\n2014-05-08,0.47\n"
        dataSet["splitData"]="Date,Stock Splits\n2014-05-05,7/1\n2014-05-07,7/1\n"
        dataSet["fileData"]=("Date,Open,High,Low,Close,Adj Close,Volume\n"
                             "2014-04-30,10,20,30,40,50,60\n"
                             "2014-05-01,11,21,31,0,51,61\n"
                             "2014-05-02,12,22,32,42,52,62\n"
                             "2014-05-05,13,23,33,43,53,63\n"
                             "2014-05-06,14,24,34,0,54,64\n"
                             "2014-05-07,15,25,35,45,55,65\n"
                             "2014-05-08,16,26,36,0,56,66\n"
                             "2014-05-09,17,27,37,47,57,67\n")
        parameters["downloadId"]=".SN"
        results["listTemp"]=[[0.0, 0.0, 0.47, 0.0, 0.0, 0.0, 0.47, 0.0],
                             [10, 11, 12, 13, 14, 15, 16, 17],
                             [20, 21, 22, 23, 24, 25, 26, 27],
                             [30, 31, 32, 33, 34, 35, 36, 37],
                             [40, 0, 42, 43, 0, 45, 0, 47],
                             [50, 51, 52, 53, 54, 55, 56, 57],
                             [60, 61, 62, 63, 64, 65, 66, 67]]
        results["listMultiplier"]=[[0.9888095238095238, 0.9888095238095238, 0.9888095238095238, 1.0, 1.0, 1.0, 1.0, 1.0],
                                   [0.02040816326530612, 0.02040816326530612, 0.02040816326530612, 0.14285714285714285, 0.14285714285714285, 1.0, 1.0, 1.0]]

    return {"dataSet":dataSet,"parameters":parameters,"results":results}
