import pandas as pd
from pandas.tseries.holiday import Holiday, AbstractHolidayCalendar
def data_custom_time_rule(c):
    parameters={}
    results={}
    if c==0:
######## checking days for one whole days
        parameters["startDate"]='1/1/2018'
        parameters["endDate"]='2/1/2018'
        parameters["startTime"]='9:00'
        parameters["endTime"]='16:00'
        parameters["holidays"]=['2018-01-03','2018-01-04','2018-01-12', '2018-01-16','2018-01-18','2018-01-22','2018-01-26']
        parameters["weekmask"]='Mon Tue Wed Thu Fri'
        class MyCalendar(AbstractHolidayCalendar):
            rules = [Holiday('holiday1', month=1, day=3),Holiday('holiday2', month=1, day=4),
                     Holiday('holiday1', month=1, day=12),Holiday('holiday2', month=1, day=16),
                     Holiday('holiday1', month=1, day=18),Holiday('holiday2', month=1, day=22),
                     Holiday('holiday1', month=1, day=26)]
        parameters["calendar"]=MyCalendar()
        parameters["frequency"]='D'
        parameters["sample"]='1'
        results["createBusinessDaySeries"]=[pd.Timestamp(' 2018-01-01 00:00:00 '),
                                            pd.Timestamp(' 2018-01-02 00:00:00 '),
                                            pd.Timestamp(' 2018-01-05 00:00:00 '),
                                            pd.Timestamp(' 2018-01-08 00:00:00 '),
                                            pd.Timestamp(' 2018-01-09 00:00:00 '),
                                            pd.Timestamp(' 2018-01-10 00:00:00 '),
                                            pd.Timestamp(' 2018-01-11 00:00:00 '),
                                            pd.Timestamp(' 2018-01-15 00:00:00 '),
                                            pd.Timestamp(' 2018-01-17 00:00:00 '),
                                            pd.Timestamp(' 2018-01-19 00:00:00 '),
                                            pd.Timestamp(' 2018-01-23 00:00:00 '),
                                            pd.Timestamp(' 2018-01-24 00:00:00 '),
                                            pd.Timestamp(' 2018-01-25 00:00:00 '),
                                            pd.Timestamp(' 2018-01-29 00:00:00 '),
                                            pd.Timestamp(' 2018-01-30 00:00:00 '),
                                            pd.Timestamp(' 2018-01-31 00:00:00 '),
                                            pd.Timestamp(' 2018-02-01 00:00:00 ')]

    if c==1:
        parameters["startDate"]='1/1/2018'
        parameters["endDate"]='1/10/2018'
######## checking hours for one day
        parameters["startTime"]='9:00'
        parameters["endTime"]='16:00'
        parameters["holidays"]=['2018-01-03','2018-01-04']
        parameters["weekmask"]='Mon Tue Wed Thu Fri'
        class MyCalendar(AbstractHolidayCalendar):
            rules = [Holiday('holiday1', month=1, day=3),Holiday('holiday2', month=1, day=4)]
        parameters["calendar"]=MyCalendar()
        parameters["frequency"]='H'
        parameters["sample"]='1'
        results["createBusinessDaySeries"]=[pd.Timestamp(' 2018-01-01 00:00:00 '),
                                            pd.Timestamp(' 2018-01-02 00:00:00 '),
                                            pd.Timestamp(' 2018-01-05 00:00:00 '),
                                            pd.Timestamp(' 2018-01-08 00:00:00 '),
                                            pd.Timestamp(' 2018-01-09 00:00:00 '),
                                            pd.Timestamp(' 2018-01-10 00:00:00 ')]
        results["createBusinessHourSeries"]=[pd.Timestamp(' 2018-01-01 09:00:00 '),
                                            pd.Timestamp(' 2018-01-01 10:00:00 '),
                                            pd.Timestamp(' 2018-01-01 11:00:00 '),
                                            pd.Timestamp(' 2018-01-01 12:00:00 '),
                                            pd.Timestamp(' 2018-01-01 13:00:00 '),
                                            pd.Timestamp(' 2018-01-01 14:00:00 '),
                                            pd.Timestamp(' 2018-01-01 15:00:00 '),
                                            pd.Timestamp(' 2018-01-02 09:00:00 '),
                                            pd.Timestamp(' 2018-01-02 10:00:00 '),
                                            pd.Timestamp(' 2018-01-02 11:00:00 '),
                                            pd.Timestamp(' 2018-01-02 12:00:00 '),
                                            pd.Timestamp(' 2018-01-02 13:00:00 '),
                                            pd.Timestamp(' 2018-01-02 14:00:00 '),
                                            pd.Timestamp(' 2018-01-02 15:00:00 '),
                                            pd.Timestamp(' 2018-01-05 09:00:00 '),
                                            pd.Timestamp(' 2018-01-05 10:00:00 '),
                                            pd.Timestamp(' 2018-01-05 11:00:00 '),
                                            pd.Timestamp(' 2018-01-05 12:00:00 '),
                                            pd.Timestamp(' 2018-01-05 13:00:00 '),
                                            pd.Timestamp(' 2018-01-05 14:00:00 '),
                                            pd.Timestamp(' 2018-01-05 15:00:00 '),
                                            pd.Timestamp(' 2018-01-08 09:00:00 '),
                                            pd.Timestamp(' 2018-01-08 10:00:00 '),
                                            pd.Timestamp(' 2018-01-08 11:00:00 '),
                                            pd.Timestamp(' 2018-01-08 12:00:00 '),
                                            pd.Timestamp(' 2018-01-08 13:00:00 '),
                                            pd.Timestamp(' 2018-01-08 14:00:00 '),
                                            pd.Timestamp(' 2018-01-08 15:00:00 '),
                                            pd.Timestamp(' 2018-01-09 09:00:00 '),
                                            pd.Timestamp(' 2018-01-09 10:00:00 '),
                                            pd.Timestamp(' 2018-01-09 11:00:00 '),
                                            pd.Timestamp(' 2018-01-09 12:00:00 '),
                                            pd.Timestamp(' 2018-01-09 13:00:00 '),
                                            pd.Timestamp(' 2018-01-09 14:00:00 '),
                                            pd.Timestamp(' 2018-01-09 15:00:00 ')]

    if c==2:
        parameters["startDate"]='1/1/2018'
        parameters["endDate"]='1/1/2018'
######## checking minutes for 30 minutes
        parameters["startTime"]='9:00'
        parameters["endTime"]='9:30'
        parameters["holidays"]=[]
        parameters["weekmask"]='Mon Tue Wed Thu Fri'
        class MyCalendar(AbstractHolidayCalendar):
            rules = []
        parameters["calendar"]=MyCalendar()
        parameters["frequency"]='M'
        parameters["sample"]='1'
        results["createBusinessDaySeries"]=[pd.Timestamp(' 2018-01-01 00:00:00 ')]
        results["createBusinessHourSeries"]=[]
        results["createBusinessMinSeries"]=[pd.Timestamp(' 2018-01-01 09:00:00 '),
                                            pd.Timestamp(' 2018-01-01 09:01:00 '),
                                            pd.Timestamp(' 2018-01-01 09:02:00 '),
                                            pd.Timestamp(' 2018-01-01 09:03:00 '),
                                            pd.Timestamp(' 2018-01-01 09:04:00 '),
                                            pd.Timestamp(' 2018-01-01 09:05:00 '),
                                            pd.Timestamp(' 2018-01-01 09:06:00 '),
                                            pd.Timestamp(' 2018-01-01 09:07:00 '),
                                            pd.Timestamp(' 2018-01-01 09:08:00 '),
                                            pd.Timestamp(' 2018-01-01 09:09:00 '),
                                            pd.Timestamp(' 2018-01-01 09:10:00 '),
                                            pd.Timestamp(' 2018-01-01 09:11:00 '),
                                            pd.Timestamp(' 2018-01-01 09:12:00 '),
                                            pd.Timestamp(' 2018-01-01 09:13:00 '),
                                            pd.Timestamp(' 2018-01-01 09:14:00 '),
                                            pd.Timestamp(' 2018-01-01 09:15:00 '),
                                            pd.Timestamp(' 2018-01-01 09:16:00 '),
                                            pd.Timestamp(' 2018-01-01 09:17:00 '),
                                            pd.Timestamp(' 2018-01-01 09:18:00 '),
                                            pd.Timestamp(' 2018-01-01 09:19:00 '),
                                            pd.Timestamp(' 2018-01-01 09:20:00 '),
                                            pd.Timestamp(' 2018-01-01 09:21:00 '),
                                            pd.Timestamp(' 2018-01-01 09:22:00 '),
                                            pd.Timestamp(' 2018-01-01 09:23:00 '),
                                            pd.Timestamp(' 2018-01-01 09:24:00 '),
                                            pd.Timestamp(' 2018-01-01 09:25:00 '),
                                            pd.Timestamp(' 2018-01-01 09:26:00 '),
                                            pd.Timestamp(' 2018-01-01 09:27:00 '),
                                            pd.Timestamp(' 2018-01-01 09:28:00 '),
                                            pd.Timestamp(' 2018-01-01 09:29:00 '),
                                            pd.Timestamp(' 2018-01-01 09:30:00 ')]

    if c==3:
        parameters["startDate"]='1/1/2018'
        parameters["endDate"]='1/1/2018'
######## checking seconds for one minute
        parameters["startTime"]='9:00'
        parameters["endTime"]='9:01'
        parameters["holidays"]=[]
        parameters["weekmask"]='Mon Tue Wed Thu Fri'
        class MyCalendar(AbstractHolidayCalendar):
            rules = []
        parameters["calendar"]=MyCalendar()
        parameters["frequency"]='S'
        parameters["sample"]='1'
        results["createBusinessDaySeries"]=[pd.Timestamp(' 2018-01-01 00:00:00 ')]
        results["createBusinessHourSeries"]=[]
        results["createBusinessMinSeries"]=[pd.Timestamp(' 2018-01-01 09:00:00 '),
                                            pd.Timestamp(' 2018-01-01 09:01:00 ')]
        results["createBusinessSecSeries"]=[pd.Timestamp(' 2018-01-01 09:00:00 '),
                                            pd.Timestamp(' 2018-01-01 09:00:01 '),
                                            pd.Timestamp(' 2018-01-01 09:00:02 '),
                                            pd.Timestamp(' 2018-01-01 09:00:03 '),
                                            pd.Timestamp(' 2018-01-01 09:00:04 '),
                                            pd.Timestamp(' 2018-01-01 09:00:05 '),
                                            pd.Timestamp(' 2018-01-01 09:00:06 '),
                                            pd.Timestamp(' 2018-01-01 09:00:07 '),
                                            pd.Timestamp(' 2018-01-01 09:00:08 '),
                                            pd.Timestamp(' 2018-01-01 09:00:09 '),
                                            pd.Timestamp(' 2018-01-01 09:00:10 '),
                                            pd.Timestamp(' 2018-01-01 09:00:11 '),
                                            pd.Timestamp(' 2018-01-01 09:00:12 '),
                                            pd.Timestamp(' 2018-01-01 09:00:13 '),
                                            pd.Timestamp(' 2018-01-01 09:00:14 '),
                                            pd.Timestamp(' 2018-01-01 09:00:15 '),
                                            pd.Timestamp(' 2018-01-01 09:00:16 '),
                                            pd.Timestamp(' 2018-01-01 09:00:17 '),
                                            pd.Timestamp(' 2018-01-01 09:00:18 '),
                                            pd.Timestamp(' 2018-01-01 09:00:19 '),
                                            pd.Timestamp(' 2018-01-01 09:00:20 '),
                                            pd.Timestamp(' 2018-01-01 09:00:21 '),
                                            pd.Timestamp(' 2018-01-01 09:00:22 '),
                                            pd.Timestamp(' 2018-01-01 09:00:23 '),
                                            pd.Timestamp(' 2018-01-01 09:00:24 '),
                                            pd.Timestamp(' 2018-01-01 09:00:25 '),
                                            pd.Timestamp(' 2018-01-01 09:00:26 '),
                                            pd.Timestamp(' 2018-01-01 09:00:27 '),
                                            pd.Timestamp(' 2018-01-01 09:00:28 '),
                                            pd.Timestamp(' 2018-01-01 09:00:29 '),
                                            pd.Timestamp(' 2018-01-01 09:00:30 '),
                                            pd.Timestamp(' 2018-01-01 09:00:31 '),
                                            pd.Timestamp(' 2018-01-01 09:00:32 '),
                                            pd.Timestamp(' 2018-01-01 09:00:33 '),
                                            pd.Timestamp(' 2018-01-01 09:00:34 '),
                                            pd.Timestamp(' 2018-01-01 09:00:35 '),
                                            pd.Timestamp(' 2018-01-01 09:00:36 '),
                                            pd.Timestamp(' 2018-01-01 09:00:37 '),
                                            pd.Timestamp(' 2018-01-01 09:00:38 '),
                                            pd.Timestamp(' 2018-01-01 09:00:39 '),
                                            pd.Timestamp(' 2018-01-01 09:00:40 '),
                                            pd.Timestamp(' 2018-01-01 09:00:41 '),
                                            pd.Timestamp(' 2018-01-01 09:00:42 '),
                                            pd.Timestamp(' 2018-01-01 09:00:43 '),
                                            pd.Timestamp(' 2018-01-01 09:00:44 '),
                                            pd.Timestamp(' 2018-01-01 09:00:45 '),
                                            pd.Timestamp(' 2018-01-01 09:00:46 '),
                                            pd.Timestamp(' 2018-01-01 09:00:47 '),
                                            pd.Timestamp(' 2018-01-01 09:00:48 '),
                                            pd.Timestamp(' 2018-01-01 09:00:49 '),
                                            pd.Timestamp(' 2018-01-01 09:00:50 '),
                                            pd.Timestamp(' 2018-01-01 09:00:51 '),
                                            pd.Timestamp(' 2018-01-01 09:00:52 '),
                                            pd.Timestamp(' 2018-01-01 09:00:53 '),
                                            pd.Timestamp(' 2018-01-01 09:00:54 '),
                                            pd.Timestamp(' 2018-01-01 09:00:55 '),
                                            pd.Timestamp(' 2018-01-01 09:00:56 '),
                                            pd.Timestamp(' 2018-01-01 09:00:57 '),
                                            pd.Timestamp(' 2018-01-01 09:00:58 '),
                                            pd.Timestamp(' 2018-01-01 09:00:59 '),
                                            pd.Timestamp(' 2018-01-01 09:01:00 ')]
    if c==4:
        parameters["startDate"]='1/1/2018'
        parameters["endDate"]='1/1/2018'
        parameters["startTime"]='9:00'
        parameters["endTime"]='9:01'
        parameters["holidays"]=[]
        parameters["weekmask"]='Mon Tue Wed Thu Fri'
        parameters["calendar"]=None
        parameters["frequency"]='S'
######## 'sample = 7 will give times with a difference of 7 seconds'
        parameters["sample"]='7'
        results["createBusinessDaySeries"]=[pd.Timestamp(' 2018-01-01 00:00:00 ')]
        results["createBusinessHourSeries"]=[]
        results["createBusinessMinSeries"]=[pd.Timestamp('2018-01-01 09:00:00', freq='7T')]
        results["createBusinessSecSeries"]=[pd.Timestamp('2018-01-01 09:00:00', freq='7S'),
                                            pd.Timestamp('2018-01-01 09:00:07', freq='7S'),
                                            pd.Timestamp('2018-01-01 09:00:14', freq='7S'),
                                            pd.Timestamp('2018-01-01 09:00:21', freq='7S'),
                                            pd.Timestamp('2018-01-01 09:00:28', freq='7S'),
                                            pd.Timestamp('2018-01-01 09:00:35', freq='7S'),
                                            pd.Timestamp('2018-01-01 09:00:42', freq='7S'),
                                            pd.Timestamp('2018-01-01 09:00:49', freq='7S'),
                                            pd.Timestamp('2018-01-01 09:00:56', freq='7S')]
    if c==5:
        parameters["startDate"]='1/1/2018'
        parameters["endDate"]='1/1/2018'
        parameters["startTime"]='9:00'
        parameters["endTime"]='9:01'
        parameters["holidays"]=[]
        parameters["weekmask"]='Mon Tue Wed Thu Fri'
        parameters["calendar"]=None
######## 'C' will give a value error
        parameters["frequency"]='C'
        parameters["sample"]='1'

    return {"results":results, "parameters":parameters}
