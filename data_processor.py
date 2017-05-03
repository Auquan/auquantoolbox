import math
import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
import greeks
import datascraper as ds
import os
import option


def atm_vol(x, y, order):
    delta = 0.5
    if order == 2:
        p = np.polyfit(x, y, 1)
        atmvol = p[0] * delta + p[1]
    else:
        p = np.polyfit(x, y, 2)
        atmvol = p[0] * delta**2 + p[1] * delta + p[2]
    return atmvol


def writecsv(results, filename):

    print('writing %s.csv' % filename)
    try:
        csv_file = open('%s.csv' % filename, 'wb')
        results.to_csv(csv_file)
    except:
        csv_file = open('%s.csv' % filename, 'w')
        results.to_csv(csv_file)
    csv_file.close()


def get_exp_date(trade_date, all_dates):
    day_of_week = pd.to_datetime(trade_date).weekday()
    exp_date = pd.to_datetime(trade_date) + \
        timedelta(days=(3 - day_of_week) % 7)
    if datetime.strftime(exp_date, '%Y%m%d') not in all_dates:
        exp_date = pd.to_datetime(exp_date) + timedelta(days=-1)
    exp_date = pd.to_datetime(exp_date) + timedelta(hours=15, minutes=30)
    print(exp_date)
    return exp_date


def get_index_val(opt_arr):
    rf = opt_arr[0].rf
    t = opt_arr[0].t
    s1 = opt_arr[1].price - opt_arr[0].price + opt_arr[0].k * math.exp(-rf * t)
    s2 = opt_arr[3].price - opt_arr[2].price + opt_arr[2].k * math.exp(-rf * t)
    return (s1 + s2) / 2.0


def get_vwap(bid_vol, bid_price, ask_price, ask_vol):
    try:
        price = (float(bid_price) * float(ask_vol) + float(ask_price) * float(bid_vol)) / \
            (float(bid_vol) + float(ask_vol)) / \
            100  # Calculated for a vol = 0.12353
    except ZeroDivisionError:
        price = (float(bid_price) + float(ask_price)) / 200
    return price


def straddle(opt_arr, s):
    std1 = opt_arr[1].price + opt_arr[0].price
    std2 = opt_arr[3].price + opt_arr[2].price
    d1 = opt_arr[1].delta + opt_arr[0].delta
    d2 = opt_arr[3].delta + opt_arr[2].delta
    atm_std = (std1 + (opt_arr[0].k - s) * d1 / 2 +
               std2 + (opt_arr[2].k - s) * d2 / 2) / 2
    return atm_std

FILE_PATH = 'C:/Users/Chandini/Nifty_Project'
SAMPLE_OPTION_INSTRUMENT_PREFIX = 'BANKNIFTY1152973800'


class UnderlyingProcessor:
    def __init__(self, trade_date, names):
        self.trade_date = trade_date
        self.names = names
        self.futures = []
        self.histOptions = {}

    # returns Future class object
    def getCurrentFuture(self):
        return self.futures[-1]

    # returns dictionary of instrumentId -> Option class object
    def getAllCurrentOptions(self):
        toRtn = {}
        for instrumentId in self.histOptions:
            toRtn[instrumentId] = self.histOptions[instrumentId][-1]
        return toRtn

    # returns Option class object
    def getCurrentOption(self, instrumentId):
        self.ensureInstrumentId(instrumentId)
        return self.histOptions[instrumentId][-1] # TODO: what happens if array is empty

    def ensureInstrumentId(self, instrumentId):
        if instrumentId not in self.histOptions:
            self.histOptions[instrumentId] = []

    def addNewOption(self, opt):
        self.ensureInstrumentId(opt.instrumentId)
        self.histOptions[opt.instrumentId].append(opt)

    def processData(self):
        filename = '%s/%s/data' % (FILE_PATH, self.trade_date)
        exp_date = get_exp_date(self.trade_date, self.names)
        instrumentsToProcess = ds.loadData(filename)  # TODO
        data = pd.DataFrame(index=[], columns=['Future', 'Vol'])
        for instrument in instrumentsToProcess:
            if instrument.isFuture():
                self.futures.append(instrument)
                # todo: update price of options
                # 1. update current future value
                # 2. opt.s = opt.s + futureValue - lastFutureValue
                # 3. calculate Vol (do not change opt.vol) 
                # 3.1 update opt.vol
            else:
                opt = option.Option(futurePrice=self.getCurrentFuture().futureVal,
                                    optionInstrument=instrument,
                                    exp_date=exp_date,
                                    instrumentPrefix=SAMPLE_OPTION_INSTRUMENT_PREFIX,
                                    rf=0.14)
                self.addNewOption(instrument)
                # todo: update new vol
                # 1. update option.price
                # 2. update option.vol
                # 3. calculate Vol




names = next(os.walk(FILE_PATH))[1]
for trade_date in names:
    up = UnderlyingProcessor(trade_date, names)
    up.processData()

    i = 0
    while i < len(df) - 1:
        i += 1
        s = df[i]['future']
        if s == 0:
            print('Future not trading')
            continue
        else:
            eval_date = df[i]['time']
            rf = .14
            div = 0
            keys = ['P0', 'C0', 'P1', 'C1']
            temp_df = pd.DataFrame(index=[eval_date], columns=[
                                   'Future', 'Vol', 'Mkt_Straddle', 'Theo_Straddle'])
            temp_df['Future'] = s
            opt_arr = []
            delta_arr = []
            vol_arr = []
            try:
                for j in range(4):
                    type = keys[j][0]
                    k, price = [df[i][keys[j]]['strike'],
                                df[i][keys[j]]['price']]
                    opt = greeks.Option(s=s, k=float(
                        k), eval_date=eval_date, exp_date=exp_date, rf=rf, price=float(price), type=type)
                    opt_arr.append(opt)
                s = get_index_val(opt_arr)
                for j in range(4):
                    opt = opt_arr[j]
                    opt.s = s
                    ivol = opt.get_impl_vol()
                    opt.vol = ivol
                    price, delta, theta, gamma = opt.get_all()
                    if (delta < 0):
                        delta = 1 + delta
                    delta_arr.append(delta)
                    vol_arr.append(ivol)
                temp_df['Vol'] = atm_vol(delta_arr, vol_arr, 2)
                temp_df['Mkt_Straddle'] = straddle(opt_arr, s)
                opt_atm = greeks.Option(s=s, k=s * math.exp(opt.rf * opt.t), eval_date=eval_date,
                                        exp_date=exp_date, rf=rf, vol=temp_df['Vol'], type='C')
                price, delta, theta, gamma = opt_atm.get_all()
                temp_df['Theo_Straddle'] = 2 * price
                data = data.append(temp_df)
            except:
                continue
        # print(temp_df['Vol'])
    writecsv(data, 'vol_%s' % trade_date)
