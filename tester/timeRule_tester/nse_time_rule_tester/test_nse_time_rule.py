import os,sys,shutil,pytest
sys.path.append(os.path.abspath(''))
from backtester.timeRule.nse_time_rule import NSETimeRule
from data_nse_time_rule import *
def test_nse_time_rule():
    for i in range(0,4):
        data = data_nse_time_rule(i)
        parameters=data["parameters"]
        results=data["results"]
        nsetimerule=NSETimeRule(parameters["startDate"],parameters["endDate"],
                               parameters["startTime"],parameters["endTime"],
                               parameters["frequency"],parameters["sample"])
######## checking holiday list
        if i==0:
            assert NSETimeRule.getNSEHolidays(nsetimerule)==results["getNSEHolidays"]
######## checking just for days
        assert NSETimeRule.createBusinessDaySeries(nsetimerule).tolist() == results["createBusinessDaySeries"]
######## checking for hours
        if(i!=0):
            assert NSETimeRule.createBusinessHourSeries(nsetimerule).tolist() == results["createBusinessHourSeries"]
######## checking for minutes
        if(i==2 or i==3):
            assert NSETimeRule.createBusinessMinSeries(nsetimerule).tolist() == results["createBusinessMinSeries"]
######## checking for seconds
        if(i==3):
            assert NSETimeRule.createBusinessSecSeries(nsetimerule).tolist() == results["createBusinessSecSeries"]
        resultemitTimeToTrade=NSETimeRule.emitTimeToTrade(nsetimerule)
######## checking just for days
        if(i==0):
            assert list(resultemitTimeToTrade) == results["createBusinessDaySeries"]
######## checking for hours
        if(i==1):
            assert list(resultemitTimeToTrade) == results["createBusinessHourSeries"]
######## checking for minutes
        if(i==2):
            assert list(resultemitTimeToTrade) == results["createBusinessMinSeries"]
######## checking for seconds
        if(i==3):
            assert list(resultemitTimeToTrade) == results["createBusinessSecSeries"]
