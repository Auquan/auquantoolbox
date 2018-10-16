import os,sys,shutil,pytest
sys.path.append(os.path.abspath(''))
from backtester.timeRule.custom_time_rule import CustomTimeRule
from data_custom_time_rule import *
def test_custom_time_rule():
    for i in range(0,6):
        data = data_custom_time_rule(i)
        parameters=data["parameters"]
        results=data["results"]
        if (i!=5):
            customtimerule=CustomTimeRule(parameters["startDate"],parameters["endDate"],
                                          parameters["startTime"],parameters["endTime"],
                                          parameters["holidays"],parameters["weekmask"],
                                          parameters["calendar"],parameters["frequency"],
                                          parameters["sample"])
############ checking just for days
            resultcreateBusinessDaySeries=CustomTimeRule.createBusinessDaySeries(customtimerule)
            assert resultcreateBusinessDaySeries.tolist() == results["createBusinessDaySeries"]
############ checking for hours
            if(i!=0):
                resultcreateBusinessHourSeries=CustomTimeRule.createBusinessHourSeries(customtimerule)
                assert resultcreateBusinessHourSeries.tolist() == results["createBusinessHourSeries"]
############ checking for minutes
            if(i==2 or i==3 or i==4):
                resultcreateBusinessMinSeries=CustomTimeRule.createBusinessMinSeries(customtimerule)
                assert resultcreateBusinessMinSeries.tolist() == results["createBusinessMinSeries"]
############ checking for seconds
            if(i==3 or i==4):
                resultcreateBusinessSecSeries=CustomTimeRule.createBusinessSecSeries(customtimerule)
                assert resultcreateBusinessSecSeries.tolist() == results["createBusinessSecSeries"]
            resultemitTimeToTrade=CustomTimeRule.emitTimeToTrade(customtimerule)
############ checking for days
            if(i==0):
                assert list(resultemitTimeToTrade) == results["createBusinessDaySeries"]
############ checking for hours
            if(i==1):
                assert list(resultemitTimeToTrade) == results["createBusinessHourSeries"]
############ checking for minutes
            if(i==2):
                assert list(resultemitTimeToTrade) == results["createBusinessMinSeries"]
############ checking for seconds
            if(i==3 or i==4):
                assert list(resultemitTimeToTrade) == results["createBusinessSecSeries"]
######## for frequency='C', gives ValueError
        if (i==5):
            with pytest.raises(ValueError):
                customtimerule=CustomTimeRule(parameters["startDate"],parameters["endDate"],
                                              parameters["startTime"],parameters["endTime"],
                                              parameters["holidays"],parameters["weekmask"],
                                              parameters["calendar"],parameters["frequency"],
                                              parameters["sample"])
