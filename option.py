import math
from scipy.stats import norm
import pandas as pd
from datetime import date
from datetime import datetime
import numpy as np
import constants
from scipy.optimize import fsolve
import useful_fn as utils

def getStrikePriceFromInstrumentId(instrumentId, instrumentPrefix):
    return int(instrumentId[len(instrumentPrefix):-3])

def get_index_val(fut, roll):
    # rf = opt_arr[0].rf
    # t = opt_arr[0].t
    # s1 = opt_arr[1].price - opt_arr[0].price + opt_arr[0].k * math.exp(-rf * t)
    # s2 = opt_arr[3].price - opt_arr[2].price + opt_arr[2].k * math.exp(-rf * t)
    return fut - roll

#=========================================================================
# CLASS OPTION
#=========================================================================
class Option:
    """
    This class will group the different black-shcoles calculations for an opion
    """
    def __init__(self, futurePrice, instrumentId, exp_date, instrumentPrefix, eval_date, rf=0.01, vol=0.3, div=0,position=0):
        self.s = futurePrice
        self.k = getStrikePriceFromInstrumentId(instrumentId, instrumentPrefix)
        self.rf = rf
        self.vol = vol
        self.eval_date = eval_date # TODO: should be eval_time
        self.exp_date = exp_date
        self.t = self.calculate_t()
        if self.t <= 0:
            self.t = 0.000001  # Case valuation in expiration date
        self.price = 0 # TODO: Set from given vol and s
        self.div = div
        # TODO: change type to enum constants instead
        self.type = "C" if (instrumentId.endswith("003")) else "P"
        self.instrumentId = instrumentId
        self.position = position

    def updateWithInstrument(self, optionInstrument, currentFutureVal):
        self.eval_date = optionInstrument.time
        self.s = get_index_val(currentFutureVal, constants.ROLL)
        self.price = optionInstrument.getVwap()
        #self.vol = self.get_impl_vol() TOo slow right now to do at every update

    def updateWithOrder(self, order):
        self.position += order.volume
        self.price = order.tradePrice

    def convert_time(self, timestamp):
        try:
            d = pd.to_datetime(timestamp, infer_datetime_format=True)
        except:
            if isinstance(timestamp, basestring):
                d = datetime.strptime(timestamp, "%Y/%m/%d %H:%M:%S:%f")
            elif type(timestamp) == float or type(timestamp) == long or type(timestamp) == np.float64:
                (year, month, day, hour, minute, second, microsecond) = (str(timestamp)[0:4], str(timestamp)[4:6], str(
                    timestamp)[6:8], str(timestamp)[8:10], str(timestamp)[10:12], str(timestamp)[12:14], str(timestamp)[14:])
                d = datetime(int(year), int(month), int(day), int(
                    hour), int(minute), int(second), int(microsecond))
            else:
                d = timestamp
        return d

    def calculate_t(self):
        d0 = self.convert_time(self.eval_date)
        d1 = self.convert_time(self.exp_date)
        sec = (d1 - d0).seconds
        if(sec < 3600):
            sec = (sec) / 12000.0
        elif(sec < 21300):
            sec = sec / 70800.0 + 0.25
        elif (sec < 22500):
            sec = sec / 12000.0 - 1.225
        else:
            sec = 1
        t = (self.busday_count(d0, d1) + sec) / 365.0
        return t

    def busday_count(self, start, end):
        daydiff = end.weekday() - start.weekday()
        days = ((end - start).days - daydiff) / 7 * 5 + \
            min(daydiff, 5) - (max(end.weekday() - 4, 0) % 5)
        return days

    def get_price_delta(self):
        d1 = 0.0 # TODO?
        try:
            d1 = (math.log(self.s / self.k) + (self.rf + self.div +
                                               math.pow(self.vol, 2) / 2) * self.t) / (self.vol * math.sqrt(self.t))
        except:
            print(math.sqrt(self.t))
        d2 = d1 - self.vol * math.sqrt(self.t)
        if self.type == 'C':
            self.calc_price = (norm.cdf(d1) * self.s * math.exp(-self.div *
                                                                self.t) - norm.cdf(d2) * self.k * math.exp(-self.rf * self.t))
            self.delta = norm.cdf(d1)
        elif self.type == 'P':
            self.calc_price = (-norm.cdf(-d1) * self.s * math.exp(-self.div *
                                                                  self.t) + norm.cdf(-d2) * self.k * math.exp(-self.rf * self.t))
            self.delta = -norm.cdf(-d1)

    def get_call(self):
        d1 = ( math.log(self.s/self.k) + ( self.rf + math.pow( self.vol, 2)/2 ) * self.t ) / ( self.vol * math.sqrt(self.t) )
        d2 = d1 - self.vol * math.sqrt(self.t)
        self.call = ( norm.cdf(d1) * self.s - norm.cdf(d2) * self.k * math.exp( -self.rf * self.t ) )
        #put =  ( -norm.cdf(-d1) * self.s + norm.cdf(-d2) * self.k * math.exp( -self.rf * self.t ) ) 
        self.call_delta = norm.cdf(d1)
 
 
    def get_put(self):
        d1 = ( math.log(self.s/self.k) + ( self.rf + math.pow( self.vol, 2)/2 ) * self.t ) / ( self.vol * math.sqrt(self.t) )
        d2 = d1 - self.vol * math.sqrt(self.t)
        #call = ( norm.cdf(d1) * self.s - norm.cdf(d2) * self.k * math.exp( -self.rf * self.t ) )
        self.put =  ( -norm.cdf(-d1) * self.s + norm.cdf(-d2) * self.k * math.exp( -self.rf * self.t ) )
        self.put_delta = -norm.cdf(-d1) 
 

    def get_theta(self, dt=0.0027777):
        self.t += dt
        self.get_price_delta()
        after_price = self.calc_price
        self.t -= dt
        self.get_price_delta()
        orig_price = self.calc_price
        self.theta = (after_price - orig_price) * (-1)

    def get_gamma(self, ds=0.01):
        self.s += ds
        self.get_price_delta()
        after_delta = self.delta
        self.s -= ds
        self.get_price_delta()
        orig_delta = self.delta
        self.gamma = (after_delta - orig_delta) / ds

    def get_all(self):
        self.get_price_delta()
        self.get_theta()
        self.get_gamma()
        return self.calc_price, self.delta, self.theta, self.gamma

    def get_price_diff(self, vol):
        self.vol = vol
        self.get_price_delta()
        return self.calc_price - self.price
 
    def get_impl_vol(self, guess=0.16):
        """
        This function will iterate until finding the implied volatility
        """
        
        ITERATIONS = 100
        ACCURACY = 0.001
        
        roots = fsolve(self.get_price_diff, guess, xtol = ACCURACY, maxfev = ITERATIONS)
        roots = filter(lambda x: x > 0, roots)
        self.vol = 0.00001 if len(roots) == 0 else roots[0]
        self.get_price_delta()

        return self.vol

    def get_impl_vol_slow(self, guess=0.16):
        """
        This function will iterate until finding the implied volatility
        """
        ITERATIONS = 500
        ACCURACY = 0.001
        low_vol = 0
        high_vol = 1
        self.vol = guess  ## It will try mid point and then choose new interval
        self.get_price_delta()
        for i in range(ITERATIONS):
            if self.calc_price > self.price + ACCURACY:
                high_vol = self.vol
            elif self.calc_price < self.price - ACCURACY:
                low_vol = self.vol
            else:
                break
            self.vol = low_vol + (high_vol - low_vol)/2.0
            #print(low_vol,high_vol,self.vol, self.price, self.calc_price)
            self.get_price_delta()
 
        return self.vol

    def get_price_by_binomial_tree(self):
        """
        This function will make the same calculation but by Binomial Tree
        """
        n = 100
        deltaT = self.t / n
        u = math.exp(self.vol * math.sqrt(deltaT))
        d = 1.0 / u
        # Initialize our f_{i,j} tree with zeros
        fs = [[0.0 for j in xrange(i + 1)] for i in xrange(n + 1)]
        a = math.exp(self.rf * deltaT)
        p = (a - d) / (u - d)
        oneMinusP = 1.0 - p
        # Compute the leaves, f_{N,j}
        for j in xrange(i + 1):
            fs[n][j] = max(self.s * u**j * d**(n - j) - self.k, 0.0)
        # print fs

        for i in xrange(n - 1, -1, -1):
            for j in xrange(i + 1):
                fs[i][j] = math.exp(-self.rf * deltaT) * (p * fs[i + 1][j + 1] +
                                                          oneMinusP * fs[i + 1][j])
        # print fs

        return fs[0][0]


#=========================================================================
# CLASS POSITION
#=========================================================================
class Position:
    """
    This class will calculate greeks for a group of options 
    """
    def __init__(self, options_arr): 
        self.options_arr = options_arr       #Store different options with a position in a list
 
    def get_greeks(self):

        self.value = 0
        self.delta = 0
        self.gamma = 0
        self.theta = 0
        self.position = {}
        for opt in self.options_arr:
 
            ## Case stock or future
            if opt.type=='FUT':
                self.delta += float(opt.position) * 1
                self.value += float(opt.position) * opt.price
                self.position[''] = opt.position
 
            ## Case option
            elif (opt.type=='C') or (opt.type=='P') :    
                opt.eval_date=datetime.now() 
                opt.get_impl_vol(vol)
                price, delta, theta, gamma = opt.get_all()
 
                self.value += float(opt.position) * price
                self.delta += float(opt.position) * delta
                self.gamma += float(opt.position) * gamma
                self.theta += float(opt.position) * theta
                self.position[''] = opt.position
 
            else:
                print "ERROR: Not known type"
 
        return self.value, self.delta, self.gamma, self.theta 
 