from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import pandas as pd
import os
import csv
import json
import datetime 
import matplotlib.pyplot as plt
import random
import csv
import re
from datetime import timedelta

def writecsv(results,filename):
    print('writing %s.csv'%filename)
    try:
        csv_file =  open('%s.csv'%filename, 'wb')
        results.to_csv(csv_file)
    except:
        csv_file =  open('%s.csv'%filename, 'w')
        results.to_csv(csv_file)
    csv_file.close()

def calc_realized(last,fut,period):
	if last !=0:
		fut = pd.concat([pd.DataFrame([last]),fut])
	ret = fut / fut.shift(1) - 1
	ret.dropna(inplace=True)
	sqsum = (ret**2).rolling(window=period).sum()
	rvol = np.sqrt(252*sqsum)
	return rvol

def ma(data,period):
    avg = data.rolling(window=period).mean()
    return avg

def ema(data,period):
    avg = data.ewm(halflife=period).mean()
    return avg

def convert_time(timestamp):
    try:
        d = pd.to_datetime(timestamp,infer_datetime_format=True)
    except:
        if isinstance(timestamp, basestring):
            d = datetime.strptime(timestamp,"%Y/%m/%d %H:%M:%S:%f")
        elif type(timestamp)==float or type(timestamp)==long or type(timestamp)==np.float64:
            (year, month, day, hour, minute, second, microsecond) = (str(timestamp)[0:4], str(timestamp)[4:6],str(timestamp)[6:8],str(timestamp)[8:10], str(timestamp)[10:12],str(timestamp)[12:14],str(timestamp)[14:])
            d = datetime(int(year), int(month), int(day),int(hour), int(minute), int(second), int(microsecond))
        else:
            d = timestamp 
    return d

def calculate_t(eval_date,exp_date):
    d0 = convert_time(eval_date)
    d1 = convert_time(exp_date)
    sec = (d1 - d0).seconds
    if(sec < 3600):
            sec = (sec)/12000.0
    elif(sec<21300):
            sec = sec/70800.0+0.25
    elif (sec<22500):
            sec = sec/12000.0 -1.225
    else:
            sec = 1
    t =  (busday_count(d0,d1) + sec)/365.0
    return t

def busday_count(start,end):
    daydiff = end.weekday() - start.weekday()
    days = ((end-start).days - daydiff) / 7 * 5 + min(daydiff,5) - (max(end.weekday() - 4, 0) % 5)
    return days

def get_vwap(bid_vol, bid_price, ask_price, ask_vol):
    volume = (np.sum(bid_vol)+np.sum(ask_vol))
    if volume>0:
        price = (np.sum(bid_price * ask_vol) + np.sum(ask_price * bid_vol))/(100*volume)  ## Calculated for a vol = 0.12353
    else:
        price = (np.sum(bid_price) + np.sum(ask_price) )/(200*len(bid_price))
    return price

def get_exp_date(trade_date, all_dates, p=False):
    day_of_week = pd.to_datetime(trade_date).weekday()
    exp_date = pd.to_datetime(trade_date).date() + timedelta( days = (3-day_of_week) % 7)
    if datetime.datetime.strftime(exp_date,'%Y%m%d') not in all_dates:
        exp_date = pd.to_datetime(exp_date) + timedelta( days = -1)
    exp_date = pd.to_datetime(exp_date) + timedelta( hours=15, minutes=30 )
    if p:
    	print(exp_date)
    return exp_date