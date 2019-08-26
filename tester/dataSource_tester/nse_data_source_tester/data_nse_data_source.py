import pandas as pd
from datetime import datetime, time, timedelta
from backtester.instrumentUpdates import *

def data_nse_data_source(c):
    dataSet={}
    parameters={}
    results={}

    if c==0:
######## testing for checkDate
        parameters["lineItem"]=""
        results["checkDate"]=False
######## testing for isFloat
        parameters["isFloat"]=""
        results["isFloat"]=False
######## testing for validateLineItem
        parameters["lineItems"]=["2018-01-31"]
        parameters["lineLength"]=2
        results["validateLineItem"]=0
######## testing for parseDataLine
        results["parseDataLine"]=None
######## testing for InstrumentFromFile
        parameters["fileName"]="Folder1/text.txt"
        parameters["instrumentId"]="AAE"
######## testing for processLine
        parameters["line"]="ABC"
        results["processLine"]=None
        parameters["instrumentIds"]=["AAE","AGG"]
######## testing for NSEStockDataSource
        parameters["folderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["date"]="2018-01-05"
        dataSet["fileData"]=("Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n"
                             "05-Jan-2018,1352.25,1351.00,1362.95,1348.25,1352.65,1356.55,1355.70,568451,770651233.05,17938,368125,64.76\n"
                             "08-Jan-2018,1356.55,1348.60,1371.00,1348.60,1370.00,1368.40,1363.11,801796,1092939507.05,28669,536934,66.97\n"
                             "09-Jan-2018,1368.40,1374.00,1375.90,1356.00,1361.35,1361.30,1364.12,708386,966326814.65,24175,489605,69.12\n")
        parameters["startDateStr"]="2018/01/05"
        parameters["endDateStr"]="2018/01/09"
        parameters["adjustPrice"]=False
        parameters["downloadId"]=".NS"
        parameters["liveUpdates"]=True
        parameters["pad"]=True
        parameters["stock"]="HINDUNILVR"
######## testing for getResponseFromUrl
        results["getResponseFromUrl"]="1"
######## testing for getInitialSymbolCountUrl
        results["getInitialSymbolCountUrl"]="https://nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol=HINDUNILVR"
######## testing for getDataUrl
        results["getDataUrl"]="https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=HINDUNILVR&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate=05-01-2018&toDate=09-01-2018&dataType=PRICEVOLUMEDELIVERABLE"
######## testing parseNseUrl
        parameters["start"]="05-01-2018"
        parameters["end"]="09-01-2018"
        results["rows"]=[['05-Jan-2018', '1352.25', '1351.00', '1362.95', '1348.25', '1352.65', '1356.55', '1355.70', '568451', '770651233.05', '17938', '368125', '64.76'],
                         ['08-Jan-2018', '1356.55', '1348.60', '1371.00', '1348.60', '1370.00', '1368.40', '1363.11', '801796', '1092939507.05', '28669', '536934', '66.97'],
                         ['09-Jan-2018', '1368.40', '1374.00', '1375.90', '1356.00', '1361.35', '1361.30', '1364.12', '708386', '966326814.65', '24175', '489605', '69.12']]
        results["headers"]=['Date', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'Average', 'Total Traded Quantity', 'Turnover', 'No. of Trades', 'Deliverable Qty', '% Dly Qt to Traded Qty']
        parameters["csvfileName"]="Folder1/abc.txt"
        results["check"]=['Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n',
                          '05-Jan-2018,1352.25,1351.00,1362.95,1348.25,1352.65,1356.55,1355.70,568451,770651233.05,17938,368125,64.76\n',
                          '08-Jan-2018,1356.55,1348.60,1371.00,1348.60,1370.00,1368.40,1363.11,801796,1092939507.05,28669,536934,66.97\n',
                          '09-Jan-2018,1368.40,1374.00,1375.90,1356.00,1361.35,1361.30,1364.12,708386,966326814.65,24175,489605,69.12\n']
######## testing getFileName and getFileName1
        results["getFileName"]="Folder1/QQ3Data/HINDUNILVR_2018-01-05to2018-01-05.csv"
######## testing getInstrumentUpdateFromRow
        parameters["rowdict"]={"Date":"01-Dec-2018", "vol": "231", "price": "451"}
######## testing getBookDataByFeature
        dataSet["DataFrames"]={"Prev Close":pd.DataFrame({"AAE":[1352.25,1356.55,1368.4],"AGG":[1352.25,1356.55,1368.4]}, index= [pd.Timestamp(' 2018-01-05 00:00:00 '),pd.Timestamp(' 2018-01-08 00:00:00 '),pd.Timestamp(' 2018-01-09 00:00:00 ')]),
                              "Turnover":pd.DataFrame({"AAE":[770651233.05,1092939507.05,966326814.65],"AGG":[770651233.05,1092939507.05,966326814.65]}, index= [pd.Timestamp(' 2018-01-05 00:00:00 '),pd.Timestamp(' 2018-01-08 00:00:00 '),pd.Timestamp(' 2018-01-09 00:00:00 ')]),
                              "Low":pd.DataFrame({"AAE":[1348.25,1348.6,1356.0],"AGG":[1348.25,1348.6,1356.0]}, index= [pd.Timestamp(' 2018-01-05 00:00:00 '),pd.Timestamp(' 2018-01-08 00:00:00 '),pd.Timestamp(' 2018-01-09 00:00:00 ')]),
                              "No. of Trades":pd.DataFrame({"AAE":[17938.0,28669.0,24175.0],"AGG":[17938.0,28669.0,24175.0]}, index= [pd.Timestamp(' 2018-01-05 00:00:00 '),pd.Timestamp(' 2018-01-08 00:00:00 '),pd.Timestamp(' 2018-01-09 00:00:00 ')]),
                              "Last":pd.DataFrame({"AAE":[1352.65,1370.0,1361.35],"AGG":[1352.65,1370.0,1361.35]}, index= [pd.Timestamp(' 2018-01-05 00:00:00 '),pd.Timestamp(' 2018-01-08 00:00:00 '),pd.Timestamp(' 2018-01-09 00:00:00 ')]),
                              "Average":pd.DataFrame({"AAE":[1355.7,1363.11,1364.12],"AGG":[1355.7,1363.11,1364.12]}, index= [pd.Timestamp(' 2018-01-05 00:00:00 '),pd.Timestamp(' 2018-01-08 00:00:00 '),pd.Timestamp(' 2018-01-09 00:00:00 ')]),
                              "Open":pd.DataFrame({"AAE":[1351.0,1348.6,1374.0],"AGG":[1351.0,1348.6,1374.0]}, index= [pd.Timestamp(' 2018-01-05 00:00:00 '),pd.Timestamp(' 2018-01-08 00:00:00 '),pd.Timestamp(' 2018-01-09 00:00:00 ')]),
                              "Total Traded Quantity":pd.DataFrame({"AAE":[568451.0,801796.0,708386.0],"AGG":[568451.0,801796.0,708386.0]}, index= [pd.Timestamp(' 2018-01-05 00:00:00 '),pd.Timestamp(' 2018-01-08 00:00:00 '),pd.Timestamp(' 2018-01-09 00:00:00 ')]),
                              "Close":pd.DataFrame({"AAE":[1356.55,1368.4,1361.3],"AGG":[1356.55,1368.4,1361.3]}, index= [pd.Timestamp(' 2018-01-05 00:00:00 '),pd.Timestamp(' 2018-01-08 00:00:00 '),pd.Timestamp(' 2018-01-09 00:00:00 ')]),
                              "High":pd.DataFrame({"AAE":[1362.95,1371.0,1375.9],"AGG":[1362.95,1371.0,1375.9]}, index= [pd.Timestamp(' 2018-01-05 00:00:00 '),pd.Timestamp(' 2018-01-08 00:00:00 '),pd.Timestamp(' 2018-01-09 00:00:00 ')]),
                              "Deliverable Qty":pd.DataFrame({"AAE":[368125.0,536934.0,489605.0],"AGG":[368125.0,536934.0,489605.0]}, index= [pd.Timestamp(' 2018-01-05 00:00:00 '),pd.Timestamp(' 2018-01-08 00:00:00 '),pd.Timestamp(' 2018-01-09 00:00:00 ')]),
                              "% Dly Qt to Traded Qty":pd.DataFrame({"AAE":[64.76,66.97,69.12],"AGG":[64.76,66.97,69.12]}, index= [pd.Timestamp(' 2018-01-05 00:00:00 '),pd.Timestamp(' 2018-01-08 00:00:00 '),pd.Timestamp(' 2018-01-09 00:00:00 ')])}
######## testing getClosingTime
        results["getClosingTime"]=datetime(2018, 1, 9)
######## testing adjustPriceForSplitAndDiv
        results["adjustPriceForSplitAndDiv"]=[['29-Dec-2017', 1354.5, 1359.0, 1374.9, 1350.0, 1362.25, 1367.85, 1366.33, 799006.0, 1091708127.0, 23341, 511548.0, 64.02],
                                              ['26-Dec-2017', 1356.5, 1350.4, 1353.9, 1340.0, 1348.0, 1348.1, 1347.23, 913529.0, 1230733171.2, 20283, 621059.0, 67.98],
                                              ['22-Dec-2017', 1348.45, 1341.3, 1359.5, 1341.3, 1350.4, 1356.5, 1354.47, 561400.0, 760400728.5, 35762, 349208.0, 62.2],
                                              ['21-Dec-2017', 1362.65, 1365.0, 1365.15, 1345.1, 1346.45, 1348.45, 1350.24, 557871.0, 753259232.0, 25809, 358001.0, 64.17],
                                              ['15-Dec-2017', 1321.6, 1328.3, 1335.0, 1310.6, 1323.3, 1324.55, 1322.7, 1420357.0, 1878709412.55, 59459, 1033307.0, 72.75],
                                              ['19-Oct-2017', 1263.95, 1265.0, 1270.0, 1253.7, 1255.0, 1257.7, 1260.69, 67835.0, 85518787.95, 2845, 18698.0, 27.56],
                                              ['07-Aug-2017', 1192.1, 1173.0, 1193.1, 1171.35, 1177.95, 1186.3, 1184.16, 868190.0, 1028072406.05, 40921, 631855.0, 72.78],
                                              ['26-May-2017', 1043.45, 1042.05, 1046.95, 1032.4, 1041.0, 1040.95, 1040.43, 716421.0, 745383722.55, 26030, 367491.0, 51.3],
                                              ['14-Mar-2017', 875.2, 881.2, 915.0, 879.05, 913.0, 913.75, 896.86, 2763421.0, 2478396096.0, 90182, 2050513.0, 74.2],
                                              ['10-Feb-2017', 850.75, 848.25, 858.4, 847.65, 850.05, 850.9, 852.62, 648644.0, 553044279.75, 28187, 364873.0, 56.25],
                                              ['02-Jan-2017', 826.35, 828.0, 828.0, 819.1, 825.1, 825.35, 824.19, 439748.0, 362434548.1, 11162, 262695.0, 59.74]]

    if c==1:
######## testing for checkDate
        parameters["lineItem"]="31-Dec-2018"
        results["checkDate"]=True
######## testing for isFloat
        parameters["isFloat"]=1
        results["isFloat"]=True
######## testing for validateLineItem
        parameters["lineItems"]=["Date","",20,30,10,21,22,20,20]
        parameters["lineLength"]=9
        results["validateLineItem"]=1
######## testing for parseDataLine
        results["parseDataLine"]={'last': 21.0, 'low': 10.0, 'average': 20.0, 'volume': 20.0, 'close': 22.0, 'high': 30.0, 'open': 20.0}
######## testing for InstrumentFromFile
        parameters["fileName"]="Folder1/text.txt"
        parameters["instrumentId"]="AGG"
######## testing for processLine
        parameters["line"]="31-Dec-2018, ,100,30,1,2,11,20,100"
######## testing for processLineIntoInstruments
        results["getStockInstrumentId"]="AGG"
        results["getTypeOfInstrument"]="stock"
        parameters["instrumentIds"]=["BBA","BST"]
######## testing for NSEStockDataSource
        parameters["folderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["date"]="2018-01-10"
        dataSet["fileData"]=("Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n"
                             "10-Jan-2018,2457.80,2459.95,2472.00,2420.00,2427.10,2425.80,2436.94,344328,839104989.10,20822,94640,27.49\n"
                             "11-Jan-2018,2425.80,2427.00,2451.00,2418.00,2424.80,2425.35,2432.89,185159,450471546.10,15411,58215,31.44\n"
                             "12-Jan-2018,2425.35,2433.00,2453.85,2413.65,2449.00,2447.65,2435.83,355780,866619682.15,21392,129447,36.38\n"
                             "15-Jan-2018,2447.65,2447.00,2461.25,2425.05,2435.00,2431.75,2443.25,156821,383152622.55,11089,45207,28.83\n")
        parameters["startDateStr"]="2018/01/10"
        parameters["endDateStr"]="2018/01/15"
        parameters["adjustPrice"]=False
        parameters["downloadId"]=".NS"
        parameters["liveUpdates"]=True
        parameters["pad"]=True
        parameters["stock"]="DRREDDY"
######## testing for getResponseFromUrl
        results["getResponseFromUrl"]="1"
######## testing for getInitialSymbolCountUrl
        results["getInitialSymbolCountUrl"]="https://nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol=DRREDDY"
######## testing for getDataUrl
        results["getDataUrl"]="https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=DRREDDY&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate=10-01-2018&toDate=15-01-2018&dataType=PRICEVOLUMEDELIVERABLE"
######## testing parseNseUrl
        parameters["start"]="10-01-2018"
        parameters["end"]="15-01-2018"
        results["rows"]=[['10-Jan-2018', '2457.80', '2459.95', '2472.00', '2420.00', '2427.10', '2425.80', '2436.94', '344328', '839104989.10', '20822', '94640', '27.49'],
                         ['11-Jan-2018', '2425.80', '2427.00', '2451.00', '2418.00', '2424.80', '2425.35', '2432.89', '185159', '450471546.10', '15411', '58215', '31.44'],
                         ['12-Jan-2018', '2425.35', '2433.00', '2453.85', '2413.65', '2449.00', '2447.65', '2435.83', '355780', '866619682.15', '21392', '129447', '36.38'],
                         ['15-Jan-2018', '2447.65', '2447.00', '2461.25', '2425.05', '2435.00', '2431.75', '2443.25', '156821', '383152622.55', '11089', '45207', '28.83']]
        results["headers"]=['Date', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'Average', 'Total Traded Quantity', 'Turnover', 'No. of Trades', 'Deliverable Qty', '% Dly Qt to Traded Qty']
        parameters["csvfileName"]="Folder1/abc.txt"
        results["check"]=['Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n',
                          '10-Jan-2018,2457.80,2459.95,2472.00,2420.00,2427.10,2425.80,2436.94,344328,839104989.10,20822,94640,27.49\n',
                          '11-Jan-2018,2425.80,2427.00,2451.00,2418.00,2424.80,2425.35,2432.89,185159,450471546.10,15411,58215,31.44\n',
                          '12-Jan-2018,2425.35,2433.00,2453.85,2413.65,2449.00,2447.65,2435.83,355780,866619682.15,21392,129447,36.38\n',
                          '15-Jan-2018,2447.65,2447.00,2461.25,2425.05,2435.00,2431.75,2443.25,156821,383152622.55,11089,45207,28.83\n']
######## testing getFileName and getFileName1
        results["getFileName"]="Folder1/QQ3Data/DRREDDY_2018-01-10to2018-01-10.csv"
######## testing getInstrumentUpdateFromRow
        parameters["rowdict"]={"Date":"02-Jan-2015", "vol": "456", "price": "444"}
######## testing getBookDataByFeature
        dataSet["DataFrames"]={"Average":pd.DataFrame({"BBA":[2436.94,2432.89,2435.83,2443.25],"BST":[2436.94,2432.89,2435.83,2443.25]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "Open":pd.DataFrame({"BBA":[2459.95,2427.0,2433.0,2447.0],"BST":[2459.95,2427.0,2433.0,2447.0]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "Turnover":pd.DataFrame({"BBA":[839104989.1,450471546.1,866619682.15,383152622.55],"BST":[839104989.1,450471546.1,866619682.15,383152622.55]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "Prev Close":pd.DataFrame({"BBA":[2457.8,2425.8,2425.35,2447.65],"BST":[2457.8,2425.8,2425.35,2447.65]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "Last":pd.DataFrame({"BBA":[2427.1,2424.8,2449.0,2435.0],"BST":[2427.1,2424.8,2449.0,2435.0]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "Low":pd.DataFrame({"BBA":[2420.0,2418.0,2413.65,2425.05],"BST":[2420.0,2418.0,2413.65,2425.05]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "% Dly Qt to Traded Qty":pd.DataFrame({"BBA":[27.49,31.44,36.38,28.83],"BST":[27.49,31.44,36.38,28.83]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "No. of Trades":pd.DataFrame({"BBA":[20822.0,15411.0,21392.0,11089.0],"BST":[20822.0,15411.0,21392.0,11089.0]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "Deliverable Qty":pd.DataFrame({"BBA":[94640.0,58215.0,129447.0,45207.0],"BST":[94640.0,58215.0,129447.0,45207.0]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "High":pd.DataFrame({"BBA":[2472.0,2451.0,2453.85,2461.25],"BST":[2472.0,2451.0,2453.85,2461.25]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "Close":pd.DataFrame({"BBA":[2425.8,2425.35,2447.65,2431.75],"BST":[2425.8,2425.35,2447.65,2431.75]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "Total Traded Quantity":pd.DataFrame({"BBA":[344328.0,185159.0,355780.0,156821.0],"BST":[344328.0,185159.0,355780.0,156821.0]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')])}
######## testing getClosingTime
        results["getClosingTime"]=datetime(2018, 1, 15)
######## testing adjustPriceForSplitAndDiv
        results["adjustPriceForSplitAndDiv"]=[['29-Dec-2017', 2430.0, 2429.95, 2445.95, 2403.15, 2414.25, 2414.2, 2424.53, 331967.0, 804864049.05, 20651, 104575.0, 31.5],
                                              ['26-Dec-2017', 2332.7, 2334.95, 2367.0, 2329.0, 2361.0, 2360.3, 2353.6, 410936.0, 967177855.2, 22405, 125836.0, 30.62],
                                              ['22-Dec-2017', 2351.75, 2360.0, 2363.0, 2330.0, 2335.0, 2332.7, 2339.02, 249602.0, 583824593.85, 11590, 74787.0, 29.96],
                                              ['21-Dec-2017', 2356.0, 2365.0, 2374.7, 2341.0, 2350.9, 2351.75, 2356.25, 249941.0, 588923932.25, 19666, 56009.0, 22.41],
                                              ['15-Dec-2017', 2310.65, 2325.0, 2380.0, 2316.45, 2370.0, 2371.5, 2350.22, 743680.0, 1747810478.65, 43902, 355975.0, 47.87],
                                              ['19-Oct-2017', 2385.4, 2385.0, 2387.0, 2362.05, 2376.9, 2373.05, 2374.37, 47303.0, 112314876.05, 2637, 13195.0, 27.89],
                                              ['07-Aug-2017', 2239.55, 2240.0, 2257.0, 2200.0, 2202.0, 2206.95, 2229.8, 736078.0, 1641306908.35, 39569, 355427.0, 48.29],
                                              ['26-May-2017', 2427.7, 2500.0, 2509.95, 2403.8, 2419.95, 2414.4, 2435.38, 721031.0, 1755982583.05, 38740, 328084.0, 45.5],
                                              ['14-Mar-2017', 2715.85, 2746.7, 2754.85, 2716.7, 2741.0, 2741.0, 2735.92, 497842.0, 1362055813.85, 49861, 247207.0, 49.66],
                                              ['10-Feb-2017', 3023.1, 3024.9, 3034.35, 2970.0, 2975.95, 2976.05, 2991.2, 315001.0, 942232074.15, 32188, 190665.0, 60.53],
                                              ['02-Jan-2017', 3060.4, 3066.0, 3117.0, 3066.0, 3078.5, 3083.4, 3094.57, 95526.0, 295611635.45, 8195, 25984.0, 27.2]]

    if c==2:
######## testing for checkDate
        parameters["lineItem"]="31-Dec-2018"
        results["checkDate"]=True
######## testing for isFloat
        parameters["isFloat"]=1
        results["isFloat"]=True
######## testing for validateLineItem
        parameters["lineItems"]=["Date","",20,30,10,21,22,20,20]
        parameters["lineLength"]=9
        results["validateLineItem"]=1
######## testing for parseDataLine
        results["parseDataLine"]={'last': 21.0, 'low': 10.0, 'average': 20.0, 'volume': 20.0, 'close': 22.0, 'high': 30.0, 'open': 20.0}
######## testing for InstrumentFromFile
        parameters["fileName"]="Folder1/text.txt"
        parameters["instrumentId"]="AGG"
######## testing for processLine
        parameters["line"]="31-Dec-2018, ,100,30,1,2,11,20,100"
######## testing for processLineIntoInstruments
        results["getStockInstrumentId"]="AGG"
        results["getTypeOfInstrument"]="stock"
        parameters["instrumentIds"]=["BBA","BST"]
######## testing for NSEStockDataSource
        parameters["folderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["date"]="2018-01-10"
        dataSet["fileData"]=("Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n"
                             "10-Jan-2018,2457.80,2459.95,2472.00,2420.00,2427.10,2425.80,2436.94,344328,839104989.10,20822,94640,27.49\n"
                             "11-Jan-2018,2425.80,2427.00,2451.00,2418.00,2424.80,2425.35,2432.89,185159,450471546.10,15411,58215,31.44\n"
                             "12-Jan-2018,2425.35,2433.00,2453.85,2413.65,2449.00,2447.65,2435.83,355780,866619682.15,21392,129447,36.38\n"
                             "15-Jan-2018,2447.65,2447.00,2461.25,2425.05,2435.00,2431.75,2443.25,156821,383152622.55,11089,45207,28.83\n")
        parameters["startDateStr"]="2018/01/10"
        parameters["endDateStr"]="2018/01/15"
        parameters["adjustPrice"]=False
        parameters["downloadId"]=".NS"
        parameters["liveUpdates"]=False
        parameters["pad"]=True
        parameters["stock"]="DRREDDY"
######## testing for getResponseFromUrl
        results["getResponseFromUrl"]="1"
######## testing for getInitialSymbolCountUrl
        results["getInitialSymbolCountUrl"]="https://nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol=DRREDDY"
######## testing for getDataUrl
        results["getDataUrl"]="https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=DRREDDY&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate=10-01-2018&toDate=15-01-2018&dataType=PRICEVOLUMEDELIVERABLE"
######## testing parseNseUrl
        parameters["start"]="10-01-2018"
        parameters["end"]="15-01-2018"
        results["rows"]=[['10-Jan-2018', '2457.80', '2459.95', '2472.00', '2420.00', '2427.10', '2425.80', '2436.94', '344328', '839104989.10', '20822', '94640', '27.49'],
                         ['11-Jan-2018', '2425.80', '2427.00', '2451.00', '2418.00', '2424.80', '2425.35', '2432.89', '185159', '450471546.10', '15411', '58215', '31.44'],
                         ['12-Jan-2018', '2425.35', '2433.00', '2453.85', '2413.65', '2449.00', '2447.65', '2435.83', '355780', '866619682.15', '21392', '129447', '36.38'],
                         ['15-Jan-2018', '2447.65', '2447.00', '2461.25', '2425.05', '2435.00', '2431.75', '2443.25', '156821', '383152622.55', '11089', '45207', '28.83']]
        results["headers"]=['Date', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'Average', 'Total Traded Quantity', 'Turnover', 'No. of Trades', 'Deliverable Qty', '% Dly Qt to Traded Qty']
        parameters["csvfileName"]="Folder1/abc.txt"
        results["check"]=['Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n',
                          '10-Jan-2018,2457.80,2459.95,2472.00,2420.00,2427.10,2425.80,2436.94,344328,839104989.10,20822,94640,27.49\n',
                          '11-Jan-2018,2425.80,2427.00,2451.00,2418.00,2424.80,2425.35,2432.89,185159,450471546.10,15411,58215,31.44\n',
                          '12-Jan-2018,2425.35,2433.00,2453.85,2413.65,2449.00,2447.65,2435.83,355780,866619682.15,21392,129447,36.38\n',
                          '15-Jan-2018,2447.65,2447.00,2461.25,2425.05,2435.00,2431.75,2443.25,156821,383152622.55,11089,45207,28.83\n']
######## testing getFileName and getFileName1
        results["getFileName"]="Folder1/QQ3Data/DRREDDY_2018-01-10to2018-01-10.csv"
######## testing getInstrumentUpdateFromRow
        parameters["rowdict"]={"Date":"02-Jan-2015", "vol": "456", "price": "444"}
######## testing getBookDataByFeature
        dataSet["DataFrames"]=pd.DataFrame()
######## testing getClosingTime
        results["getClosingTime"]=datetime(2018, 1, 15)
######## testing adjustPriceForSplitAndDiv
        parameters["divfileName"]='Folder1/div/GOOG_2018-01-10to2018-01-10.csv'
        parameters["splitfileName"]='Folder1/split/GOOG_2018-01-10to2018-01-10.csv'
        dataSet["divData"]="Date,Dividends\n2014-05-02,0.47\n2014-05-08,0.47\n"
        dataSet["splitData"]="Date,Stock Splits\n2014-05-05,7/1\n2014-05-07,7/1\n"
        dataSet["fileData"]=("Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n"
                             "2014-04-30,1352.25,1351.00,1362.95,1348.25,1352.65,1356.55,1355.70,568451,770651233.05,17938,368125,64.76\n"
                             "2014-05-01,1356.55,1348.60,1371.00,1348.60,1370.00,1368.40,1363.11,801796,1092939507.05,28669,536934,66.97\n"
                             "2014-05-02,1368.40,1374.00,1375.90,1356.00,1361.35,1361.30,1364.12,708386,966326814.65,24175,489605,69.12\n"
                             "2014-05-05,1352.25,1351.00,1362.95,1348.25,1352.65,1356.55,1355.70,568451,770651233.05,17938,368125,64.76\n"
                             "2014-05-06,1356.55,1348.60,1371.00,1348.60,1370.00,1368.40,1363.11,801796,1092939507.05,28669,536934,66.97\n"
                             "2014-05-07,1368.40,1374.00,1375.90,1356.00,1361.35,1361.30,1364.12,708386,966326814.65,24175,489605,69.12\n"
                             "2014-05-08,1352.25,1351.00,1362.95,1348.25,1352.65,1356.55,1355.70,568451,770651233.05,17938,368125,64.76\n"
                             "2014-05-09,1356.55,1348.60,1371.00,1348.60,1370.00,1368.40,1363.11,801796,1092939507.05,28669,536934,66.97\n")
        results["adjustPriceForSplitAndDiv"]=[['2014-04-30', '2014-05-01', '2014-05-02', '2014-05-05', '2014-05-06', '2014-05-07', '2014-05-08', '2014-05-09'],
                                              [1352.25, 1356.55, 1368.4, 1352.25, 1356.55, 1368.4, 1352.25, 1356.55],
                                              [27.55236, 27.50341, 28.02142, 192.93313, 192.59039, 1373.52395, 1350.53192, 1348.6],
                                              [27.79607, 27.96024, 28.06017, 194.63968, 195.78928, 1375.4233, 1362.47778, 1371.0],
                                              [27.49628, 27.50341, 27.65433, 192.54041, 192.59039, 1355.53019, 1347.78288, 1348.6],
                                              [27.58601, 27.93985, 27.76344, 193.16876, 195.64648, 1360.87834, 1352.18135, 1370.0],
                                              [27.66555, 27.90722, 27.76242, 193.72571, 195.41798, 1360.82835, 1356.08, 1368.4],
                                              [27.64821, 27.79933, 27.81993, 193.60433, 194.66253, 1363.64738, 1355.23029, 1363.11],
                                              [27854099.0, 39288004.0, 34710914.0, 3979157.0, 5612572.0, 708386.0, 568451.0, 801796.0],
                                              [770118246.24189, 1092183623.82509, 965658497.48856, 770384227.72065, 1092560839.42381, 965992014.16134, 770384227.72065, 1092939507.05],
                                              [17938, 28669, 24175, 17938, 28669, 24175, 17938, 28669],
                                              [18038125.0, 26309766.0, 23990645.0, 2576875.0, 3758538.0, 489605.0, 368125.0, 536934.0],
                                              [64.76, 66.97, 69.12, 64.76, 66.97, 69.12, 64.76, 66.97]]


    if c==3:
######## testing for checkDate
        parameters["lineItem"]="31-Dec-2018"
        results["checkDate"]=True
######## testing for isFloat
        parameters["isFloat"]=1
        results["isFloat"]=True
######## testing for validateLineItem
        parameters["lineItems"]=["Date","",20,30,10,21,22,20,20]
        parameters["lineLength"]=9
        results["validateLineItem"]=1
######## testing for parseDataLine
        results["parseDataLine"]={'last': 21.0, 'low': 10.0, 'average': 20.0, 'volume': 20.0, 'close': 22.0, 'high': 30.0, 'open': 20.0}
######## testing for InstrumentFromFile
        parameters["fileName"]="Folder1/text.txt"
        parameters["instrumentId"]="AGG"
######## testing for processLine
        parameters["line"]="31-Dec-2018, ,100,30,1,2,11,20,100"
######## testing for processLineIntoInstruments
        results["getStockInstrumentId"]="AGG"
        results["getTypeOfInstrument"]="stock"
        parameters["instrumentIds"]=["BBA","BST"]
######## testing for NSEStockDataSource
        parameters["folderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["date"]="2018-01-10"
        dataSet["fileData"]=("Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n"
                             "10-Jan-2018,2457.80,2459.95,2472.00,2420.00,2427.10,2425.80,2436.94,344328,839104989.10,20822,94640,27.49\n"
                             "11-Jan-2018,2425.80,2427.00,2451.00,2418.00,2424.80,2425.35,2432.89,185159,450471546.10,15411,58215,31.44\n"
                             "12-Jan-2018,2425.35,2433.00,2453.85,2413.65,2449.00,2447.65,2435.83,355780,866619682.15,21392,129447,36.38\n"
                             "15-Jan-2018,2447.65,2447.00,2461.25,2425.05,2435.00,2431.75,2443.25,156821,383152622.55,11089,45207,28.83\n")
        parameters["startDateStr"]="2018/01/10"
        parameters["endDateStr"]="2018/01/15"
        parameters["adjustPrice"]=False
        parameters["downloadId"]=".NS"
        parameters["liveUpdates"]=False
        parameters["pad"]=False
        parameters["stock"]="DRREDDY"
######## testing for getResponseFromUrl
        results["getResponseFromUrl"]="1"
######## testing for getInitialSymbolCountUrl
        results["getInitialSymbolCountUrl"]="https://nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol=DRREDDY"
######## testing for getDataUrl
        results["getDataUrl"]="https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=DRREDDY&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate=10-01-2018&toDate=15-01-2018&dataType=PRICEVOLUMEDELIVERABLE"
######## testing parseNseUrl
        parameters["start"]="10-01-2018"
        parameters["end"]="15-01-2018"
        results["rows"]=[['10-Jan-2018', '2457.80', '2459.95', '2472.00', '2420.00', '2427.10', '2425.80', '2436.94', '344328', '839104989.10', '20822', '94640', '27.49'],
                         ['11-Jan-2018', '2425.80', '2427.00', '2451.00', '2418.00', '2424.80', '2425.35', '2432.89', '185159', '450471546.10', '15411', '58215', '31.44'],
                         ['12-Jan-2018', '2425.35', '2433.00', '2453.85', '2413.65', '2449.00', '2447.65', '2435.83', '355780', '866619682.15', '21392', '129447', '36.38'],
                         ['15-Jan-2018', '2447.65', '2447.00', '2461.25', '2425.05', '2435.00', '2431.75', '2443.25', '156821', '383152622.55', '11089', '45207', '28.83']]
        results["headers"]=['Date', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'Average', 'Total Traded Quantity', 'Turnover', 'No. of Trades', 'Deliverable Qty', '% Dly Qt to Traded Qty']
        parameters["csvfileName"]="Folder1/abc.txt"
        results["check"]=['Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n',
                          '10-Jan-2018,2457.80,2459.95,2472.00,2420.00,2427.10,2425.80,2436.94,344328,839104989.10,20822,94640,27.49\n',
                          '11-Jan-2018,2425.80,2427.00,2451.00,2418.00,2424.80,2425.35,2432.89,185159,450471546.10,15411,58215,31.44\n',
                          '12-Jan-2018,2425.35,2433.00,2453.85,2413.65,2449.00,2447.65,2435.83,355780,866619682.15,21392,129447,36.38\n',
                          '15-Jan-2018,2447.65,2447.00,2461.25,2425.05,2435.00,2431.75,2443.25,156821,383152622.55,11089,45207,28.83\n']
######## testing getFileName and getFileName1
        results["getFileName"]="Folder1/QQ3Data/DRREDDY_2018-01-10to2018-01-10.csv"
######## testing getInstrumentUpdateFromRow
        parameters["rowdict"]={"Date":"02-Jan-2015", "vol": "456", "price": "444"}
######## testing getBookDataByFeature
        dataSet["DataFrames"]=pd.DataFrame()
######## testing getClosingTime
        results["getClosingTime"]=datetime(2018, 1, 15)
######## testing adjustPriceForSplitAndDiv
        parameters["divfileName"]='Folder1/div/GOOG_2018-01-10to2018-01-10.csv'
        parameters["splitfileName"]='Folder1/split/GOOG_2018-01-10to2018-01-10.csv'
        dataSet["divData"]="Date,Dividends\n2014-05-02,0.47\n2014-05-08,0.47\n"
        dataSet["splitData"]="Date,Stock Splits\n2014-05-05,7/1\n2014-05-07,7/1\n"
        dataSet["fileData"]=("Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n"
                             "2014-04-30,10,20,30,40,50,60,70,80,90,100,110,120\n"
                             "2014-05-01,11,21,31,0,51,61,71,81,91,101,111,121\n"
                             "2014-05-02,12,22,32,42,52,62,72,82,92,102,112,122\n"
                             "2014-05-05,13,23,33,43,53,63,73,83,93,103,113,123\n"
                             "2014-05-06,14,24,34,0,54,64,74,84,94,104,114,124\n"
                             "2014-05-07,15,25,35,45,55,65,75,85,95,105,115,125\n"
                             "2014-05-08,16,26,36,0,56,66,76,86,96,106,116,126\n"
                             "2014-05-09,17,27,37,47,57,67,77,87,97,107,117,127\n")
        results["adjustPriceForSplitAndDiv"]=[['2014-04-30', '2014-05-01', '2014-05-02', '2014-05-05', '2014-05-06', '2014-05-07', '2014-05-08', '2014-05-09'],
                                              [10, 11, 12, 13, 14, 15, 16, 17], [0.40218, 0.42229, 0.4424, 3.26232, 3.40416, 24.82197, 25.81485, 27.0],
                                              [0.60328, 0.62339, 0.6435, 4.68071, 4.82255, 34.75076, 35.74364, 37.0],
                                              [0.80437, 0.0, 0.84459, 6.09911, 0.0, 44.67955, 0.0, 47.0],
                                              [1.00546, 1.02557, 1.04568, 7.51751, 7.65935, 54.60833, 55.60121, 57.0],
                                              [1.20655, 1.22666, 1.24677, 8.93591, 9.07775, 64.53712, 65.53, 67.0],
                                              [1.40765, 1.42776, 1.44786, 10.35431, 10.49615, 74.46591, 75.45879, 77.0],
                                              [3920.0, 3969.0, 4018.0, 581.0, 588.0, 85.0, 86.0, 87.0],
                                              [88.68169, 89.66704, 90.6524, 92.33773, 93.33061, 94.32348, 95.31636, 97.0],
                                              [100, 101, 102, 103, 104, 105, 106, 107],
                                              [5390.0, 5439.0, 5488.0, 791.0, 798.0, 115.0, 116.0, 117.0],
                                              [120, 121, 122, 123, 124, 125, 126, 127]]




    if c==4:
######## testing for checkDate
        parameters["lineItem"]="31-Dec-2018"
        results["checkDate"]=True
######## testing for isFloat
        parameters["isFloat"]=1
        results["isFloat"]=True
######## testing for validateLineItem
        parameters["lineItems"]=["Date","",20,30,10,21,22,20,20]
        parameters["lineLength"]=9
        results["validateLineItem"]=1
######## testing for parseDataLine
        results["parseDataLine"]={'last': 21.0, 'low': 10.0, 'average': 20.0, 'volume': 20.0, 'close': 22.0, 'high': 30.0, 'open': 20.0}
######## testing for InstrumentFromFile
        parameters["fileName"]="Folder1/text.txt"
        parameters["instrumentId"]="AGG"
######## testing for processLine
        parameters["line"]="31-Dec-2018, ,100,30,1,2,11,20,100"
######## testing for processLineIntoInstruments
        results["getStockInstrumentId"]="AGG"
        results["getTypeOfInstrument"]="stock"
        parameters["instrumentIds"]=["BBA","BST"]
######## testing for NSEStockDataSource
        parameters["folderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["date"]="2018-01-10"
        dataSet["fileData"]=("Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n"
                             "10-Jan-2018,2457.80,2459.95,2472.00,2420.00,2427.10,2425.80,2436.94,344328,839104989.10,20822,94640,27.49\n"
                             "11-Jan-2018,2425.80,2427.00,2451.00,2418.00,2424.80,2425.35,2432.89,185159,450471546.10,15411,58215,31.44\n"
                             "12-Jan-2018,2425.35,2433.00,2453.85,2413.65,2449.00,2447.65,2435.83,355780,866619682.15,21392,129447,36.38\n"
                             "15-Jan-2018,2447.65,2447.00,2461.25,2425.05,2435.00,2431.75,2443.25,156821,383152622.55,11089,45207,28.83\n")
        parameters["startDateStr"]="2018/01/10"
        parameters["endDateStr"]="2018/01/15"
        parameters["adjustPrice"]=True
        parameters["downloadId"]=".NS"
        parameters["liveUpdates"]=True
        parameters["pad"]=True
        parameters["stock"]="DRREDDY"
######## testing for getResponseFromUrl
        results["getResponseFromUrl"]="1"
######## testing for getInitialSymbolCountUrl
        results["getInitialSymbolCountUrl"]="https://nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol=DRREDDY"
######## testing for getDataUrl
        results["getDataUrl"]="https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=DRREDDY&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate=10-01-2018&toDate=15-01-2018&dataType=PRICEVOLUMEDELIVERABLE"
######## testing parseNseUrl
        parameters["start"]="10-01-2018"
        parameters["end"]="15-01-2018"
        results["rows"]=[['10-Jan-2018', '2457.80', '2459.95', '2472.00', '2420.00', '2427.10', '2425.80', '2436.94', '344328', '839104989.10', '20822', '94640', '27.49'],
                         ['11-Jan-2018', '2425.80', '2427.00', '2451.00', '2418.00', '2424.80', '2425.35', '2432.89', '185159', '450471546.10', '15411', '58215', '31.44'],
                         ['12-Jan-2018', '2425.35', '2433.00', '2453.85', '2413.65', '2449.00', '2447.65', '2435.83', '355780', '866619682.15', '21392', '129447', '36.38'],
                         ['15-Jan-2018', '2447.65', '2447.00', '2461.25', '2425.05', '2435.00', '2431.75', '2443.25', '156821', '383152622.55', '11089', '45207', '28.83']]
        results["headers"]=['Date', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'Average', 'Total Traded Quantity', 'Turnover', 'No. of Trades', 'Deliverable Qty', '% Dly Qt to Traded Qty']
        parameters["csvfileName"]="Folder1/abc.txt"
        results["check"]=['Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n',
                          '10-Jan-2018,2457.80,2459.95,2472.00,2420.00,2427.10,2425.80,2436.94,344328,839104989.10,20822,94640,27.49\n',
                          '11-Jan-2018,2425.80,2427.00,2451.00,2418.00,2424.80,2425.35,2432.89,185159,450471546.10,15411,58215,31.44\n',
                          '12-Jan-2018,2425.35,2433.00,2453.85,2413.65,2449.00,2447.65,2435.83,355780,866619682.15,21392,129447,36.38\n',
                          '15-Jan-2018,2447.65,2447.00,2461.25,2425.05,2435.00,2431.75,2443.25,156821,383152622.55,11089,45207,28.83\n']
######## testing getFileName and getFileName1
        results["getFileName"]="Folder1/QQ3Data/DRREDDY_2018-01-10to2018-01-10.csv"
######## testing getInstrumentUpdateFromRow
        parameters["rowdict"]={"Date":"02-Jan-2015", "vol": "456", "price": "444"}
######## testing getBookDataByFeature
        dataSet["DataFrames"]={"Average":pd.DataFrame({"BBA":[2436.94,2432.89,2435.83,2443.25],"BST":[2436.94,2432.89,2435.83,2443.25]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "Open":pd.DataFrame({"BBA":[2459.95,2427.0,2433.0,2447.0],"BST":[2459.95,2427.0,2433.0,2447.0]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "Turnover":pd.DataFrame({"BBA":[839104989.1,450471546.1,866619682.15,383152622.55],"BST":[839104989.1,450471546.1,866619682.15,383152622.55]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "Prev Close":pd.DataFrame({"BBA":[2457.8,2425.8,2425.35,2447.65],"BST":[2457.8,2425.8,2425.35,2447.65]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "Last":pd.DataFrame({"BBA":[2427.1,2424.8,2449.0,2435.0],"BST":[2427.1,2424.8,2449.0,2435.0]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "Low":pd.DataFrame({"BBA":[2420.0,2418.0,2413.65,2425.05],"BST":[2420.0,2418.0,2413.65,2425.05]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "% Dly Qt to Traded Qty":pd.DataFrame({"BBA":[27.49,31.44,36.38,28.83],"BST":[27.49,31.44,36.38,28.83]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "No. of Trades":pd.DataFrame({"BBA":[20822.0,15411.0,21392.0,11089.0],"BST":[20822.0,15411.0,21392.0,11089.0]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "Deliverable Qty":pd.DataFrame({"BBA":[94640.0,58215.0,129447.0,45207.0],"BST":[94640.0,58215.0,129447.0,45207.0]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "High":pd.DataFrame({"BBA":[2472.0,2451.0,2453.85,2461.25],"BST":[2472.0,2451.0,2453.85,2461.25]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "Close":pd.DataFrame({"BBA":[2425.8,2425.35,2447.65,2431.75],"BST":[2425.8,2425.35,2447.65,2431.75]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
                              "Total Traded Quantity":pd.DataFrame({"BBA":[344328.0,185159.0,355780.0,156821.0],"BST":[344328.0,185159.0,355780.0,156821.0]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')])}
######## testing getClosingTime
        results["getClosingTime"]=datetime(2018, 1, 15)

    if c==5:
######## testing for checkDate
        parameters["lineItem"]="2018-05-21"
        results["checkDate"]=True
######## testing for isFloat
        parameters["isFloat"]=1.00
        results["isFloat"]=True
######## testing for validateLineItem
        parameters["lineItems"]=["2018-05-21","",25.80,30.52,1.02,2,1.1,20.24,1.1]
        parameters["lineLength"]=9
        results["validateLineItem"]=2
######## testing for parseDataLine
        results["parseDataLine"]={'last': 2.0, 'low': 1.02, 'average': 20.24, 'volume': 1.1, 'close': 1.1, 'high': 30.52, 'open': 25.8}
######## testing for InstrumentFromFile
        parameters["fileName"]="Folder1/text.txt"
        parameters["instrumentId"]="BBA"
######## testing for processLine
        parameters["line"]="2018-05-21, ,25.80,30.52,1.02,2,1.1,20.24"
        results["processLine"]=None
        ######## testing for processLineIntoInstruments
        parameters["instrumentIds"]=["QZO","QZU"]
######## testing for NSEStockDataSource
        parameters["folderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["date"]="2018-01-24"
        dataSet["fileData"]=("Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n"
                             "24-Jan-2018,995.35,994.00,1040.70,992.00,1020.00,1018.45,1021.46,4634888,4734354679.90,158184,2689213,58.02\n"
                             "25-Jan-2018,1018.45,1018.80,1020.00,990.05,1020.00,1009.55,1005.45,2653727,2668184643.80,69123,1776445,66.94\n"
                             "29-Jan-2018,1009.55,1010.00,1021.00,1005.05,1005.75,1012.05,1015.15,2006648,2037047218.20,77146,1427424,71.13\n"
                             "30-Jan-2018,1012.05,1017.50,1017.50,998.00,1000.00,1000.40,1002.93,1355676,1359653985.50,40486,864658,63.78\n"
                             "31-Jan-2018,1000.40,999.95,1017.90,981.70,984.05,986.55,997.58,1610572,1606671902.35,44282,736833,45.75\n")
        parameters["startDateStr"]="2018/01/24"
        parameters["endDateStr"]="2018/01/31"
        parameters["adjustPrice"]=False
        parameters["downloadId"]=".NS"
        parameters["liveUpdates"]=True
        parameters["pad"]=True
        parameters["stock"]=""
######## testing for getResponseFromUrl
        results["getResponseFromUrl"]="2"
######## testing for getInitialSymbolCountUrl
        results["getInitialSymbolCountUrl"]="https://nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol="
######## testing for getDataUrl
        results["getDataUrl"]="https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=&segmentLink=3&symbolCount=2&series=EQ&dateRange=+&fromDate=24-01-2018&toDate=31-01-2018&dataType=PRICEVOLUMEDELIVERABLE"
######## testing parseNseUrl
        parameters["start"]="24-01-2018"
        parameters["end"]="31-01-2018"
        parameters["csvfileName"]="Folder1/abc.txt"
######## testing getFileName and getFileName1
        results["getFileName"]="Folder1/QQ3Data/_2018-01-24to2018-01-24.csv"
######## testing getInstrumentUpdateFromRow
        parameters["rowdict"]={"Date":"08-Feb-2019", "vol": "222", "price": "111"}
######## testing getBookDataByFeature
        dataSet["DataFrames"]={"Total Traded Quantity":pd.DataFrame({"QZO":[4634888.0,2653727.0,2006648.0,1355676.0,1610572.0],"QZU":[4634888.0,2653727.0,2006648.0,1355676.0,1610572.0]}, index= [pd.Timestamp(' 2018-01-24 00:00:00 '),pd.Timestamp(' 2018-01-25 00:00:00 '),pd.Timestamp(' 2018-01-29 00:00:00 '),pd.Timestamp(' 2018-01-30 00:00:00 '),pd.Timestamp(' 2018-01-31 00:00:00 ')]),
                             "Average":pd.DataFrame({"QZO":[1021.46,1005.45,1015.15,1002.93,997.58],"QZU":[1021.46,1005.45,1015.15,1002.93,997.58]}, index= [pd.Timestamp(' 2018-01-24 00:00:00 '),pd.Timestamp(' 2018-01-25 00:00:00 '),pd.Timestamp(' 2018-01-29 00:00:00 '),pd.Timestamp(' 2018-01-30 00:00:00 '),pd.Timestamp(' 2018-01-31 00:00:00 ')]),
                             "Last":pd.DataFrame({"QZO":[1020.0,1020.0,1005.75,1000.0,984.05],"QZU":[1020.0,1020.0,1005.75,1000.0,984.05]}, index= [pd.Timestamp(' 2018-01-24 00:00:00 '),pd.Timestamp(' 2018-01-25 00:00:00 '),pd.Timestamp(' 2018-01-29 00:00:00 '),pd.Timestamp(' 2018-01-30 00:00:00 '),pd.Timestamp(' 2018-01-31 00:00:00 ')]),
                             "Low":pd.DataFrame({"QZO":[992.0,990.05,1005.05,998.0,981.7],"QZU":[992.0,990.05,1005.05,998.0,981.7]}, index= [pd.Timestamp(' 2018-01-24 00:00:00 '),pd.Timestamp(' 2018-01-25 00:00:00 '),pd.Timestamp(' 2018-01-29 00:00:00 '),pd.Timestamp(' 2018-01-30 00:00:00 '),pd.Timestamp(' 2018-01-31 00:00:00 ')]),
                             "% Dly Qt to Traded Qty":pd.DataFrame({"QZO":[58.02,66.94,71.13,63.78,45.75],"QZU":[58.02,66.94,71.13,63.78,45.75]}, index= [pd.Timestamp(' 2018-01-24 00:00:00 '),pd.Timestamp(' 2018-01-25 00:00:00 '),pd.Timestamp(' 2018-01-29 00:00:00 '),pd.Timestamp(' 2018-01-30 00:00:00 '),pd.Timestamp(' 2018-01-31 00:00:00 ')]),
                             "Close":pd.DataFrame({"QZO":[1018.45,1009.55,1012.05,1000.4,986.55],"QZU":[1018.45,1009.55,1012.05,1000.4,986.55]}, index= [pd.Timestamp(' 2018-01-24 00:00:00 '),pd.Timestamp(' 2018-01-25 00:00:00 '),pd.Timestamp(' 2018-01-29 00:00:00 '),pd.Timestamp(' 2018-01-30 00:00:00 '),pd.Timestamp(' 2018-01-31 00:00:00 ')]),
                             "Open":pd.DataFrame({"QZO":[994.0,1018.8,1010.0,1017.5,999.95],"QZU":[994.0,1018.8,1010.0,1017.5,999.95]}, index= [pd.Timestamp(' 2018-01-24 00:00:00 '),pd.Timestamp(' 2018-01-25 00:00:00 '),pd.Timestamp(' 2018-01-29 00:00:00 '),pd.Timestamp(' 2018-01-30 00:00:00 '),pd.Timestamp(' 2018-01-31 00:00:00 ')]),
                             "No. of Trades":pd.DataFrame({"QZO":[158184.0,69123.0,77146.0,40486.0,44282.0],"QZU":[158184.0,69123.0,77146.0,40486.0,44282.0]}, index= [pd.Timestamp(' 2018-01-24 00:00:00 '),pd.Timestamp(' 2018-01-25 00:00:00 '),pd.Timestamp(' 2018-01-29 00:00:00 '),pd.Timestamp(' 2018-01-30 00:00:00 '),pd.Timestamp(' 2018-01-31 00:00:00 ')]),
                             "Deliverable Qty":pd.DataFrame({"QZO":[2689213.0,1776445.0,1427424.0,864658.0,736833.0],"QZU":[2689213.0,1776445.0,1427424.0,864658.0,736833.0]}, index= [pd.Timestamp(' 2018-01-24 00:00:00 '),pd.Timestamp(' 2018-01-25 00:00:00 '),pd.Timestamp(' 2018-01-29 00:00:00 '),pd.Timestamp(' 2018-01-30 00:00:00 '),pd.Timestamp(' 2018-01-31 00:00:00 ')]),
                             "Turnover":pd.DataFrame({"QZO":[4734354679.9,2668184643.8,2037047218.2,1359653985.5,1606671902.35],"QZU":[4734354679.9,2668184643.8,2037047218.2,1359653985.5,1606671902.35]}, index= [pd.Timestamp(' 2018-01-24 00:00:00 '),pd.Timestamp(' 2018-01-25 00:00:00 '),pd.Timestamp(' 2018-01-29 00:00:00 '),pd.Timestamp(' 2018-01-30 00:00:00 '),pd.Timestamp(' 2018-01-31 00:00:00 ')]),
                             "Prev Close":pd.DataFrame({"QZO":[995.35,1018.45,1009.55,1012.05,1000.4],"QZU":[995.35,1018.45,1009.55,1012.05,1000.4]}, index= [pd.Timestamp(' 2018-01-24 00:00:00 '),pd.Timestamp(' 2018-01-25 00:00:00 '),pd.Timestamp(' 2018-01-29 00:00:00 '),pd.Timestamp(' 2018-01-30 00:00:00 '),pd.Timestamp(' 2018-01-31 00:00:00 ')]),
                             "High":pd.DataFrame({"QZO":[1040.7,1020.0,1021.0,1017.5,1017.9],"QZU":[1040.7,1020.0,1021.0,1017.5,1017.9]}, index= [pd.Timestamp(' 2018-01-24 00:00:00 '),pd.Timestamp(' 2018-01-25 00:00:00 '),pd.Timestamp(' 2018-01-29 00:00:00 '),pd.Timestamp(' 2018-01-30 00:00:00 '),pd.Timestamp(' 2018-01-31 00:00:00 ')])}
######## testing getClosingTime
        results["getClosingTime"]=datetime(2018, 1, 31)

    if c==6:
######## testing for checkDate
        parameters["lineItem"]="01-2018-31"
        results["checkDate"]=False
######## testing for isFloat
        parameters["isFloat"]="abc"
        results["isFloat"]=False
######## testing for validateLineItem
        parameters["lineItems"]=["Book"]
        parameters["lineLength"]=2
        results["validateLineItem"]=0
######## testing for parseDataLine
        results["parseDataLine"]=None
######## testing for InstrumentFromFile
        parameters["fileName"]="Folder1/text.txt"
        parameters["instrumentId"]="BPM"
######## testing for processLine
        parameters["line"]="Book"
        results["processLine"]=None
######## testing for processLineIntoInstruments
        parameters["instrumentIds"]=["QZO","QQQ"]
######## testing for NSEStockDataSource
        parameters["folderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["date"]="2018-01-01"
        dataSet["fileData"]=""
        parameters["startDateStr"]="2018/01/01"
        parameters["endDateStr"]="2018/01/01"
        parameters["adjustPrice"]=False
        parameters["downloadId"]=".NS"
        parameters["liveUpdates"]=True
        parameters["pad"]=True
        parameters["stock"]="JPASSOCIAT"
######## testing for getResponseFromUrl
        results["getResponseFromUrl"]="1"
######## testing for getInitialSymbolCountUrl
        results["getInitialSymbolCountUrl"]="https://nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol=JPASSOCIAT"
######## testing for getDataUrl
        results["getDataUrl"]="https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=JPASSOCIAT&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate=01-01-2018&toDate=01-01-2018&dataType=PRICEVOLUMEDELIVERABLE"
        parameters["start"]="01-01-2018"
        parameters["end"]="01-01-2018"
        results["rows"]=[['01-Jan-2018', '26.00', '26.40', '27.25', '24.70', '24.95', '25.10', '25.89', '140366939', '3634070946.35', '96726', '27846810', '19.84']]
        results["headers"]=['Date', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'Average', 'Total Traded Quantity', 'Turnover', 'No. of Trades', 'Deliverable Qty', '% Dly Qt to Traded Qty']
        parameters["csvfileName"]="Folder1/abc.txt"
        results["check"]=['Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n',
                          '01-Jan-2018,26.00,26.40,27.25,24.70,24.95,25.10,25.89,140366939,3634070946.35,96726,27846810,19.84\n']
######## testing getFileName and getFileName1
        results["getFileName"]="Folder1/QQ3Data/JPASSOCIAT_2018-01-01to2018-01-01.csv"
######## testing getInstrumentUpdateFromRow
        parameters["rowdict"]={"Date":"31-Dec-2017", "vol": "2.20", "price": "4.4"}
######## testing getBookDataByFeature
        dataSet["DataFrames"]=pd.DataFrame()
######## testing getClosingTime
        results["getClosingTime"]=None

    if c==7:
######## testing for checkDate
        parameters["lineItem"]="01-2018-31"
        results["checkDate"]=False
######## testing for isFloat
        parameters["isFloat"]="abc"
        results["isFloat"]=False
######## testing for validateLineItem
        parameters["lineItems"]=["Book"]
        parameters["lineLength"]=2
        results["validateLineItem"]=0
######## testing for parseDataLine
        results["parseDataLine"]=None
######## testing for InstrumentFromFile
        parameters["fileName"]="Folder1/text.txt"
        parameters["instrumentId"]="BPM"
######## testing for processLine
        parameters["line"]="Book"
        results["processLine"]=None
######## testing for processLineIntoInstruments
        parameters["instrumentIds"]=["QZO","QQQ"]
######## testing for NSEStockDataSource
        parameters["folderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["date"]="2018-01-01"
        dataSet["fileData"]=""
        parameters["startDateStr"]="2018/01/01"
        parameters["endDateStr"]="2018/01/01"
        parameters["adjustPrice"]=False
        parameters["downloadId"]=".NS"
        parameters["liveUpdates"]=True
        parameters["pad"]=True
        parameters["stock"]=""
######## testing for getResponseFromUrl
        results["getResponseFromUrl"]=None
######## testing for getInitialSymbolCountUrl
        results["getInitialSymbolCountUrl"]="https://nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol="

    return {"dataSet":dataSet,"parameters":parameters,"results":results}
