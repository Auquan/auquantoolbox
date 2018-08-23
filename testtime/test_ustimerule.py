from backtester.timeRule.us_time_rule import USTimeRule
from unittest.mock import Mock, MagicMock
import pytest
from initialize import Initialize
def test_ustimerule():
        initialize = Initialize()
        for i in range(0,4):
                dataSet = initialize.getDataSet(i)
                parameters=dataSet["parameters"]
                results=dataSet["results"]
                ustimerule=USTimeRule(parameters["startDateustimerule"],parameters["endDateustimerule"],
                                      parameters["startTimeustimerule"],parameters["endTimeustimerule"],
                                      parameters["frequency"],parameters["sample"])
                resultcreateBusinessDaySeries=USTimeRule.createBusinessDaySeries(ustimerule)
                assert resultcreateBusinessDaySeries.tolist() == results["createBusinessDaySeriesforustimerule"]
                if(i!=0):
                        resultcreateBusinessHourSeries=USTimeRule.createBusinessHourSeries(ustimerule)
                        assert resultcreateBusinessHourSeries.tolist() == results["createBusinessHourSeriesforustimerule"]
                if(i==2 or i==3):
                        resultcreateBusinessMinSeries=USTimeRule.createBusinessMinSeries(ustimerule)
                        assert resultcreateBusinessMinSeries.tolist() == results["createBusinessMinSeriesforustimerule"]
                if(i==3):
                        resultcreateBusinessSecSeries=USTimeRule.createBusinessSecSeries(ustimerule)
                        assert resultcreateBusinessSecSeries.tolist() == results["createBusinessSecSeriesforustimerule"]
                resultemitTimeToTrade=USTimeRule.emitTimeToTrade(ustimerule)
                if(i==0):
                        assert list(resultemitTimeToTrade) == results["createBusinessDaySeriesforustimerule"]
                if(i==1):
                        assert list(resultemitTimeToTrade) == results["createBusinessHourSeriesforustimerule"]
                if(i==2):
                        assert list(resultemitTimeToTrade) == results["createBusinessMinSeriesforustimerule"]
                if(i==3):
                        assert list(resultemitTimeToTrade) == results["createBusinessSecSeriesforustimerule"]
