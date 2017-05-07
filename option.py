import math
from scipy.stats import norm
import pandas as pd
from datetime import date
from datetime import datetime
import numpy as np
import constants
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
    def __init__(self, futurePrice, instrumentId, exp_date, instrumentPrefix, eval_date, rf=0.01, vol=0.3, div=0):
        self.s = futurePrice
        self.k = getStrikePriceFromInstrumentId(instrumentId, instrumentPrefix)
        self.rf = rf
        self.vol = vol
        self.eval_date = eval_date # TODO: should be eval_time
        self.exp_date = exp_date
        self.t = self.calculate_t()
        if self.t == 0:
            self.t = 0.000001  # Case valuation in expiration date
        self.price = 0 # TODO: Set from given vol and s
        self.div = div
        # TODO: change type to enum constants instead
        self.type = "C" if (instrumentId.endswith("003")) else "P"
        self.instrumentId = instrumentId

    def updateWithInstrument(self, optionInstrument, currentFutureVal):
        self.eval_date = optionInstrument.time
        self.s = get_index_val(currentFutureVal, constants.ROLL)
        self.price = optionInstrument.getVwap()
        self.vol = self.get_impl_vol()


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

    def get_impl_vol(self, guess=0.16):
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
# CLASS OPTIONS STRATEGY
#=========================================================================
class Options_strategy:
    """
    This class will calculate greeks for a group of options (called Options Strategy)
    """

    def __init__(self, df_options):
        # It will store the different options in a pandas dataframe
        self.df_options = df_options

    def get_greeks(self):
        """
        For analysis underlying (option chain format)
        """
        self.delta = 0
        self.gamma = 0
        self.theta = 0
        for k, v in self.df_options.iterrows():

            # Case stock or future
            if v['m_secType'] == 'STK':
                self.delta += float(v['position']) * 1

            # Case option
            elif v['m_secType'] == 'OPT':
                opt = Option(s=v['underlying_price'], k=v['m_strike'], eval_date=date.today(),  # We want greeks for today
                             exp_date=v['m_expiry'], rf=v[
                                 'interest'], vol=v['volatility'],
                             type=v['m_type'])

                price, delta, theta, gamma = opt.get_all()

                self.delta += float(v['position']) * delta
                self.gamma += float(v['position']) * gamma
                self.theta += float(v['position']) * theta

            else:
                print "ERROR: Not known type"

        return self.delta, self.gamma, self.theta

    def get_greeks2(self):
        """
        For analysis_options_strategy
        """
        self.delta = 0
        self.gamma = 0
        self.theta = 0
        for k, v in self.df_options.iterrows():

            # Case stock or future
            if v['m_secType'] == 'STK':
                self.delta += float(v['position']) * 1

            # Case option
            elif v['m_secType'] == 'OPT':
                opt = Option(s=v['underlying_price'], k=v['m_strike'], eval_date=date.today(),  # We want greeks for today
                             exp_date=v['m_expiry'], rf=v[
                                 'interest'], vol=v['volatility'],
                             type=v['m_type'])

                price, delta, theta, gamma = opt.get_all()

                if v['m_side'] == 'BOT':
                    position = float(v['position'])
                else:
                    position = - float(v['position'])
                self.delta += position * delta
                self.gamma += position * gamma
                self.theta += position * theta

            else:
                print "ERROR: Not known type"

        return self.delta, self.gamma, self.theta


if __name__ == '__main__':
 
 
    #===========================================================================
    # TO CHECK OPTION CALCULATIONS
    #===========================================================================
    s = 22307
    k = 22300   
    exp_date = '20170504 15:30:00'
    eval_date = datetime.now()
    rf = .064
    vol = 0.155
    div = 0
    type = 'C'
    opt = Option(s=s, k=k, eval_date=eval_date, exp_date=exp_date, rf=rf, vol=vol, type=type,
                 div = div)
    # price, delta, theta, gamma = opt.get_all()
    # print "-------------- FIRST OPTION -------------------"
    # print "Price CALL: " + str(price)  # 2.97869320042
    # print "Delta CALL: " + str(delta)  # 0.664877358932
    # print "Theta CALL: " + str(theta)  # 0.000645545628288
    # print "Gamma CALL:" + str(gamma)   # 0.021127937082
 

    #===========================================================================
    # TO CHECK OPTION IMPLIED VOLATILITY CALCULATION 
    #===========================================================================
    bid_vol, bid_price, ask_price, ask_vol = [120 ,  69.40 ,  70.00   ,3560  ]
    vwap_price = (float(bid_price) * float(ask_vol) + float(ask_price) * float(bid_vol))/float(bid_vol+ask_vol) 
    opt = Option(s=s, k=k, eval_date=eval_date, exp_date=exp_date, rf=rf, price=vwap_price, type=type)
    ivol = opt.get_impl_vol(vol)
    price, delta, theta, gamma = opt.get_all()
    print "-------------- FIRST OPTION -------------------"
    print "VWAP Price: " + str(vwap_price)
    print "Implied Volatility: " + str(ivol)
    print "Price CALL: " + str(price)
    price = opt.get_price_by_binomial_tree()
    print "Price by BT:" + str(price)


    k = 22300
    type = 'P'
    opt = Option(s=s, k=k, eval_date=eval_date, exp_date=exp_date, rf=rf, vol=vol, type=type)
    # price, delta, theta, gamma = opt.get_all()
    # print "-------------- SECOND OPTION -------------------"
    # print "Price CALL: " + str(price)   # 7.02049813137
    # print "Delta CALL: " + str(delta)   # 0.53837898036
    # print "Theta CALL: " + str(theta)   # -0.00699852931575
    # print "Gamma CALL:" + str(gamma)    # 0.0230279263655

    #===========================================================================
    # TO CHECK OPTION IMPLIED VOLATILITY CALCULATION 
    #===========================================================================
    bid_vol, bid_price, ask_price, ask_vol = [960 ,65.10 ,  65.65  , 200]  
    vwap_price =0.8# (float(bid_price) * float(ask_vol) + float(ask_price) * float(bid_vol))/float(bid_vol+ask_vol)  ## Calculated for a vol = 0.12353
    opt = Option(s=s, k=k, eval_date=eval_date, exp_date=exp_date, rf=rf, price=vwap_price, type=type)
    ivol = opt.get_impl_vol(vol)
    price, delta, theta, gamma = opt.get_all()
    print "-------------- SECOND OPTION -------------------"
    print "VWAP Price: " + str(vwap_price)
    print "Implied Volatility: " + str(ivol)
    print "Price: " + str(price)   # 7.02049813137
    price = opt.get_price_by_binomial_tree()
    print "Price by BT:" + str(price)



    #===========================================================================
    # TO CHECK OPTIONS STRATEGIES CALCULATIONS
    #===========================================================================
    # d_option1 = {'m_secType': 'OPT', 'm_expiry': '20150116', 'm_type': 'C', 'm_symbol': 'TLT', 'm_strike': '115', 
    #              'm_multiplier': '100', 'position': '-2', 'trade_price': '3.69', 'comission': '0',
    #              'eval_date': '20140422', 'interest': '0.01', 'volatility': '0.12353', 'underlying_price': '109.96'}
    # d_option2 = {'m_secType': 'OPT', 'm_expiry': '20150116', 'm_type': 'C', 'm_symbol': 'TLT', 'm_strike': '135', 
    #              'm_multiplier': '100', 'position': '2', 'trade_price': '0.86', 'comission': '0',
    #              'eval_date': '20140422', 'interest': '0.01', 'volatility': '0.12353', 'underlying_price': '109.96'}
 
    # df_options = pd.DataFrame([d_option1, d_option2])
    # opt_strat = Options_strategy(df_options)
    # delta, gamma, theta = opt_strat.get_greeks()
    # print "-------- OPTIONS STRATEGY --------------"
    # print "Delta: " + str(delta)
    # print "Gamma: " + str(gamma)
    # print "Theta: " + str(theta)