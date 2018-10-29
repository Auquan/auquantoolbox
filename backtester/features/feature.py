import numpy as np
import math

def checkData(data):
    if data is None or data.empty :
        raise ValueError('data cannot be null')
        logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
        return None


def checkDataMultiple(data1, data2):
    if data1 is None or data2 is None or data1.empty or data2.empty:
        raise ValueError('data cannot be null')
        logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
        return None


def checkVwapData(askVolume, bidVolume, askPrice, bidPrice):
    if askVolume is None or askVolume.empty:
        raise ValueError('data cannot be null')
        logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
        return None
    if bidVolume is None or bidVolume.empty:
        raise ValueError('data cannot be null')
        logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
        return None
    if askPrice is None or askPrice.empty:
        raise ValueError('data cannot be null')
        logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
        return None
    if bidPrice is None or bidPrice.empty:
        raise ValueError('data cannot be null')
        logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
        return None


def checkPeriod(featureParams):
    if featureParams['period']==0:
        raise ValueError('period cannot be 0')
        return None


def checkScale(featureParams):
    if featureParams['scale']==0:
        raise ValueError('scale cannot be 0')
        return None


def infToNan(data):
    data.replace(np.Inf, np.nan, inplace = True)
    data.replace(-np.Inf, np.nan, inplace = True)


def cClean(data):
    data.replace(np.Inf, np.nan, inplace = True)
    data.replace(-np.Inf, np.nan, inplace = True)
    data.fillna(0.0, inplace = True)

def fClean(data):
    if(math.isinf(data)):
        data = 0
    data = np.nan_to_num(float(data))
    return data

def pClean(data):
    data.fillna(0.0, inplace = True)

class Feature(object):

    '''
    Computing for Instrument Update
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        raise NotImplementedError
        return None

    '''
    Computing for Market.
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        raise NotImplementedError
        return None


    '''
    Computing for Instrument Data.
    '''
    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        raise NotImplementedError
        return None
