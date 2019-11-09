from backtester.timeRule.time_rule import TimeRule
from datetime import datetime, timedelta
import pandas as pd
from pandas.tseries.offsets import CustomBusinessHour
from pandas.tseries.offsets import CustomBusinessDay

class CustomTimeRule(TimeRule):
    def __init__(self, startDate, endDate, startTime='9:00', endTime='16:00', holidays = [], weekmask = 'Mon Tue Wed Thu Fri', calendar = None, frequency='H', sample='1'):
        self.__startDate = startDate
        self.__endDate = endDate
        self.__sample = sample

        acceptable_freq = ['B', 'C', 'D', 'W', 'M', 'SM', 'BM', 'CBM', 'MS', 'SMS',
                            'BMS', 'CBMS', 'Q', 'BQ', 'QS', 'BQS', 'A', 'Y', 'BA', 
                            'BY', 'AS', 'YS', 'BAS', 'BYS', 'BH', 'H', 'T', 'S', 'L', 'U', 'N']
        if frequency not in acceptable_freq:
            raise ValueError('Frequency Value Not acceptable. Specify D, M, H, S')
        self.__frequency = frequency

        start = datetime.strptime(startTime, '%H:%M')
        self.startMinuteDelta = start.hour * 60 + start.minute
        end = datetime.strptime(endTime, '%H:%M')
        self.endMinuteDelta = end.hour * 60 + end.minute

        if(calendar != None):
            self.__bday = CustomBusinessDay(calendar = calendar)
            self.__bhour =  CustomBusinessHour(start = startTime, end = endTime, calendar = calendar)
        else:
            self.__bday = CustomBusinessDay(holidays = holidays, weekmask = weekmask)
            self.__bhour = CustomBusinessHour(start = startTime, end = endTime, holidays = holidays, weekmask = weekmask)

    def createBusinessDaySeries(self):
        return pd.date_range(start=self.__startDate, end=self.__endDate, freq= self.__bday)

    def createBusinessHourSeries(self):
        return pd.date_range(start=self.__startDate, end=self.__endDate, freq= self.__bhour)

    def createBusinessMinSeries(self):
        day_series = self.createBusinessDaySeries()
        datetime_index = None
        for day in day_series:
            if(datetime_index is None):
                datetime_index = pd.date_range(start=day+timedelta(minutes=self.startMinuteDelta), end=day+timedelta(minutes=self.endMinuteDelta), freq= self.__sample + ' min')
            else:
                datetime_index = datetime_index.append(pd.date_range(start=day+timedelta(minutes=self.startMinuteDelta), end=day+timedelta(minutes=self.endMinuteDelta), freq= self.__sample + ' min'))
        return datetime_index

    def createBusinessSecSeries(self):
        day_series = self.createBusinessDaySeries()
        datetime_index = None
        for day in day_series:
            if(datetime_index is None):
                datetime_index = pd.date_range(start=day+timedelta(minutes=self.startMinuteDelta), end=day+timedelta(minutes=self.endMinuteDelta), freq= self.__sample + ' s')
            else:
                datetime_index = datetime_index.append(pd.date_range(start=day+timedelta(minutes=self.startMinuteDelta), end=day+timedelta(minutes=self.endMinuteDelta), freq= self.__sample + ' s'))
        return datetime_index

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
        else:
            try: 
                time_range = pd.date_range(start=self.__startDate, end=self.__endDate, freq= self.__frequency)
            except ValueError as e:
                print(e)


        for timestamp in time_range:
            yield timestamp
