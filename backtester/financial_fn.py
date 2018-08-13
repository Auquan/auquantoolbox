from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import pandas as pd
import math


def writecsv(results, filename):
    print('writing %s.csv' % filename)
    try:
        csv_file = open('%s.csv' % filename, 'wb')
        results.to_csv(csv_file)
    except:
        csv_file = open('%s.csv' % filename, 'w')
        results.to_csv(csv_file)
    csv_file.close()


def calc_realized(last, fut, period, time):
    if last != 0:
        fut = pd.concat([pd.DataFrame([last]), fut])
    ret = fut / fut.shift(1) - 1
    ret.dropna(inplace=True)
    sqsum = (ret**2).rolling(window=period).sum()
    rvol = np.sqrt(252 * sqsum / time)
    return rvol


def calc_var_RT(var, fut, fut0):
    if fut0 > 0:
        var = var + (fut / fut0 - 1)**2
    return var


def ema_RT(prev_ema, data, period):
    alpha = 1 - math.exp(math.log(0.5) / period)
    avg = data * alpha + prev_ema * (1 - alpha)
    return avg


def ma(data, period):
    avg = data.rolling(window=period).mean()
    return avg


def ema(data, period):
    avg = data.ewm(halflife=period).mean()
    return avg

def msdev(data,period):
    s = data.rolling(window=period).std()
    return s
    
def convert_time(timestamp):
    try:
        d = pd.to_datetime(timestamp, infer_datetime_format=True)
    except:
        if isinstance(timestamp, basestring):
            d = dt.datetime.strptime(timestamp, "%Y/%m/%d %H:%M:%S:%f")
        elif type(timestamp) == float or type(timestamp) == long or type(timestamp) == np.float64:
            (year, month, day, hour, minute, second, microsecond) = (str(timestamp)[0:4], str(timestamp)[4:6], str(
                timestamp)[6:8], str(timestamp)[8:10], str(timestamp)[10:12], str(timestamp)[12:14], str(timestamp)[14:])
            d = dt(int(year), int(month), int(day), int(hour), int(minute), int(second), int(microsecond))
        else:
            d = timestamp
    return d


def calculate_t(eval_date, exp_date):
    t = calculate_t_days(eval_date, exp_date) / 365.0
    return t


def calculate_t_days(eval_date, exp_date):
    d0 = convert_time(eval_date)
    d1 = convert_time(exp_date)
    sec = (d1 - d0).seconds
    if(sec < 3600):
        sec = (sec) / 12000.0
    elif(sec < 21300):
        sec = sec / 70800.0 + 0.25
    elif (sec < 22500):
        sec = sec / 12000.0 - 1.225
    else:
        sec = 1
    t = (busday_count(d0, d1) + sec)
    return t


def busday_count(start, end):
    daydiff = end.weekday() - start.weekday()
    days = ((end - start).days - daydiff) / 7 * 5 + min(daydiff, 5) - (max(end.weekday() - 4, 0) % 5)
    return days
