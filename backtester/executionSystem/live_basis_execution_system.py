from backtester.executionSystem.simple_execution_system_fairvalue import SimpleExecutionSystemWithFairValue
from backtester.logger import *
import numpy as np
import pandas as pd
import time
from datetime import datetime, time, timedelta


class LiveBasisExecutionSystem(SimpleExecutionSystemWithFairValue):
    def __init__(self, basisEnter_threshold=0.5, basisExit_threshold=0.1,
                 basisLongLimit=5000, basisShortLimit=5000,
                 basisCapitalUsageLimit=0.05, basisLotSize=100,
                 basisLimitType='L', basis_thresholdParam='sdev',
                 price='', feeDict=0.0001, feesRatio=1.5, spreadLimit=0.1,
                 hackTime = time(15,25,0)):
        super(LiveBasisExecutionSystem, self).__init__(enter_threshold_deviation=basisEnter_threshold,
                                                   exit_threshold_deviation=basisExit_threshold,
                                                   longLimit=basisLongLimit, shortLimit=basisShortLimit,
                                                   capitalUsageLimit=basisCapitalUsageLimit,
                                                   enterlotSize=basisLotSize, exitlotSize = 2*basisLotSize,
                                                   limitType=basisLimitType, price=price)
        self.fees = feeDict
        self.thresholdParam = basis_thresholdParam
        self.feesRatio = feesRatio
        self.spreadLimit = spreadLimit
        self.hackTime = hackTime

    def getDeviationFromPrediction(self, currentPredictions, instrumentsManager):
        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        try:
            currentMidPrice = instrumentLookbackData.getFeatureDf(self.priceFeature).iloc[-1]
        except KeyError:
            logError('You have specified FairValue Execution Type but Price Feature Key does not exist')

        currentDeviationFromPrediction = currentMidPrice.transpose() - currentPredictions
        return currentDeviationFromPrediction

    def getSpread(self, instrumentsManager):
        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        try:
            # TODO: Change the hard key references
            currentStockBidPrice = instrumentLookbackData.getFeatureDf('stockTopBidPrice').iloc[-1]
            currentStockAskPrice = instrumentLookbackData.getFeatureDf('stockTopAskPrice').iloc[-1]
            currentFutureBidPrice = instrumentLookbackData.getFeatureDf('futureTopBidPrice').iloc[-1]
            currentFutureAskPrice = instrumentLookbackData.getFeatureDf('futureTopAskPrice').iloc[-1]
        except KeyError:
            logError('Bid and Ask Price Feature Key does not exist')

        currentSpread = currentStockAskPrice - currentStockBidPrice + currentFutureAskPrice - currentFutureBidPrice
        return np.maximum(self.spreadLimit ,currentSpread / 4.0)

    def getFees(self, instrumentsManager):
        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        try:
            # TODO: Change the hard key references
            currentStockPrice = instrumentLookbackData.getFeatureDf('stockVWAP').iloc[-1]
        except KeyError:
            logError('VWAP Price Feature Key does not exist')

        return currentStockPrice * self.fees

    def getBuySell(self, currentPredictions, instrumentsManager):
        return pd.Series(1, index=currentPredictions.index)

    def enterCondition(self, currentPredictions, instrumentsManager):
        return pd.Series(True, index=currentPredictions.index)

    def exitCondition(self, currentPredictions, instrumentsManager):
        return pd.Series(False, index=currentPredictions.index)

    def hackCondition(self, currentPredictions, instrumentsManager):
        hack = pd.Series(False, index=currentPredictions.index)
        return hack


