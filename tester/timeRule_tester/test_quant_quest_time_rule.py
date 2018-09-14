import os,sys,shutil
sys.path.append(os.path.abspath('../..'))
from backtester.timeRule.quant_quest_time_rule import QuantQuestTimeRule
from unittest.mock import Mock, MagicMock
import pandas as pd
import pytest
from initializetime import Initialize
from datetime import datetime, timedelta
import os
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


def test_quant_quest_time_rule():
        initialize = Initialize()
        for i in range(0,2):
                dataSet = initialize.getDataSet(i)
                parameters=dataSet["parameters"]
                results=dataSet["results"]
                quantquesttimerule=QuantQuestTimeRule(parameters["cachedFolderName"],
                                                      parameters["dataSetId"])
                QuantQuestTimeRule.ensureDirectoryExists(quantquesttimerule,parameters["testcachedFolderName"],parameters["testdataSetId"])
                assert os.path.exists(parameters["testcachedFolderName"])
                assert os.path.exists(parameters["testcachedFolderName"] + '/' + parameters["testdataSetId"])
                os.rmdir(parameters["testcachedFolderName"]+'/'+parameters["testdataSetId"])
                os.rmdir(parameters["testcachedFolderName"])
                resultgetFileName=QuantQuestTimeRule.getFileName(quantquesttimerule)
                assert resultgetFileName == results["getFileName"]
                resultdownloadFile=QuantQuestTimeRule.downloadFile(quantquesttimerule,parameters["dataSetId"],parameters["downloadLocation"])
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
                os.rmdir(parameters["cachedFolderName"]+'/'+parameters["dataSetId"])
                os.rmdir(parameters["cachedFolderName"])
                """resultemitTimeToTrade=QuantQuestTimeRule.emitTimeToTrade(quantquesttimerule)
                #print (list(resultemitTimeToTrade))
                if resultdownloadFile:
                        os.remove(resultgetFileName)
                os.rmdir(parameters["cachedFolderName"]+'/'+parameters["dataSetId"])
                os.rmdir(parameters["cachedFolderName"])"""
