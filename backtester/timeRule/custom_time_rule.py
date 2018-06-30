from backtester.timeRule.time_rule import TimeRule
from datetime import datetime, timedelta
import pandas as pd
from pandas.tseries.offsets import CustomBusinessHour
from pandas.tseries.offsets import CustomBusinessDay

class CustomTimeRule(TimeRule):
    def __init__(self, startDate, endDate, start_time='9:00', end_time='16:00', holidays = [], weekmask = 'Mon Tue Wed Thu Fri', calendar = None, frequency='H', sample='1'):
        self.__startDate = startDate
        self.__endDate = endDate
        self.__sample = sample

        acceptable_freq = ['D', 'M', 'H', 'S']
        if frequency not in acceptable_freq:
            raise ValueError('Frequency Value Not acceptable. Specify D, M, H, S')
        self.__frequency = frequency

        if(calendar != None):
            self.__bday = CustomBusinessDay(calendar = calendar)
            self.__bhour =  CustomBusinessHour(start = start_time, end = end_time, calendar = calendar)
        else:
            self.__bday = CustomBusinessDay(holidays = holidays, weekmask = weekmask)
            self.__bhour = CustomBusinessHour(start = start_time, end = end_time, holidays = holidays, weekmask = weekmask)

    def createBusinessDaySeries(self):
        return pd.date_range(start=self.__startDate, end=self.__endDate, freq= self.__bday)

    def createBusinessHourSeries(self):
        return pd.date_range(start=self.__startDate, end=self.__endDate, freq= self.__bhour)

    def createBusinessMinSeries(self):
        hour_series = self.createBusinessHourSeries()
        return pd.date_range(hour_series.min(), hour_series.max(), freq= self.__sample + ' min')

    def createBusinessSecSeries(self):
        hour_series = self.createBusinessHourSeries()
        return pd.date_range(hour_series.min(), hour_series.max(), freq= self.__sample + ' s')

    def emitTimeToTrade(self):
        time_range = None
        if(self.__frequency == 'D'):
            time_range = self.createBusinessDaySeries()
        elif(self.__frequency == 'H'):
            time_range = self.createBusinessHourSeries()
        elif(self.__frequency == 'M'):
            time_range = self.createBusinessMinSeries()
        elif(self.__frequency == 'S'):
            time_range = self.createBusinessSecSeries()

        for timestamp in time_range:
            yield timestamp
