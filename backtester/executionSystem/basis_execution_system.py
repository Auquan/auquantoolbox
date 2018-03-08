from backtester.executionSystem.simple_execution_system_fairvalue import SimpleExecutionSystemWithFairValue
from backtester.logger import *
import numpy as np
import pandas as pd
import time
from datetime import datetime, time, timedelta


class BasisExecutionSystem(SimpleExecutionSystemWithFairValue):
    def __init__(self, basisEnter_threshold=0.5, basisExit_threshold=0.1,
                 basisLongLimit=5000, basisShortLimit=5000,
                 basisCapitalUsageLimit=0.05, basisLotSize=100,
                 basisLimitType='L', basis_thresholdParam='sdev',
                 price='', feeDict=0.0001, feesRatio=1.5, spreadLimit=0.1,
                 hackTime = time(15,25,0)):
        super(BasisExecutionSystem, self).__init__(enter_threshold_deviation=basisEnter_threshold,
                                                   exit_threshold_deviation=basisExit_threshold,
                                                   longLimit=basisLongLimit, shortLimit=basisShortLimit,
                                                   capitalUsageLimit=basisCapitalUsageLimit, 
                                                   enterlotSize=basisLotSize, exitlotSize = 5*basisLotSize,
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
        return currentSpread / 4.0

    def getFees(self, instrumentsManager):
        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        try:
            # TODO: Change the hard key references
            currentStockPrice = instrumentLookbackData.getFeatureDf('stockVWAP').iloc[-1]
        except KeyError:
            logError('VWAP Price Feature Key does not exist')

        return currentStockPrice * self.fees

    def getBuySell(self, currentPredictions, instrumentsManager):
        currentDeviationFromPrediction = self.getDeviationFromPrediction(currentPredictions, instrumentsManager)
        return -np.sign(currentDeviationFromPrediction)

    def enterCondition(self, currentPredictions, instrumentsManager):
        currentDeviationFromPrediction = self.getDeviationFromPrediction(currentPredictions, instrumentsManager)
        currentSpread = self.getSpread(instrumentsManager)
        # print(np.minimum(self.spreadLimit, currentSpread))
        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        if instrumentLookbackData.getFeatureDf('position').index[-1].time() < time(15,25,0):#(self.hackTime - timedelta(minutes=10)) :
            shouldTrade = np.abs(currentDeviationFromPrediction) > (self.enter_threshold) * np.abs(instrumentsManager.getLookbackInstrumentFeatures().getFeatureDf(self.thresholdParam).iloc[-1])
            shouldTrade[np.abs(currentDeviationFromPrediction) - (self.feesRatio * 2 * self.getFees(instrumentsManager)) - 2 * np.minimum(self.spreadLimit, currentSpread)< 0 ]=False
            shouldTrade[instrumentLookbackData.getFeatureDf('enter_flag').iloc[-1]==True] = False
            # shouldTrade[currentSpread > self.spreadLimit] = False
            # shouldTrade[['HDFCBANK', 'YESBANK', 'IBREALEST']] = False
            # print('enter_flag')
            # print(instrumentLookbackData.getFeatureDf('enter_flag').iloc[-1])
        else:
            print('Trading time over')
            shouldTrade = pd.Series(False, index=currentPredictions.index)

        # print(instrumentLookbackData.getFeatureDf('basis').iloc[-1])
        # print(instrumentLookbackData.getFeatureDf('stockVWAP').iloc[-1])
        # print(instrumentLookbackData.getFeatureDf('futureVWAP').iloc[-1])
        # print(currentDeviationFromPrediction)
        # print('Check if we are outside error thresholdParam')
        # print(np.abs(currentDeviationFromPrediction) > (self.enter_threshold) * np.abs(instrumentsManager.getLookbackInstrumentFeatures().getFeatureDf(self.thresholdParam).iloc[-1]))
        # print(currentSpread)
        # print(self.feesRatio * 4 * self.getFees(instrumentsManager))
        # print('Check if fee critera met')
        # print(np.abs(currentDeviationFromPrediction) - (self.feesRatio * 4 * self.getFees(instrumentsManager)) - 4 * np.minimum(self.spreadLimit, currentSpread))
        # print('Check if spread limit met')
        # print(currentSpread > self.spreadLimit)
        # print(shouldTrade)
        return shouldTrade

    def exitCondition(self, currentPredictions, instrumentsManager):
        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        currentDeviationFromPrediction = self.getDeviationFromPrediction(currentPredictions, instrumentsManager)
        currentSpread = self.getSpread(instrumentsManager)
        try:
            currentMidPrice = instrumentLookbackData.getFeatureDf(self.priceFeature).iloc[-1]
        except KeyError:
            logError('You have specified FairValue Execution Type but Price Feature Key does not exist')
        avgEnterPrice = instrumentLookbackData.getFeatureDf('enter_price').iloc[-1]
        avgEnterDeviation = currentMidPrice.transpose() - avgEnterPrice
        position = instrumentLookbackData.getFeatureDf('position').iloc[-1]
        avgEnterDeviation[position==0] = 0
        # print(currentDeviationFromPrediction)
        # print((self.exit_threshold) * np.abs(instrumentLookbackData.getFeatureDf(self.thresholdParam).iloc[-1]))
        # print('Check if exit exitCondition met')
        # print(-np.sign(position) * (currentDeviationFromPrediction) < (self.exit_threshold) * np.abs(instrumentLookbackData.getFeatureDf(self.thresholdParam).iloc[-1]))
        
        ## Exit if no longer attractive
        #shouldExit = -np.sign(position) * (currentDeviationFromPrediction) < (self.exit_threshold) * np.abs(instrumentLookbackData.getFeatureDf(self.thresholdParam).iloc[-1])
        
        ## Exit to collect profits
        shouldExit[avgEnterDeviation*np.sign(position) - (self.feesRatio * 4 * self.getFees(instrumentsManager)) - 4 * np.minimum(self.spreadLimit, currentSpread) > 0 ]=True
        return shouldExit

    def hackCondition(self, currentPredictions, instrumentsManager):
        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        position = instrumentLookbackData.getFeatureDf('position').iloc[-1]
        hack = pd.Series(False, index=currentPredictions.index)
        if instrumentLookbackData.getFeatureDf('position').index[-1].time() > self.hackTime :
            hack[position!=0] = True
            print('Hacking at Close......')
            print(hack)
        return hack


    # def getExecutions(self, time, instrumentsManager, capital):
    #   # TODO:
    #   marketFeaturesDf = instrumentsManager.getDataDf()
    #   currentMarketFeatures = marketFeaturesDf.iloc[-1]
    #   currentPredictions = marketFeaturesDf['prediction'].iloc[-1]
    #   logInfo(str(currentPredictions))
    #   currentDeviationFromPredictions = {}
    #   currentProbabilityPredictions = {}
    #   for instrumentId in currentPredictions.keys():
    #       instrument = instrumentsManager.getInstrument(instrumentId)
    #       if instrument is None:
    #           continue
    #       try:
    #           currentPrice = instrument.getDataDf()[self.priceFeature].iloc[-1]
    #       except KeyError:
    #           logError('You have specified FairValue Execution Type but Price Feature Key does not exist')

    #       currentDeviationFromPrediction = currentPredictions[instrumentId]/currentPrice
    #       currentProbabilityPredictions[instrumentId] = currentDeviationFromPrediction/2

    #   executions = []
    #   executions += self.exitPosition(instrumentsManager, currentProbabilityPredictions)
    #   executions += self.enterPosition(instrumentsManager, currentProbabilityPredictions, capital)
    #   return executions
