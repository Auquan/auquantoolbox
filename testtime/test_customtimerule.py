from backtester.timeRule.custom_time_rule import CustomTimeRule
from unittest.mock import Mock, MagicMock
import pytest
from initialize import Initialize
def test_customtimerule():
        initialize = Initialize()
        for i in range(0,4):
                dataSet = initialize.getDataSet(i)
                parameters=dataSet["parameters"]
                results=dataSet["results"]
                customtimerule=CustomTimeRule(parameters["startDate"],parameters["endDate"],
                                              parameters["startTime"],parameters["endTime"],
                                              parameters["holidays"],parameters["weekmask"],
                                              parameters["calendar"],parameters["frequency"],parameters["sample"])
                resultcreateBusinessDaySeries=CustomTimeRule.createBusinessDaySeries(customtimerule)
                assert resultcreateBusinessDaySeries.tolist() == results["createBusinessDaySeries"]
                if(i!=0):
                        resultcreateBusinessHourSeries=CustomTimeRule.createBusinessHourSeries(customtimerule)
                        assert resultcreateBusinessHourSeries.tolist() == results["createBusinessHourSeries"]
                if(i==2 or i==3):
                        resultcreateBusinessMinSeries=CustomTimeRule.createBusinessMinSeries(customtimerule)
                        assert resultcreateBusinessMinSeries.tolist() == results["createBusinessMinSeries"]
                if(i==3):
                        resultcreateBusinessSecSeries=CustomTimeRule.createBusinessSecSeries(customtimerule)
                        assert resultcreateBusinessSecSeries.tolist() == results["createBusinessSecSeries"]
                resultemitTimeToTrade=CustomTimeRule.emitTimeToTrade(customtimerule)
                if(i==0):
                        assert list(resultemitTimeToTrade) == results["createBusinessDaySeries"]
                if(i==1):
                        assert list(resultemitTimeToTrade) == results["createBusinessHourSeries"]
                if(i==2):
                        assert list(resultemitTimeToTrade) == results["createBusinessMinSeries"]
                if(i==3):
                        assert list(resultemitTimeToTrade) == results["createBusinessSecSeries"]
