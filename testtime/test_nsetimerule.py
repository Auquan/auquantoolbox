import os,sys,shutil
sys.path.append(os.path.abspath('..'))
from backtester.timeRule.nse_time_rule import NSETimeRule
from unittest.mock import Mock, MagicMock
import pytest
from initializetime import Initialize
def test_nsetimerule():
        initialize = Initialize()
        for i in range(0,4):
                dataSet = initialize.getDataSet(i)
                parameters=dataSet["parameters"]
                results=dataSet["results"]
                nsetimerule=NSETimeRule(parameters["startDatensetimerule"],parameters["endDatensetimerule"],
                                       parameters["startTimensetimerule"],parameters["endTimensetimerule"],
                                       parameters["frequency"],parameters["sample"])
                resultgetNSEHolidays=NSETimeRule.getNSEHolidays(nsetimerule)
                resultcreateBusinessDaySeries=NSETimeRule.createBusinessDaySeries(nsetimerule)
                assert resultcreateBusinessDaySeries.tolist() == results["createBusinessDaySeriesfornsetimerule"]
                if(i!=0):
                        resultcreateBusinessHourSeries=NSETimeRule.createBusinessHourSeries(nsetimerule)
                        assert resultcreateBusinessHourSeries.tolist() == results["createBusinessHourSeriesfornsetimerule"]
                if(i==2 or i==3):
                        resultcreateBusinessMinSeries=NSETimeRule.createBusinessMinSeries(nsetimerule)
                        assert resultcreateBusinessMinSeries.tolist() == results["createBusinessMinSeriesfornsetimerule"]
                if(i==3):
                        resultcreateBusinessSecSeries=NSETimeRule.createBusinessSecSeries(nsetimerule)
                        assert resultcreateBusinessSecSeries.tolist() == results["createBusinessSecSeriesfornsetimerule"]
                resultemitTimeToTrade=NSETimeRule.emitTimeToTrade(nsetimerule)
                if(i==0):
                        assert list(resultemitTimeToTrade) == results["createBusinessDaySeriesfornsetimerule"]
                if(i==1):
                        assert list(resultemitTimeToTrade) == results["createBusinessHourSeriesfornsetimerule"]
                if(i==2):
                        assert list(resultemitTimeToTrade) == results["createBusinessMinSeriesfornsetimerule"]
                if(i==3):
                        assert list(resultemitTimeToTrade) == results["createBusinessSecSeriesfornsetimerule"]
