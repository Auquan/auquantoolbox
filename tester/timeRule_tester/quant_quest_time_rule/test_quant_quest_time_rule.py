import os,sys,shutil,pytest
sys.path.append(os.path.abspath(''))
from backtester.timeRule.quant_quest_time_rule import QuantQuestTimeRule
from data_quant_quest_time_rule import *
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
def test_quant_quest_time_rule():
    for i in range(0,2):
        data = data_quant_quest_time_rule(i)
        parameters=data["parameters"]
        results=data["results"]
        quantquesttimerule=QuantQuestTimeRule(parameters["cachedFolderName"],
                                              parameters["dataSetId"])
######## ensureDirectoryExists
        QuantQuestTimeRule.ensureDirectoryExists(quantquesttimerule,parameters["testcachedFolderName"],parameters["testdataSetId"])
        assert os.path.exists(parameters["testcachedFolderName"])
        assert os.path.exists(parameters["testcachedFolderName"] + '/' + parameters["testdataSetId"])
        os.rmdir(parameters["testcachedFolderName"]+'/'+parameters["testdataSetId"])
        os.rmdir(parameters["testcachedFolderName"])
######## getFileName
        assert QuantQuestTimeRule.getFileName(quantquesttimerule) == results["getFileName"]
######## downloadFile
        resultdownloadFile=QuantQuestTimeRule.downloadFile(quantquesttimerule,parameters["dataSetIdfordownloadFile"],parameters["downloadLocation"])
        assert resultdownloadFile == results["downloadFile"]
        if resultdownloadFile:
            assert os.path.isfile(parameters["downloadLocation"])
            contents = ""
            with open(parameters["downloadLocation"]) as f:
                for line in f.readlines():
                    contents += line
            link = 'https://raw.githubusercontent.com/Auquan/auquan-historical-data/master/qq2Data/%s/date_list.txt' % parameters["dataSetId"]
            f = urlopen(link)
            myfile = f.read().decode('utf8')
            assert contents == myfile
            os.remove(parameters["downloadLocation"])
######## emitTimeToTrade
######## checking for sample data
        if i==0:
            f = open(results["getFileName"],"w")
            f.write("2017-09-15\n")
            resultemitTimeToTrade=QuantQuestTimeRule.emitTimeToTrade(quantquesttimerule)
            f = open(results["getFileName"],"a+")
            f.write("2017-09-16\n")
            timelist=list(resultemitTimeToTrade)
############ checking for random dates in the list assuming if those dates are right then the list is right
            resulttimelist=[timelist[0],timelist[10],timelist[50],timelist[100],timelist[200],timelist[250],timelist[300],timelist[350],timelist[372]]
            assert resulttimelist==results["emitTimeToTrade"]
######## checking for wrong url
        if i==1:
            quantquesttimerule=QuantQuestTimeRule(parameters["cachedFolderName"],
                                                  parameters["dataSetIdfordownloadFile"])
            assert (list(quantquesttimerule.emitTimeToTrade())) == results["emitTimeToTrade"]
        shutil.rmtree(parameters["cachedFolderName"])
