import pandas as pd
import numpy as np
import time
import os
from datetime import datetime, time, timedelta
from pandas.tseries.holiday import Holiday, AbstractHolidayCalendar
from backtester.instrumentUpdates import *

class Initialize(object):

    def getDataSet(self,c):
            index=[pd.tslib.Timestamp(' 2018-01-01 00:00:00 ')]
            if c==0:
                a=[pd.Timestamp(' 2018-01-01 00:00:00 ')]*12
                dataSet = {"records":[{'datetime': '2011-02-21 14:55:00'},
                                      {'datetime': '2011-02-21 15:00:00'},
                                      {'datetime': '2011-02-21 15:05:00'},
                                      {'datetime': '2011-02-21 15:10:00'}],
                           "datafornse":   ("Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n"
                                            "05-Jan-2018,1352.25,1351.00,1362.95,1348.25,1352.65,1356.55,1355.70,568451,770651233.05,17938,368125,64.76\n"
                                            "08-Jan-2018,1356.55,1348.60,1371.00,1348.60,1370.00,1368.40,1363.11,801796,1092939507.05,28669,536934,66.97\n"
                                            "09-Jan-2018,1368.40,1374.00,1375.90,1356.00,1361.35,1361.30,1364.12,708386,966326814.65,24175,489605,69.12\n"),
                           "DataFramesfornse":{ "Prev Close":pd.DataFrame({"AAE":[1352.25,1356.55,1368.4],"AGG":[1352.25,1356.55,1368.4]}, index= [pd.Timestamp(' 2018-01-05 00:00:00 '),pd.Timestamp(' 2018-01-08 00:00:00 '),pd.Timestamp(' 2018-01-09 00:00:00 ')]),
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
                                                "% Dly Qt to Traded Qty":pd.DataFrame({"AAE":[64.76,66.97,69.12],"AGG":[64.76,66.97,69.12]}, index= [pd.Timestamp(' 2018-01-05 00:00:00 '),pd.Timestamp(' 2018-01-08 00:00:00 '),pd.Timestamp(' 2018-01-09 00:00:00 ')])},
                            "str":("Date,Open,High,Low,Close,Adj Close,Volume\n"
                                   "2018-01-02,1048.339966,1066.939941,1045.229980,1065.000000,1065.000000,1237600\n"
                                   "2018-01-03,1064.310059,1086.290039,1063.209961,1082.479980,1082.479980,1430200\n"
                                   "2018-01-04,1088.000000,1093.569946,1084.001953,1086.400024,1086.400024,1004600\n"
                                   "2018-01-05,1094.000000,1104.250000,1092.000000,1102.229980,1102.229980,1279100\n"
                                   "2018-01-08,1102.229980,1111.270020,1101.619995,1106.939941,1106.939941,1047600\n"),
                            "dsdict":{"AAE":pd.DataFrame({'F0':[48.124,48.189,48.189,48.189],'F1':[0.297,0.297,0.297,0.297],'F2':[-0.1,0.1,0.1,0.1]}, index=[pd.Timestamp('2010-06-02 09:20:00'),pd.Timestamp('2010-06-02 09:25:00'),pd.Timestamp('2010-12-24 15:30:00'),pd.Timestamp('2010-12-27 09:20:00')]),
                                      "AGG":pd.DataFrame({'F0':[0.00,0.00,128.326,127.607],'F1':[0.00,0.00,0.503,0.500]}, index=[pd.Timestamp('2010-06-02 09:20:00'),pd.Timestamp('2010-06-02 09:25:00'),pd.Timestamp('2010-12-24 15:30:00'),pd.Timestamp('2010-12-27 09:20:00')]),
                                     },
                          }

                parameters = {#*************** PARAMETERS FOR data_source_utils *****************"
                              "instrumentId": "GOOG", "startDate": datetime.strptime("1/1/2018","%m/%d/%Y"),
                              "endDate": datetime.strptime("1/9/2018","%m/%d/%Y"), "fileName": "data.txt", "event":'history',
                              "datelist": [datetime.strptime("1/2/2018","%m/%d/%Y"),datetime.strptime("1/1/2018","%m/%d/%Y"),
                                           datetime.strptime("1/4/2018","%m/%d/%Y"),datetime.strptime("1/3/2018","%m/%d/%Y"),
                                           datetime.strptime("1/1/2018","%m/%d/%Y"),datetime.strptime("1/2/2018","%m/%d/%Y"),
                                           datetime.strptime("1/3/2018","%m/%d/%Y"),datetime.strptime("1/4/2018","%m/%d/%Y")],
                              #*************** PARAMETERS FOR data_source *****************"
                              "cachedFolderName":"Folder1/", "dataSetId":"QQ3Data", "dateRange":None,
                              "instrumentIds":["AAE","AGG"],"startDateStr":"2018/01/01","endDateStr":"2018/02/01",
                              "startDateStrforfilterUpdates":"2010/06/02","endDateStrforfilterUpdates":"2010/12/27",
                              #*************** PARAMETERS FOR csv_data_source *****************"
                              "s":1,"downloadUrl":"https://raw.githubusercontent.com/Auquan/test_repo/master",
                              "timeKey":'datetime',"timeStringFormat":"%Y-%m-%d %H:%M:%S","liveUpdates":True,"pad":True,
                              "instrumentIdforcsv":"BYB",
                              #*************** PARAMETERS FOR auquan_data_source *****************"
                              "startDateStrforauquan":"2018/01/01","endDateStrforauquan":"2018/01/02",
                              "lineItem":"2018/01/01","lineItems":["2018/01/01"],"trade_date":datetime.strptime("1/1/2018","%m/%d/%Y"),
                              "instrumentIdsByType":{'a':["AAE","AGG"],'b':["BBA","BPM"]},
                              "fileNameforinstrumentsfromfile":"Folder1/text.txt","instrumentIdforinstrumentsfromfile":"AAE",
                              "line": "",
                              #*************** PARAMETERS FOR logfile_data_source *****************"
                              "fileNameforlogfile":"Folder1/text.txt",
                              #*************** PARAMETERS FOR nse_data_source *****************"
                              "lineItemfornse":"", 'isFloat': "", 'is_number': "","lineItemsfornse":["2018-01-31"],"lineLength":2,
                              "fileNamefornse":"Folder1/text.txt","instrumentIdfornse":"AAE",
                              "linefornse":"ABC","stock":"HINDUNILVR","fileNameforcsv":"Folder1/abc.txt",
                              "startDatefornse":datetime.strptime("1/5/2018","%m/%d/%Y"),"endDatefornse":datetime.strptime("1/9/2018","%m/%d/%Y"),
                              "rowdict":{"Date":"01-Dec-2018", "vol": "231", "price": "451"},
                              }

                results = { #****************** RESULTS FOR data_source_utils*************
                            'timeUpdates'                                      :   [datetime(2018, 1, 1, 0, 0),
                                                                                    datetime(2018, 1, 2, 0, 0),
                                                                                    datetime(2018, 1, 3, 0, 0),
                                                                                    datetime(2018, 1, 4, 0, 0)],
                            'listmul'                                          :   [0.99829, 0.02041, 0.99829, 0.02041, 0.99829, 0.14286, 0.99829, 1.0, 0.99913, 1.0],
                            'listtemp'                                         :   [[0.0, 536.05249, 541.00525, 535.65668, 538.12109, 538.12109, 1794800.0],
                                                                                    [0.0, 562.81537, 573.43695, 561.92029, 567.97693, 567.97693, 1360400.0],
                                                                                    [0.0, 588.26538, 593.21814, 586.27637, 592.82037, 592.82037, 3746900.0],
                                                                                    [0.0, 554.94861, 556.8183, 551.98486, 555.784, 555.784, 1103100.0],
                                                                                    [0.0, 527.98682, 533.13849, 526.61438, 530.1748, 530.1748, 1657900.0],
                                                                                    [0.0, 541.38318, 541.90033, 532.86005, 536.82825, 536.82825, 1978500.0]],
                            #****************** RESULTS FOR data_source*************
                            'getInstrumentIds'                                 :   ['AAE', 'AGG'],
                            'setStartDate'                                     :   datetime(2018, 1, 1, 0, 0),
                            'setEndDate'                                       :   datetime(2018, 2, 1, 0, 0),
                            'setDateRange'                                     :   None,
                            'resulttimeUpdatesforgetGrouped'                   :   [datetime(2010, 6, 2, 9, 20),datetime(2010, 6, 2, 9, 25),datetime(2010, 12, 24, 15, 30),datetime(2010, 12, 27, 9, 20)],
                            #****************** RESULTS FOR csv_data_source*************
                            'is_number'                                        :   True,
                            'getFileNameforcsv'                                :   "Folder1/QQ3Data/BYB.csv",
                            'getAllInstrumentIds'                              :   ['SIZ', 'MLQ', 'MAI', 'PVV', 'IPV', 'DHP', 'EKA', 'WTX', 'EYC', 'YSB', 'SEP', 'INS', 'IIZ', 'DFY', 'OAX', 'HIS',
                                                                                    'QZO', 'ZSB', 'SXH', 'CUY', 'GYQ', 'ARD', 'YCY', 'FXQ', 'CJV', 'OJF', 'DDV', 'EEN', 'SSD', 'FWX', 'AWU', 'ONS',
                                                                                    'KEH', 'ZHU', 'HNM', 'LTN', 'ZKF', 'SJB', 'WCJ', 'JBP', 'EGP', 'FVA', 'JHB', 'AKK', 'QON', 'URZ', 'CAW', 'OSF',
                                                                                    'TDW', 'KMY', 'ATN', 'MLP', 'EMD', 'AGM', 'QCE', 'HRY', 'BPM', 'MPC', 'DIZ', 'GWI', 'FVB', 'DZU', 'GQX', 'WMN',
                                                                                    'ENQ', 'DJV', 'WBM', 'ORH', 'YAE', 'BYZ', 'YXP', 'SLM', 'NMS', 'WJP', 'DGT', 'KCN', 'WWV', 'GOR', 'ZMP', 'QCM',
                                                                                    'VML', 'XZC', 'AJM', 'NLF', 'NTG', 'NSN', 'CSI', 'PES', 'OIL', 'SJL', 'ZFC', 'BST', 'DLL', 'AAE', 'OLY', 'VIC',
                                                                                    'QZU', 'DOE', 'GUY', 'BBA', 'YSL', 'ZGR', 'AGG', 'AQM', 'LUY', 'SNF', 'UNB', 'ZRN', 'VSV', 'SSL', 'VUV', 'ZQY',
                                                                                    'RCL', 'EXR', 'BYB'],
                            "ensureAllInstrumentsFile"                         :    True,
                            #****************** RESULTS FOR auquan_data_source*************
                            'checkDate'                                        :    True,
                            'validateLineItem'                                 :    0,
                            'parseBookDataOptionLine'                          :    None,
                            'get_exp_date'                                     :    datetime(2018, 1, 25, 15, 30),
                            'getFileName'                                      :    "Folder1//a/GOOG/GOOG_20180101.txt",
                            'emitInstrumentUpdates'                            :    [datetime(2016, 1, 1, 9, 30), datetime(2017, 1, 1, 9, 30), datetime(2018, 1, 1, 9, 30)],
                            'countforprocessLine'                              :    1,
                            'currentBookDatalist'                              :    [None],
                            'countforprocessLinesIntoInstruments'              :    0,
                            #****************** RESULTS FOR yahoo_data_source*************
                            'checkDateYahoo'                                   :    False,
                            'validateLineItemYahoo'                            :    0,
                            'parseDataLineYahoo'                               :    None,
                            #****************** RESULTS FOR nse_data_source*************
                            'checkDatefornse'                                  :    False,
                            'isFloat'                                          :    False,
                            'is_numberfornse'                                  :    False,
                            'validateLineItemfornse'                           :    0,
                            'parseDataLine'                                    :    None,
                            'processLine'                                      :    type(None),
                            'getResponseFromUrl'                               :    '1',
                            'getInitialSymbolCountUrl'                         :    "https://nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol=HINDUNILVR",
                            'getDataUrl'                                       :    "https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=HINDUNILVR&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate=05-01-2018&toDate=09-01-2018&dataType=PRICEVOLUMEDELIVERABLE",
                            'getDataResponseForStockrows'                      :    [['05-Jan-2018', '1352.25', '1351.00', '1362.95', '1348.25', '1352.65', '1356.55', '1355.70', '568451', '770651233.05', '17938', '368125', '64.76'],
                                                                                     ['08-Jan-2018', '1356.55', '1348.60', '1371.00', '1348.60', '1370.00', '1368.40', '1363.11', '801796', '1092939507.05', '28669', '536934', '66.97'],
                                                                                     ['09-Jan-2018', '1368.40', '1374.00', '1375.90', '1356.00', '1361.35', '1361.30', '1364.12', '708386', '966326814.65', '24175', '489605', '69.12']],
                            'getDataResponseForStockheader'                    :    ['Date', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'Average', 'Total Traded Quantity', 'Turnover', 'No. of Trades', 'Deliverable Qty', '% Dly Qt to Traded Qty'],
                            'getFileNamefornse'                                :    "Folder1/QQ3Data/HINDUNILVR_2018-01-05to2018-01-05.csv",
                            'getClosingTime'                                   :    datetime(2018, 1, 9),
                            'adjustPriceForSplitAndDiv'                        :    [['2017-12-29', 1354.5, 1359.0, 1374.9, 1350.0, 1362.25, 1367.85, 1366.33, 799006.0, 1091708127.0, 23341, 511548.0, 64.02],
                                                                                     ['2017-12-15', 1321.6, 1328.3, 1335.0, 1310.6, 1323.3, 1324.55, 1322.7, 1420357.0, 1878709412.55, 59459, 1033307.0, 72.75],
                                                                                     ['2017-10-19', 1263.95, 1256.95548, 1261.92369, 1245.72734, 1247.01908, 1249.70191, 1252.67289, 67835.0, 84974948.281, 2845, 18698.0, 27.56],
                                                                                     ['2017-08-07', 1192.1, 1165.54054, 1185.51272, 1163.90103, 1170.45906, 1178.75596, 1176.62957, 868190.0, 1021534584.70787, 40921, 631855.0, 72.78],
                                                                                     ['2017-05-26', 1043.45, 1025.95916, 1030.7835, 1016.45817, 1024.92537, 1024.87615, 1024.36417, 716421.0, 733873861.67069, 26030, 367491.0, 51.3],
                                                                                     ['2017-03-14', 875.2, 867.59293, 900.87101, 865.47613, 898.90189, 899.64031, 883.01111, 2763421.0, 2440125882.40961, 90182, 2050513.0, 74.2],
                                                                                     ['2017-02-10', 850.75, 835.15173, 845.145, 834.56099, 836.92393, 837.76081, 839.45425, 648644.0, 544504433.05434, 28187, 364873.0, 56.25]],
                          }

                return {"dataSet":dataSet, "results":results, "parameters":parameters}

            if c==1:
                dataSet = {"records":[{'datetime': '2011-02-21 14:55:00'},
                                      {'datetime': '2011-02-21 15:00:00'},
                                      {'datetime': '2011-02-21 15:05:00'},
                                      {'datetime': '2011-02-21 15:10:00'}],
                           "datafornse":  ("Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n"
                                           "10-Jan-2018,2457.80,2459.95,2472.00,2420.00,2427.10,2425.80,2436.94,344328,839104989.10,20822,94640,27.49\n"
                                           "11-Jan-2018,2425.80,2427.00,2451.00,2418.00,2424.80,2425.35,2432.89,185159,450471546.10,15411,58215,31.44\n"
                                           "12-Jan-2018,2425.35,2433.00,2453.85,2413.65,2449.00,2447.65,2435.83,355780,866619682.15,21392,129447,36.38\n"
                                           "15-Jan-2018,2447.65,2447.00,2461.25,2425.05,2435.00,2431.75,2443.25,156821,383152622.55,11089,45207,28.83\n"),
                           "DataFramesfornse":{ "Average":pd.DataFrame({"BBA":[2436.94,2432.89,2435.83,2443.25],"BST":[2436.94,2432.89,2435.83,2443.25]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')]),
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
                                                "Total Traded Quantity":pd.DataFrame({"BBA":[344328.0,185159.0,355780.0,156821.0],"BST":[344328.0,185159.0,355780.0,156821.0]}, index= [pd.Timestamp(' 2018-01-10 00:00:00 '),pd.Timestamp(' 2018-01-11 00:00:00 '),pd.Timestamp(' 2018-01-12 00:00:00 '),pd.Timestamp(' 2018-01-15 00:00:00 ')])
                                              },
                          }

                parameters = {#*************** PARAMETERS FOR data_source_utils *****************"
                              "instrumentId": "AAA", "startDate": datetime.strptime("1/1/2018","%m/%d/%Y"),
                              "endDate": datetime.strptime("2/1/2018","%m/%d/%Y"), "fileName": "data.txt", "event":'history',
                              "datelist": [datetime.strptime("1/2/2018","%m/%d/%Y"),datetime.strptime("1/1/2018","%m/%d/%Y"),
                                           datetime.strptime("1/4/2018","%m/%d/%Y"),datetime.strptime("1/3/2018","%m/%d/%Y"),
                                           datetime.strptime("1/1/2018","%m/%d/%Y"),datetime.strptime("1/2/2018","%m/%d/%Y"),
                                           datetime.strptime("1/3/2018","%m/%d/%Y"),datetime.strptime("1/4/2018","%m/%d/%Y")],
                              #*************** PARAMETERS FOR data_source *****************"
                              "cachedFolderName":"Folder1/", "dataSetId":"QQ3Data",
                              "instrumentIds":["BBA","BST"],"startDateStr":"2018/01/01","endDateStr":"2018/02/01",
                              #*************** PARAMETERS FOR csv_data_source *****************"
                              "s":1.02,"downloadUrl":"https://raw.githubusercontent.com/Auquan/test_repo/master",
                              "timeKey":'datetime',"timeStringFormat":"%Y-%m-%d %H:%M:%S","liveUpdates":True,"pad":True,
                              "instrumentIdforcsv":"MAI",
                              #*************** PARAMETERS FOR auquan_data_source *****************"
                              "startDateStrforauquan":"2018/01/01","endDateStrforauquan":"2018/01/02",
                              "lineItem":"2018/01/","lineItems":["2018/01/01","09:30:00","Book",100,"AAA"],
                              "trade_date":datetime.strptime("12/15/2018","%m/%d/%Y"),
                              "instrumentIdsByType":{'a':["AAE","AGG"],'b':["BBA","BPM"]},
                              "fileNameforinstrumentsfromfile":"Folder1/text.txt","instrumentIdforinstrumentsfromfile":"AGG",
                              "line":"2017/01/01 09:30:00:000000 Book 100 AAA\n2018/01/01 09:30:00:000000 Book 100 AAA\n2019/01/01 09:30:00:000000 Book 100 AAA",
                              #*************** PARAMETERS FOR logfile_data_source *****************"
                              "fileNameforlogfile":"Folder1/text.txt",
                              #*************** PARAMETERS FOR nse_data_source *****************"
                              "lineItemfornse":"31-Dec-2018", 'isFloat': "ABC", 'is_number': "ABC",
                              "lineItemsfornse":["Date","",20,30,10,21,22,20,20],"lineLength":9,
                              "fileNamefornse":"Folder1/text.txt","instrumentIdfornse":"AGG",
                              "linefornse":"31-Dec-2018, ,100,30,1,2,11,20,100","stock":"DRREDDY","fileNameforcsv":"Folder1/abc.txt",
                              "startDatefornse":datetime.strptime("1/10/2018","%m/%d/%Y"),"endDatefornse":datetime.strptime("1/15/2018","%m/%d/%Y"),
                              "rowdict":{"Date":"02-Jan-2015", "vol": "456", "price": "444"},
                              }

                results = { #****************** RESULTS FOR data_source_utils*************
                            'timeUpdates'                                      :   [datetime(2018, 1, 1, 0, 0),
                                                                                    datetime(2018, 1, 2, 0, 0),
                                                                                    datetime(2018, 1, 3, 0, 0),
                                                                                    datetime(2018, 1, 4, 0, 0)],
                            #****************** RESULTS FOR data_source*************
                            'getInstrumentIds'                                 :   ['BBA', 'BST'],
                            #****************** RESULTS FOR csv_data_source*************
                            'is_number'                                        :   True,
                            'getFileNameforcsv'                                :   "Folder1/QQ3Data/MAI.csv",
                            'getAllInstrumentIds'                              :   ['SIZ', 'MLQ', 'MAI', 'PVV', 'IPV', 'DHP', 'EKA', 'WTX', 'EYC', 'YSB', 'SEP', 'INS', 'IIZ', 'DFY', 'OAX', 'HIS',
                                                                                    'QZO', 'ZSB', 'SXH', 'CUY', 'GYQ', 'ARD', 'YCY', 'FXQ', 'CJV', 'OJF', 'DDV', 'EEN', 'SSD', 'FWX', 'AWU', 'ONS',
                                                                                    'KEH', 'ZHU', 'HNM', 'LTN', 'ZKF', 'SJB', 'WCJ', 'JBP', 'EGP', 'FVA', 'JHB', 'AKK', 'QON', 'URZ', 'CAW', 'OSF',
                                                                                    'TDW', 'KMY', 'ATN', 'MLP', 'EMD', 'AGM', 'QCE', 'HRY', 'BPM', 'MPC', 'DIZ', 'GWI', 'FVB', 'DZU', 'GQX', 'WMN',
                                                                                    'ENQ', 'DJV', 'WBM', 'ORH', 'YAE', 'BYZ', 'YXP', 'SLM', 'NMS', 'WJP', 'DGT', 'KCN', 'WWV', 'GOR', 'ZMP', 'QCM',
                                                                                    'VML', 'XZC', 'AJM', 'NLF', 'NTG', 'NSN', 'CSI', 'PES', 'OIL', 'SJL', 'ZFC', 'BST', 'DLL', 'AAE', 'OLY', 'VIC',
                                                                                    'QZU', 'DOE', 'GUY', 'BBA', 'YSL', 'ZGR', 'AGG', 'AQM', 'LUY', 'SNF', 'UNB', 'ZRN', 'VSV', 'SSL', 'VUV', 'ZQY',
                                                                                    'RCL', 'EXR', 'BYB'],
                            "ensureAllInstrumentsFile"                         :    True,
                            #****************** RESULTS FOR auquan_data_source*************
                            'checkDate'                                        :    False,
                            'validateLineItem'                                 :    1,
                            'parseBookDataOptionLine'                          :    None,
                            'get_exp_date'                                     :    datetime(2018, 12, 27, 15, 30),
                            'getFileName'                                      :    "Folder1//a/AAA/AAA_20180101.txt",
                            'countforprocessLine'                              :    3,
                            'currentBookDatalist'                              :    [None, None, None],
                            'countforprocessLinesIntoInstruments'              :    3,
                            #****************** RESULTS FOR yahoo_data_source*************
                            'checkDateYahoo'                                        :    False,
                            'validateLineItemYahoo'                                 :    0,
                            'parseDataLineYahoo'                          :    None,
                            #****************** RESULTS FOR nse_data_source*************
                            'checkDatefornse'                                  :    True,
                            'isFloat'                                          :    False,
                            'is_numberfornse'                                  :    False,
                            'validateLineItemfornse'                           :    1,
                            'parseDataLine'                                    :    {'last': 21.0, 'low': 10.0, 'average': 20.0, 'volume': 20.0, 'close': 22.0, 'high': 30.0, 'open': 20.0},
                            'processLine'                                      :    StockInstrumentUpdate,
                            'getResponseFromUrl'                               :    '1',
                            'getInitialSymbolCountUrl'                         :    "https://nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol=DRREDDY",
                            'getDataUrl'                                       :    "https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=DRREDDY&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate=10-01-2018&toDate=15-01-2018&dataType=PRICEVOLUMEDELIVERABLE",
                            'getDataResponseForStockrows'                      :    [['10-Jan-2018', '2457.80', '2459.95', '2472.00', '2420.00', '2427.10', '2425.80', '2436.94', '344328', '839104989.10', '20822', '94640', '27.49'],
                                                                                     ['11-Jan-2018', '2425.80', '2427.00', '2451.00', '2418.00', '2424.80', '2425.35', '2432.89', '185159', '450471546.10', '15411', '58215', '31.44'],
                                                                                     ['12-Jan-2018', '2425.35', '2433.00', '2453.85', '2413.65', '2449.00', '2447.65', '2435.83', '355780', '866619682.15', '21392', '129447', '36.38'],
                                                                                     ['15-Jan-2018', '2447.65', '2447.00', '2461.25', '2425.05', '2435.00', '2431.75', '2443.25', '156821', '383152622.55', '11089', '45207', '28.83']],
                            'getDataResponseForStockheader'                    :    ['Date', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'Average', 'Total Traded Quantity', 'Turnover', 'No. of Trades', 'Deliverable Qty', '% Dly Qt to Traded Qty'],
                            'getFileNamefornse'                                :    "Folder1/QQ3Data/DRREDDY_2018-01-10to2018-01-10.csv",
                            'getClosingTime'                                   :    datetime(2018, 1, 15),
                            'adjustPriceForSplitAndDiv'                        :    [['2017-12-29', 2430.0, 2429.95, 2445.95, 2403.15, 2414.25, 2414.2, 2424.53, 331967.0, 804864049.05, 20651, 104575.0, 31.5],
                                                                                     ['2017-12-15', 2310.65, 2325.0, 2380.0, 2316.45, 2370.0, 2371.5, 2350.22, 743680.0, 1747810478.65, 43902, 355975.0, 47.87],
                                                                                     ['2017-10-19', 2385.4, 2385.0, 2387.0, 2362.05, 2376.9, 2373.05, 2374.37, 47303.0, 112314876.05, 2637, 13195.0, 27.89],
                                                                                     ['2017-08-07', 2239.55, 2240.0, 2257.0, 2200.0, 2202.0, 2206.95, 2229.8, 736078.0, 1641306908.35, 39569, 355427.0, 48.29],
                                                                                     ['2017-05-26', 2427.7, 2481.4626, 2491.33882, 2385.97592, 2402.00617, 2396.49732, 2417.32176, 721031.0, 1742962042.99587, 38740, 328084.0, 45.5],
                                                                                     ['2017-03-14', 2715.85, 2726.33333, 2734.4229, 2696.55578, 2720.6756, 2720.6756, 2715.63326, 497842.0, 1351956224.90682, 49861, 247207.0, 49.66],
                                                                                     ['2017-02-10', 3023.1, 3002.47049, 3011.85042, 2947.97757, 2953.88345, 2953.98271, 2969.02037, 315001.0, 935245461.30989, 32188, 190665.0, 60.53]],
                        }

                return {"dataSet":dataSet, "results":results, "parameters":parameters}
            if c==2:
                dataSet = {"records":[{'datetime': '2011-02-21 14:55:00'},
                                      {'datetime': '2011-02-21 15:00:00'},
                                      {'datetime': '2011-02-21 15:05:00'},
                                      {'datetime': '2011-02-21 15:10:00'}],
                           "datafornse":("Date,Prev Close,Open,High,Low,Last,Close,Average,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty\n"
                                         "24-Jan-2018,995.35,994.00,1040.70,992.00,1020.00,1018.45,1021.46,4634888,4734354679.90,158184,2689213,58.02\n"
                                         "25-Jan-2018,1018.45,1018.80,1020.00,990.05,1020.00,1009.55,1005.45,2653727,2668184643.80,69123,1776445,66.94\n"
                                         "29-Jan-2018,1009.55,1010.00,1021.00,1005.05,1005.75,1012.05,1015.15,2006648,2037047218.20,77146,1427424,71.13\n"
                                         "30-Jan-2018,1012.05,1017.50,1017.50,998.00,1000.00,1000.40,1002.93,1355676,1359653985.50,40486,864658,63.78\n"
                                         "31-Jan-2018,1000.40,999.95,1017.90,981.70,984.05,986.55,997.58,1610572,1606671902.35,44282,736833,45.75\n"),
                           "DataFramesfornse":{"Total Traded Quantity":pd.DataFrame({"QZO":[4634888.0,2653727.0,2006648.0,1355676.0,1610572.0],"QZU":[4634888.0,2653727.0,2006648.0,1355676.0,1610572.0]}, index= [pd.Timestamp(' 2018-01-24 00:00:00 '),pd.Timestamp(' 2018-01-25 00:00:00 '),pd.Timestamp(' 2018-01-29 00:00:00 '),pd.Timestamp(' 2018-01-30 00:00:00 '),pd.Timestamp(' 2018-01-31 00:00:00 ')]),
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
                                                "High":pd.DataFrame({"QZO":[1040.7,1020.0,1021.0,1017.5,1017.9],"QZU":[1040.7,1020.0,1021.0,1017.5,1017.9]}, index= [pd.Timestamp(' 2018-01-24 00:00:00 '),pd.Timestamp(' 2018-01-25 00:00:00 '),pd.Timestamp(' 2018-01-29 00:00:00 '),pd.Timestamp(' 2018-01-30 00:00:00 '),pd.Timestamp(' 2018-01-31 00:00:00 ')])
                                              },
                          }

                parameters = {#*************** PARAMETERS FOR data_source_utils *****************"
                              "instrumentId": "GOOG", "startDate": datetime.strptime("1/1/2018","%m/%d/%Y"),
                              "endDate": datetime.strptime("2/1/2018","%m/%d/%Y"), "fileName": "data.txt", "event":'history',
                              "datelist": [datetime.strptime("1/2/2018","%m/%d/%Y"),datetime.strptime("1/1/2018","%m/%d/%Y"),
                                           datetime.strptime("1/4/2018","%m/%d/%Y"),datetime.strptime("1/3/2018","%m/%d/%Y"),
                                           datetime.strptime("1/1/2018","%m/%d/%Y"),datetime.strptime("1/2/2018","%m/%d/%Y"),
                                           datetime.strptime("1/3/2018","%m/%d/%Y"),datetime.strptime("1/4/2018","%m/%d/%Y")],
                              #*************** PARAMETERS FOR data_source *****************"
                              "cachedFolderName":"Folder1/", "dataSetId":"QQ3Data",
                              "instrumentIds":["QZO","QZU"],"startDateStr":"2018/01/01","endDateStr":"2018/02/01",
                              #*************** PARAMETERS FOR csv_data_source *****************"
                              "s":"abc","downloadUrl":"https://raw.githubuserconnnntent.com/Auquan/test_repo/master",
                              "timeKey":'datetime',"timeStringFormat":"%Y-%m-%d %H:%M:%S","liveUpdates":True,"pad":True,
                              "instrumentIdforcsv":"PVV",
                              #*************** PARAMETERS FOR auquan_data_source *****************"
                              "startDateStrforauquan":"2018/01/01","endDateStrforauquan":"2018/01/02",
                              "lineItem":"2018/01/01","lineItems":["2018/01/01","09:30:00","Greek:",100,100],
                              "trade_date":datetime.strptime("12/31/2018","%m/%d/%Y"),
                              "instrumentIdsByType":{'a':["AAE","AGG"],'b':["BBA","BPM"]},
                              "fileNameforinstrumentsfromfile":"Folder1/text.txt","instrumentIdforinstrumentsfromfile":"BBA",
                              "line":"2016/01/01 09:30:00:000000 Book 100 AAA\n2015/01/01 09:30:00:000000 Book 100 AAA",
                              #*************** PARAMETERS FOR logfile_data_source *****************"
                              "fileNameforlogfile":"Folder1/text.txt",
                              #*************** PARAMETERS FOR nse_data_source *****************"
                              "lineItemfornse":"2018-05-21", 'isFloat': "123", 'is_number': "123",
                              "lineItemsfornse":["2018-05-21","",25.80,30.52,1.02,2,1.1,20.24,1.1],"lineLength":9,
                              "fileNamefornse":"Folder1/text.txt","instrumentIdfornse":"BBA",
                              "linefornse":"2018-05-21, ,25.80,30.52,1.02,2,1.1,20.24","stock":"HCLTECH","fileNameforcsv":"Folder1/abc.txt",
                              "startDatefornse":datetime.strptime("1/24/2018","%m/%d/%Y"),"endDatefornse":datetime.strptime("1/31/2018","%m/%d/%Y"),
                              "rowdict":{"Date":"08-Feb-2019", "vol": "222", "price": "111"},
                              }

                results = { #****************** RESULTS FOR data_source_utils*************
                            'timeUpdates'                                      :   [datetime(2018, 1, 1, 0, 0),
                                                                                    datetime(2018, 1, 2, 0, 0),
                                                                                    datetime(2018, 1, 3, 0, 0),
                                                                                    datetime(2018, 1, 4, 0, 0)],
                            #****************** RESULTS FOR data_source*************
                            'getInstrumentIds'                                 :   ['QZO', 'QZU'],
                            #****************** RESULTS FOR csv_data_source*************
                            'is_number'                                        :   False,
                            'getFileNameforcsv'                                :   "Folder1/QQ3Data/PVV.csv",
                            'getAllInstrumentIds'                              :   [],
                            "ensureAllInstrumentsFile"                         :   False,
                            #****************** RESULTS FOR auquan_data_source*************
                            'checkDate'                                        :    True,
                            'validateLineItem'                                 :    2,
                            'parseBookDataOptionLine'                          :    None,
                            'get_exp_date'                                     :    datetime(2019, 1, 31, 15, 30),
                            'getFileName'                                      :    "Folder1//a/GOOG/GOOG_20180101.txt",
                            'countforprocessLine'                              :    2,
                            'currentBookDatalist'                              :    [None, None],
                            'countforprocessLinesIntoInstruments'              :    2,
                            #****************** RESULTS FOR yahoo_data_source*************
                            'checkDateYahoo'                                        :    False,
                            'validateLineItemYahoo'                                 :    0,
                            'parseDataLineYahoo'                          :    None,
                            #****************** RESULTS FOR nse_data_source*************
                            'checkDatefornse'                                  :    True,
                            'isFloat'                                          :    123.0,
                            'is_numberfornse'                                  :    True,
                            'validateLineItemfornse'                           :    2,
                            'parseDataLine'                                    :    {'last': 2.0, 'low': 1.02, 'average': 20.24, 'volume': 1.1, 'close': 1.1, 'high': 30.52, 'open': 25.8},
                            'processLine'                                      :    type(None),
                            'getResponseFromUrl'                               :    '1',
                            'getInitialSymbolCountUrl'                         :    "https://nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol=HCLTECH",
                            'getDataUrl'                                       :    "https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=HCLTECH&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate=24-01-2018&toDate=31-01-2018&dataType=PRICEVOLUMEDELIVERABLE",
                            'getDataResponseForStockrows'                      :    [['24-Jan-2018', '995.35', '994.00', '1040.70', '992.00', '1020.00', '1018.45', '1021.46', '4634888', '4734354679.90', '158184', '2689213', '58.02'],
                                                                                     ['25-Jan-2018', '1018.45', '1018.80', '1020.00', '990.05', '1020.00', '1009.55', '1005.45', '2653727', '2668184643.80', '69123', '1776445', '66.94'],
                                                                                     ['29-Jan-2018', '1009.55', '1010.00', '1021.00', '1005.05', '1005.75', '1012.05', '1015.15', '2006648', '2037047218.20', '77146', '1427424', '71.13'],
                                                                                     ['30-Jan-2018', '1012.05', '1017.50', '1017.50', '998.00', '1000.00', '1000.40', '1002.93', '1355676', '1359653985.50', '40486', '864658', '63.78'],
                                                                                     ['31-Jan-2018', '1000.40', '999.95', '1017.90', '981.70', '984.05', '986.55', '997.58', '1610572', '1606671902.35', '44282', '736833', '45.75']],
                            'getDataResponseForStockheader'                    :    ['Date', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'Average', 'Total Traded Quantity', 'Turnover', 'No. of Trades', 'Deliverable Qty', '% Dly Qt to Traded Qty'],
                            'getFileNamefornse'                                :    "Folder1/QQ3Data/HCLTECH_2018-01-24to2018-01-24.csv",
                            'getClosingTime'                                   :    datetime(2018, 1, 31),
                            'adjustPriceForSplitAndDiv'                        :    [['2017-12-29', 878.3, 878.3, 901.75, 875.0, 895.95, 890.5, 891.16, 1546925.0, 1378556459.4, 40882, 980177.0, 63.36],
                                                                                     ['2017-12-15', 882.85, 888.9, 896.45, 885.0, 891.85, 891.8, 891.49, 2234611.0, 1992129512.65, 115333, 1755013.0, 78.54],
                                                                                     ['2017-10-19', 923.7, 914.41931, 923.79694, 914.41931, 921.8017, 920.10575, 919.13805, 29194.0, 26833298.10128, 1220, 10746.0, 36.81],
                                                                                     ['2017-08-07', 890.65, 887.88259, 892.57141, 879.30305, 883.89211, 883.89211, 883.75244, 823485.0, 727753147.80756, 36779, 639105.0, 77.61],
                                                                                     ['2017-05-26', 859.6, 853.70532, 861.96666, 851.4658, 854.05369, 855.0988, 856.30316, 1302415.0, 1115259930.67705, 74293, 973969.0, 74.78],
                                                                                     ['2017-03-14', 846.35, 854.92835, 854.92835, 840.10301, 842.07972, 843.66109, 845.23258, 1585864.0, 1340419066.44122, 60861, 1116242.0, 70.39],
                                                                                     ['2017-02-10', 819.7, 812.52786, 820.33588, 802.84197, 820.23704, 818.75451, 814.31679, 1775497.0, 1445822851.54743, 46490, 1001902.0, 56.43]],
                        }

                return {"dataSet":dataSet, "results":results, "parameters":parameters}
            if c==3:
                dataSet = {"records":[{'datetime': '2011-02-21 14:55:00'},
                                      {'datetime': '2011-02-21 15:00:00'},
                                      {'datetime': '2011-02-21 15:05:00'},
                                      {'datetime': '2011-02-21 15:10:00'}],
                           "datafornse":"",
                           "DataFramesfornse":{},
                          }

                parameters = {#*************** PARAMETERS FOR data_source_utils *****************"
                              "instrumentId": "GOOG", "startDate": datetime.strptime("1/1/2018","%m/%d/%Y"),
                              "endDate": datetime.strptime("2/1/2018","%m/%d/%Y"), "fileName": "data.txt", "event":'history',
                              "datelist": [datetime.strptime("1/2/2018","%m/%d/%Y"),datetime.strptime("1/1/2018","%m/%d/%Y"),
                                           datetime.strptime("1/4/2018","%m/%d/%Y"),datetime.strptime("1/3/2018","%m/%d/%Y"),
                                           datetime.strptime("1/1/2018","%m/%d/%Y"),datetime.strptime("1/2/2018","%m/%d/%Y"),
                                           datetime.strptime("1/3/2018","%m/%d/%Y"),datetime.strptime("1/4/2018","%m/%d/%Y")],
                              #*************** PARAMETERS FOR data_source *****************"
                              "cachedFolderName":"Folder1/", "dataSetId":"QQ3Data",
                              "instrumentIds":["QZO","QQQ"],"startDateStr":"2018/01/01","endDateStr":"2018/02/01",
                              #*************** PARAMETERS FOR csv_data_source *****************"
                              "s":"abc","downloadUrl":"https://raw.githubusercontent.com/Auquan/test_repo/master",
                              "timeKey":'datetime',"timeStringFormat":"%Y-%m-%d %H:%M:%S","liveUpdates":True,"pad":True,
                              "instrumentIdforcsv":"PVV",
                              #*************** PARAMETERS FOR auquan_data_source *****************"
                              "startDateStrforauquan":"2018/01/01","endDateStrforauquan":"2018/01/02",
                              "lineItem":"2018/01/01","lineItems":["2018/01/01",100,50,"|",200,100,"ABC"],
                              "trade_date":datetime.strptime("10/06/2016","%m/%d/%Y"),
                              "instrumentIdsByType":{'a':["AAE","AGG"],'b':["BBA","BPM"]},
                              "fileNameforinstrumentsfromfile":"Folder1/text.txt","instrumentIdforinstrumentsfromfile":"BPM",
                              "line":"2018/01/01 100 50 | 200 100 ABC",
                              #*************** PARAMETERS FOR logfile_data_source *****************"
                              "fileNameforlogfile":"Folder1/text.txt",
                              #*************** PARAMETERS FOR nse_data_source *****************"
                              "lineItemfornse":"01-2018-31", 'isFloat': "123.45", 'is_number': "123.45",
                              "lineItemsfornse":["Book"],"lineLength":2,
                              "fileNamefornse":"Folder1/text.txt","instrumentIdfornse":"BPM",
                              "linefornse":"Book","stock":"JPASSOCIAT","fileNameforcsv":"Folder1/abc.txt",
                              "startDatefornse":datetime.strptime("1/1/2018","%m/%d/%Y"),"endDatefornse":datetime.strptime("1/1/2018","%m/%d/%Y"),
                              "rowdict":{"Date":"31-Dec-2017", "vol": "2.20", "price": "4.4"},
                              }

                results = { #****************** RESULTS FOR data_source_utils*************
                            'timeUpdates'                                      :   [datetime(2018, 1, 1, 0, 0),
                                                                                    datetime(2018, 1, 2, 0, 0),
                                                                                    datetime(2018, 1, 3, 0, 0),
                                                                                    datetime(2018, 1, 4, 0, 0)],
                            #****************** RESULTS FOR data_source*************
                            'getInstrumentIds'                                 :   ['QZO', 'QZU'],
                            #****************** RESULTS FOR csv_data_source*************
                            'is_number'                                        :   False,
                            'getFileNameforcsv'                                :   "Folder1/QQ3Data/PVV.csv",
                            'getAllInstrumentIds'                              :   ['SIZ', 'MLQ', 'MAI', 'PVV', 'IPV', 'DHP', 'EKA', 'WTX', 'EYC', 'YSB', 'SEP', 'INS', 'IIZ', 'DFY', 'OAX', 'HIS',
                                                                                    'QZO', 'ZSB', 'SXH', 'CUY', 'GYQ', 'ARD', 'YCY', 'FXQ', 'CJV', 'OJF', 'DDV', 'EEN', 'SSD', 'FWX', 'AWU', 'ONS',
                                                                                    'KEH', 'ZHU', 'HNM', 'LTN', 'ZKF', 'SJB', 'WCJ', 'JBP', 'EGP', 'FVA', 'JHB', 'AKK', 'QON', 'URZ', 'CAW', 'OSF',
                                                                                    'TDW', 'KMY', 'ATN', 'MLP', 'EMD', 'AGM', 'QCE', 'HRY', 'BPM', 'MPC', 'DIZ', 'GWI', 'FVB', 'DZU', 'GQX', 'WMN',
                                                                                    'ENQ', 'DJV', 'WBM', 'ORH', 'YAE', 'BYZ', 'YXP', 'SLM', 'NMS', 'WJP', 'DGT', 'KCN', 'WWV', 'GOR', 'ZMP', 'QCM',
                                                                                    'VML', 'XZC', 'AJM', 'NLF', 'NTG', 'NSN', 'CSI', 'PES', 'OIL', 'SJL', 'ZFC', 'BST', 'DLL', 'AAE', 'OLY', 'VIC',
                                                                                    'QZU', 'DOE', 'GUY', 'BBA', 'YSL', 'ZGR', 'AGG', 'AQM', 'LUY', 'SNF', 'UNB', 'ZRN', 'VSV', 'SSL', 'VUV', 'ZQY',
                                                                                    'RCL', 'EXR', 'BYB'],
                            "ensureAllInstrumentsFile"                         :    True,
                            #****************** RESULTS FOR auquan_data_source*************
                            'checkDate'                                        :    True,
                            'validateLineItem'                                 :    3,
                            'parseBookDataOptionLine'                          :    {'bidVolume': 100.0, 'askPrice': 200.0, 'bidPrice': 50.0, 'askVolume': 100.0},
                            'get_exp_date'                                     :    datetime(2016, 10, 27, 15, 30),
                            'getFileName'                                      :    "Folder1//a/GOOG/GOOG_20180101.txt",
                            'countforprocessLine'                              :    1,
                            'currentBookDatalist'                              :    [{'bidVolume': 100.0, 'askPrice': 200.0, 'bidPrice': 50.0, 'askVolume': 100.0}],
                            'countforprocessLinesIntoInstruments'              :    0,
                            #****************** RESULTS FOR yahoo_data_source*************
                            'checkDateYahoo'                                        :    False,
                            'validateLineItemYahoo'                                 :    0,
                            'parseDataLineYahoo'                          :    {'open': 100,'high': 50,'low': "|",'close': 200,
                                                                                'adjClose' : 100,'volume':"ABC"},
                            #****************** RESULTS FOR nse_data_source*************
                            'checkDatefornse'                                  :    False,
                            'isFloat'                                          :    123.45,
                            'is_numberfornse'                                  :    True,
                            'validateLineItemfornse'                           :    0,
                            'parseDataLine'                                    :    None,
                            'processLine'                                      :    type(None),
                            'getResponseFromUrl'                               :    '1',
                            'getInitialSymbolCountUrl'                         :    "https://nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol=JPASSOCIAT",
                            'getDataUrl'                                       :    "https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=JPASSOCIAT&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate=01-01-2018&toDate=01-01-2018&dataType=PRICEVOLUMEDELIVERABLE",
                            'getDataResponseForStockrows'                      :    [['01-Jan-2018', '26.00', '26.40', '27.25', '24.70', '24.95', '25.10', '25.89', '140366939', '3634070946.35', '96726', '27846810', '19.84']],
                            'getDataResponseForStockheader'                    :    ['Date', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'Average', 'Total Traded Quantity', 'Turnover', 'No. of Trades', 'Deliverable Qty', '% Dly Qt to Traded Qty'],
                            'getFileNamefornse'                                :    "Folder1/QQ3Data/JPASSOCIAT_2018-01-01to2018-01-01.csv",
                            'adjustPriceForSplitAndDiv'                        :    [['2017-12-29', 23.2, 23.4, 27.3, 23.3, 26.15, 26.0, 25.63, 293435834.0, 7519329510.2, 147626, 66899709.0, 22.8],
                                                                                     ['2017-12-15', 17.6, 17.75, 18.0, 17.35, 17.45, 17.55, 17.64, 36819322.0, 649612580.05, 22559, 9032696.0, 24.53],
                                                                                     ['2017-10-19', 18.9, 19.0, 19.2, 18.45, 18.6, 18.8, 18.91, 14516160.0, 274433634.9, 8888, 3811275.0, 26.26],
                                                                                     ['2017-08-07', 25.35, 27.5, 30.15, 27.0, 28.85, 28.95, 28.91, 155900716.0, 4507642443.2, 105812, 34733667.0, 22.28],
                                                                                     ['2017-05-26', 11.5, 12.0, 13.15, 11.05, 12.6, 12.65, 12.45, 148164830.0, 1843915291.8, 62929, 26750896.0, 18.05],
                                                                                     ['2017-03-14', 14.95, 14.9, 15.1, 13.4, 14.2, 14.05, 14.01, 103064085.0, 1444351771.65, 40215, 20635542.0, 20.02],
                                                                                     ['2017-02-10', 14.05, 14.25, 14.35, 13.15, 13.45, 13.4, 13.71, 40417866.0, 554179030.0, 15818, 8401704.0, 20.79]],
                        }

                return {"dataSet":dataSet, "results":results, "parameters":parameters}
