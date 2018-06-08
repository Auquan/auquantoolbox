from backtester.timeRule.custom_time_rule import CustomTimeRule
from datetime import datetime, timedelta
import pandas as pd
from pandas.tseries.offsets import CustomBusinessHour
from pandas.tseries.offsets import CustomBusinessDay
from pandas.tseries.holiday import USFederalHolidayCalendar
import os


class USTimeRule(CustomTimeRule):
    def __init__(self, startDate, endDate, frequency='H', sample='1'):
        super().__init__(startDate = startDate, endDate = endDate, calendar = USFederalHolidayCalendar(), frequency = frequency, sample = sample)
