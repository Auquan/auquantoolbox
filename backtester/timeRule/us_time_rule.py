from backtester.timeRule.custom_time_rule import CustomTimeRule
from datetime import datetime, timedelta
import pandas as pd
from pandas.tseries.offsets import CustomBusinessHour
from pandas.tseries.offsets import CustomBusinessDay
from pandas.tseries.holiday import USFederalHolidayCalendar
import os


class USTimeRule(CustomTimeRule):
    def __init__(self, startDate, endDate, startTime='9:30', endTime='15:30', frequency='H', sample='1'):
        super(USTimeRule, self).__init__(startDate = startDate, endDate = endDate, startTime = startTime, endTime = endTime, calendar = USFederalHolidayCalendar(), frequency = frequency, sample = sample)
