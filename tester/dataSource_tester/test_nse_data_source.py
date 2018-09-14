import os,sys,shutil
sys.path.append(os.path.abspath('../..'))
from backtester.dataSource.nse_data_source import *
from backtester.instrumentUpdates import *
from backtester.logger import *
import os,sys,shutil
from datetime import datetime, time, timedelta
from unittest.mock import Mock, MagicMock
import pytest
import pandas as pd
from initializeds import Initialize
import os

def test_nse_data_source():
        initialize=Initialize()
        for c in range(0,4):
                dataSet = initialize.getDataSet(c)
                data=dataSet["dataSet"]
                parameters=dataSet["parameters"]
                results=dataSet["results"]
                assert checkDate(parameters["lineItemfornse"]) == results["checkDatefornse"]
                assert checkTimestamp(parameters["lineItemfornse"]) == True
                assert isFloat(parameters["isFloat"]) == results["isFloat"]
                assert is_number(parameters["is_number"]) == results["is_numberfornse"]
                assert validateLineItem(parameters["lineItemsfornse"],parameters["lineLength"]) == results["validateLineItemfornse"]
                assert parseDataLine(parameters["lineItemsfornse"],parameters["lineLength"]) == results["parseDataLine"]
                instrumentsfromfile=InstrumentsFromFile(parameters["fileNamefornse"],parameters["instrumentIdfornse"])
                assert isinstance(instrumentsfromfile.processLine(parameters["linefornse"],parameters["lineLength"]),results["processLine"])
                os.makedirs(os.path.dirname(parameters["fileNamefornse"]), exist_ok=True)
                with open(parameters["fileNamefornse"], 'w') as f:
                        f.write(parameters["linefornse"])
                if c!=1:
                        assert instrumentsfromfile.processLinesIntoInstruments(parameters["lineLength"])==[]
                else:
                        count=0
                        for i in instrumentsfromfile.processLinesIntoInstruments(parameters["lineLength"]):
                                assert isinstance(i,results["processLine"])
                                count+=1
                        assert count==1
                for i in parameters["instrumentIds"]:
                        date=parameters["startDatefornse"].strftime("%Y-%m-%d")
                        filepath="%s%s/%s_%sto%s.csv"%(parameters["cachedFolderName"],parameters["dataSetId"],i,date,date)
                        os.makedirs(os.path.dirname(filepath), exist_ok=True)
                        with open(filepath, 'w') as f:
                                f.write(data["datafornse"])
                nsestockdatasource=NSEStockDataSource(parameters["cachedFolderName"],parameters["dataSetId"],
                                                      parameters["instrumentIds"],datetime.strftime(parameters["startDatefornse"], '%Y/%m/%d'),
                                                      datetime.strftime(parameters["endDatefornse"], '%Y/%m/%d'),
                                                      False,".SN",parameters["liveUpdates"])
                url="https://nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol=%s" % (parameters["stock"])
                assert nsestockdatasource.getResponseFromUrl(url,False).strip() == results["getResponseFromUrl"]
                assert nsestockdatasource.getInitialSymbolCountUrl(parameters["stock"]) == results["getInitialSymbolCountUrl"]
                assert nsestockdatasource.getSymbolCountForStock(parameters["stock"]) == results["getResponseFromUrl"]
                assert nsestockdatasource.getDataUrl(parameters["stock"],results["getResponseFromUrl"],datetime.strftime(parameters["startDatefornse"], '%d-%m-%Y'),datetime.strftime(parameters["endDatefornse"], '%d-%m-%Y')) == results["getDataUrl"]
                result= (nsestockdatasource.getDataResponseForStock(parameters["stock"],results["getResponseFromUrl"],datetime.strftime(parameters["startDatefornse"], '%d-%m-%Y'),datetime.strftime(parameters["endDatefornse"], '%d-%m-%Y') ))
                dataRows = BeautifulSoup(result, 'lxml').find(id="csvContentDiv").get_text().split(":")
                headers = [x.replace('"', '').strip() for x in dataRows[0].split(",")[2:]]
                headers = [x.replace(' Price', '').strip() for x in headers]
                rows = []
                for row in dataRows[1:-1]:
                        rows.append([x.replace('"', '').strip() for x in row.split(",")[2:]])
                assert rows == results["getDataResponseForStockrows"]
                assert headers == results["getDataResponseForStockheader"]
                soup=BeautifulSoup(result, 'lxml')
                nsestockdatasource.parseHtmlToCSV(soup,parameters["fileNameforcsv"])
                def check():
                        with open (parameters["fileNameforcsv"],'r') as f:
                                count=-1
                                for line in f:
                                        if count==-1:
                                                str=','.join(results["getDataResponseForStockheader"])
                                                str+='\n'
                                                assert str==line
                                        else:
                                                str=','.join(results["getDataResponseForStockrows"][count])
                                                str+='\n'
                                                assert str==line
                                        count+=1
                                os.remove(parameters["fileNameforcsv"])
                check()
                nsestockdatasource.parseNSEUrl(parameters["stock"],datetime.strftime(parameters["startDatefornse"], '%d-%m-%Y'),datetime.strftime(parameters["endDatefornse"], '%d-%m-%Y'),parameters["fileNameforcsv"])
                check()
                assert nsestockdatasource.downloadFile(parameters["stock"],parameters["fileNameforcsv"])==True
                if c!=3:
                        check()
                assert nsestockdatasource.downloadAndAdjustData(parameters["stock"],parameters["fileNameforcsv"])==True
                assert nsestockdatasource.getFileName(parameters["stock"])==results["getFileNamefornse"]
                #processGroupedInstrumentUpdates() has been checked through getBookDataByFeature
                inst=nsestockdatasource.getInstrumentUpdateFromRow(parameters["instrumentIdfornse"],parameters["rowdict"])
                assert isinstance(inst,StockInstrumentUpdate) == True
                for k, d in nsestockdatasource.getBookDataByFeature().items():
                        assert nsestockdatasource.getBookDataByFeature()[k].equals(data["DataFramesfornse"][k])
                if c!=3:
                        assert nsestockdatasource.getClosingTime()==results["getClosingTime"]
                for inst in parameters["instrumentIds"]:
                        nsestockdatasource.parseNSEUrl(parameters["stock"],"01-01-2017","31-12-2017","Folder1/QQ3Data/%s_2017-01-01to2017-01-01.csv"%(inst))
                if c!=2 or c!=3:
                        nsestockdatasource.parseNSEUrl(parameters["stock"],"01-01-2017","31-12-2017","Folder1/def.csv")
                        nsestockdatasource2=NSEStockDataSource(parameters["cachedFolderName"],parameters["dataSetId"],
                                                               parameters["instrumentIds"],"2017/01/01","2017/12/31")
                        nsestockdatasource2.adjustPriceForSplitAndDiv(parameters["stock"],"Folder1/def.csv")
                if c==2 or c==3:
                        nsestockdatasource2=NSEStockDataSource(parameters["cachedFolderName"],parameters["dataSetId"],
                                                               parameters["instrumentIds"],"2017/01/01","2017/12/31",True)
                        assert nsestockdatasource2.downloadAndAdjustData(parameters["stock"],"Folder1/def.csv")
                df=pd.read_csv("Folder1/def.csv").round(5)
                list=[df.iloc[-1].tolist(),df.iloc[-10].tolist(),df.iloc[-50].tolist(),df.iloc[-100].tolist(),df.iloc[-150].tolist(),df.iloc[-200].tolist(),df.iloc[-220].tolist()]
                assert list==results["adjustPriceForSplitAndDiv"]
                shutil.rmtree(parameters["cachedFolderName"])
