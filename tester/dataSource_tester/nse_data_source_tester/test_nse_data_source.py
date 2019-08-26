import os,sys,shutil,pytest,pandas as pd
from datetime import datetime, time, timedelta
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath(''))
from backtester.dataSource.nse_data_source import *
from backtester.instrumentUpdates import *
from data_nse_data_source import *

def test_nse_data_source():
    for i in range(0,8):
        print(i)
        try:
            data = data_nse_data_source(i)
            dataSet=data["dataSet"]
            parameters=data["parameters"]
            results=data["results"]
            assert checkDate(parameters["lineItem"]) == results["checkDate"]
            assert checkTimestamp(parameters["lineItem"]) == True
            assert isFloat(parameters["isFloat"]) == results["isFloat"]
            assert is_number(parameters["isFloat"]) == results["isFloat"]
            assert validateLineItem(parameters["lineItems"],parameters["lineLength"]) == results["validateLineItem"]
            assert parseDataLine(parameters["lineItems"],parameters["lineLength"]) == results["parseDataLine"]
            instrumentsfromfile=InstrumentsFromFile(parameters["fileName"],parameters["instrumentId"])
            if i in range(1, 5):
                assert isinstance(instrumentsfromfile.processLine(parameters["line"],parameters["lineLength"]),StockInstrumentUpdate)
                assert instrumentsfromfile.processLine(parameters["line"],parameters["lineLength"]).getStockInstrumentId()==results["getStockInstrumentId"]
                assert instrumentsfromfile.processLine(parameters["line"],parameters["lineLength"]).getTypeOfInstrument()==results["getTypeOfInstrument"]
            else:
                assert instrumentsfromfile.processLine(parameters["line"],parameters["lineLength"])==results["processLine"]
            os.makedirs(os.path.dirname(parameters["fileName"]), exist_ok=True)
            with open(parameters["fileName"], 'w') as f:
                f.write(parameters["line"]+"\n"+parameters["line"]+"\n"+"ABC"+"\n"+parameters["line"]+"\n")
            if i in range(1, 5):
                count=0
                for ele in instrumentsfromfile.processLinesIntoInstruments(parameters["lineLength"]):
                    assert isinstance(ele,StockInstrumentUpdate)
                    assert ele.getStockInstrumentId()==results["getStockInstrumentId"]
                    assert ele.getTypeOfInstrument()==results["getTypeOfInstrument"]
                    count+=1
                assert count==3
            else:
                assert instrumentsfromfile.processLinesIntoInstruments(parameters["lineLength"])==[]
            for inst in parameters["instrumentIds"]:
                filepath="%s%s/%s_%sto%s.csv"%(parameters["folderName"],parameters["dataSetId"],inst,parameters["date"],parameters["date"])
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, 'w') as f:
                    f.write(dataSet["fileData"])
            nsestockdatasource=NSEStockDataSource(parameters["folderName"],parameters["dataSetId"],
                                                  parameters["instrumentIds"],parameters["startDateStr"],
                                                  parameters["endDateStr"],parameters["adjustPrice"],
                                                  parameters["downloadId"],parameters["liveUpdates"],
                                                  parameters["pad"])
            url="https://nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol=%s" % (parameters["stock"])
            if i==7:
                assert nsestockdatasource.getResponseFromUrl("https://nseindia.com/marketinfo/sym_map/symbolCounted.jsp?symbol=",False)==results["getResponseFromUrl"]
            else:
                assert nsestockdatasource.getResponseFromUrl(url,False).strip() == results["getResponseFromUrl"]
            assert nsestockdatasource.getInitialSymbolCountUrl(parameters["stock"]) == results["getInitialSymbolCountUrl"]
            if i!=7:
                assert nsestockdatasource.getSymbolCountForStock(parameters["stock"]) == results["getResponseFromUrl"]
                assert nsestockdatasource.getDataUrl(parameters["stock"],results["getResponseFromUrl"],parameters["start"],parameters["end"]) == results["getDataUrl"]
                result= (nsestockdatasource.getDataResponseForStock(parameters["stock"],results["getResponseFromUrl"],parameters["start"],parameters["end"]))
                if i!=5:
                    dataRows = BeautifulSoup(result, 'lxml').find(id="csvContentDiv").get_text().split(":")
                    headers = [x.replace('"', '').strip() for x in dataRows[0].split(",")[2:]]
                    headers = [x.replace(' Price', '').strip() for x in headers]
                    rows = []
                    for row in dataRows[1:-1]:
                        rows.append([x.replace('"', '').strip() for x in row.split(",")[2:]])
                    assert rows == results["rows"]
                    assert headers == results["headers"]
                    def check():
                        with open (parameters["csvfileName"],'r') as f:
                            list=[]
                            for line in f:
                                list.append(line)
                            assert list==results["check"]
                        os.remove(parameters["csvfileName"])
                    if i==2:
                        result="abcdef"
                    if i==6:
                        result=""
                    soup=BeautifulSoup(result, 'lxml')
                    nsestockdatasource.parseHtmlToCSV(soup,parameters["csvfileName"])
                    if i==2 or i==6:
                        pass
                    else:
                        check()
                    nsestockdatasource.parseNSEUrl(parameters["stock"],parameters["start"],parameters["end"],parameters["csvfileName"])
                    check()
                    assert nsestockdatasource.downloadFile(parameters["stock"],parameters["csvfileName"])==True
                    if i==2 or i==6:
                        pass
                    else:
                        check()
                assert nsestockdatasource.downloadAndAdjustData(parameters["stock"],parameters["csvfileName"])==True
                assert nsestockdatasource.getFileName(parameters["stock"])==results["getFileName"]
                assert nsestockdatasource.getFileName1("QQ3Data",parameters["stock"])==results["getFileName"]
                #processGroupedInstrumentUpdates() has been checked through getBookDataByFeature
                inst=nsestockdatasource.getInstrumentUpdateFromRow(parameters["instrumentId"],parameters["rowdict"])
                assert isinstance(inst,StockInstrumentUpdate) == True
                assert inst.getStockInstrumentId()==parameters["instrumentId"]
                assert inst.getTypeOfInstrument()=="stock"
                for k, d in nsestockdatasource.getBookDataByFeature().items():
                    assert nsestockdatasource.getBookDataByFeature()[k].equals(dataSet["DataFrames"][k])
                if i==0 or i==1:
                    assert nsestockdatasource.getClosingTime()==results["getClosingTime"]
                    nsestockdatasource.parseNSEUrl(parameters["stock"],"01-01-2017","31-12-2017","Folder1/def.csv")
                    nsestockdatasource.adjustPriceForSplitAndDiv(parameters["stock"],"Folder1/def.csv")
                    df=pd.read_csv("Folder1/def.csv").round(5)
                    assert df.shape==(248,13)
                    #selecting a few specific dates from the datatframe for one year
                    #assuming the fact that if those days are correct then the whole dataframe is correct
                    #christmas and weekends are covered to check the dates
                    list=[df.iloc[-1].tolist(),
                          df.iloc[-4].tolist(),
                          df.iloc[-5].tolist(),
                          df.iloc[-6].tolist(),
                          df.iloc[-10].tolist(),
                          df.iloc[-50].tolist(),
                          df.iloc[-100].tolist(),
                          df.iloc[-150].tolist(),
                          df.iloc[-200].tolist(),
                          df.iloc[-220].tolist(),
                          df.iloc[-248].tolist()]
                    assert list==results["adjustPriceForSplitAndDiv"]
                if i==2 or i==3:
                    os.makedirs(os.path.dirname(parameters["divfileName"]), exist_ok=True)
                    os.makedirs(os.path.dirname(parameters["splitfileName"]), exist_ok=True)
                    with open(parameters["divfileName"], 'w') as f:
                        f.write(dataSet["divData"])
                    with open(parameters["splitfileName"], 'w') as f:
                        f.write(dataSet["splitData"])
                    with open("Folder1/def.csv", 'w') as f:
                        f.write(dataSet["fileData"])
                    nsestockdatasource.adjustPriceForSplitAndDiv("GOOG","Folder1/def.csv")
                    df=pd.read_csv("Folder1/def.csv").round(5)
                    #making a list of the DataFrame to test the DataFrame
                    list=[]
                    for col in df:
                        list.append(df[col].tolist())
                    # assert list==results["adjustPriceForSplitAndDiv"]
            shutil.rmtree(parameters["folderName"])
        #Using sys.exit() because have to delete the Folder1/ for every loop run
        except Exception as e:
            shutil.rmtree(parameters["folderName"])
            sys.exit(e)
