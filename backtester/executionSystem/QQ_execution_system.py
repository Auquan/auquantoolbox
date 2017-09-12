from backtester.executionSystem.simple_execution_system_fairvalue import SimpleExecutionSystemWithFairValue
from backtester.logger import *
import numpy as np


class QQExecutionSystem(SimpleExecutionSystemWithFairValue):
    def __init__(self, basisEnter_threshold=0.1, basisExit_threshold=0.05,
                 basisLongLimit=5000, basisShortLimit=5000,
                 basisCapitalUsageLimit=0.05, basisLotSize=100,
                 basisLimitType='L', basis_thresholdParam='sdev',
                 price='', feeDict=0.05):
        super(QQExecutionSystem, self).__init__(enter_threshold_deviation=basisEnter_threshold,
                                                exit_threshold_deviation=basisExit_threshold,
                                                longLimit=basisLongLimit, shortLimit=basisShortLimit,
                                                capitalUsageLimit=basisCapitalUsageLimit, lotSize=basisLotSize,
                                                limitType=basisLimitType, price=price)
        self.fees = feeDict
        self.thresholdParam = basis_thresholdParam

    def getBuySell(self, instrument, currentPredictions):
        instrumentId = instrument.getInstrumentId()
        try:
            currentPrice = instrument.getDataDf()[self.priceFeature].iloc[-1]
            fairValue = currentPredictions[instrumentId]
            currentDeviationFromPrediction = currentPrice - fairValue
            return -np.sign(currentDeviationFromPrediction)
        except KeyError:
            logError('You have specified FairValue Execution Type but Price Feature Key does not exist')

    def enterCondition(self, instrumentsManager, instrument, currentPredictions):
        instrumentId = instrument.getInstrumentId()
        try:
            currentPrice = instrument.getDataDf()[self.priceFeature].iloc[-1]
            fairValue = currentPredictions[instrumentId]
            currentDeviationFromPrediction = currentPrice - fairValue
            return np.abs(currentDeviationFromPrediction) -\
                2 * self.fees > (self.enter_threshold) * np.abs(instrument.getDataDf()[self.thresholdParam].iloc[-1])
        except KeyError:
            logError('You have specified FairValue Execution Type but Price Feature Key does not exist')

    def exitCondition(self, instrumentsManager, instrument, currentPredictions):
        instrumentId = instrument.getInstrumentId()
        try:
            currentPrice = instrument.getDataDf()[self.priceFeature].iloc[-1]
            fairValue = currentPredictions[instrumentId]
            currentDeviationFromPrediction = currentPrice - fairValue
            position = instrument.getCurrentPosition()
            return -np.sign(position)*(currentDeviationFromPrediction) < (self.exit_threshold) * np.abs(instrument.getDataDf()[self.thresholdParam].iloc[-1])
        except KeyError:
            logError('You have specified FairValue Execution Type but Price Feature Key does not exist')

    def hackCondition(self, instrumentsManager):
        return False

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
