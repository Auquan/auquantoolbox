import os,sys,shutil,pytest
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath(''))
from backtester.timeRule.us_time_rule import USTimeRule
from data_us_time_rule import *
def test_us_time_rule():
    for i in range(0,5):
        data = data_us_time_rule(i)
        parameters=data["parameters"]
        results=data["results"]
        ustimerule=USTimeRule(parameters["startDate"],parameters["endDate"],
                              parameters["startTime"],parameters["endTime"],
                              parameters["frequency"],parameters["sample"])
######## checking for dates
        assert USTimeRule.createBusinessDaySeries(ustimerule).tolist() == results["createBusinessDaySeries"]
######## checking for hours
        if(i!=0):
            assert USTimeRule.createBusinessHourSeries(ustimerule).tolist() == results["createBusinessHourSeries"]
######## checking for minutes
        if(i==2 or i==3):
            assert USTimeRule.createBusinessMinSeries(ustimerule).tolist() == results["createBusinessMinSeries"]
######## checking for seconds
        if(i==3):
            assert USTimeRule.createBusinessSecSeries(ustimerule).tolist() == results["createBusinessSecSeries"]
######## checking for a holiday
        if(i==4):
            assert USTimeRule.createBusinessMinSeries(ustimerule) == results["createBusinessMinSeries"]
            assert USTimeRule.createBusinessSecSeries(ustimerule) == results["createBusinessSecSeries"]
        resultemitTimeToTrade=USTimeRule.emitTimeToTrade(ustimerule)
######## checking for dates
        if(i==0):
            assert list(resultemitTimeToTrade) == results["createBusinessDaySeries"]
######## checking for hours
        if(i==1):
            assert list(resultemitTimeToTrade) == results["createBusinessHourSeries"]
######## checking for minites
        if(i==2):
            assert list(resultemitTimeToTrade) == results["createBusinessMinSeries"]
######## checking for seconds
        if(i==3):
            assert list(resultemitTimeToTrade) == results["createBusinessSecSeries"]
