from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem
from backtester.logger import *
import numpy as np
import pandas as pd


class SimpleExecutionSystemWithFairValue(SimpleExecutionSystem):
    def __init__(self, enter_threshold_deviation=0.07, exit_threshold_deviation=0.05, longLimit=10,
                 shortLimit=10, capitalUsageLimit=0, enterlotSize=1, exitlotSize=1, limitType='L', price=''):
        super(SimpleExecutionSystemWithFairValue, self).__init__(enter_threshold=enter_threshold_deviation,
                                                                 exit_threshold=exit_threshold_deviation,
                                                                 longLimit=longLimit, shortLimit=shortLimit,
                                                                 capitalUsageLimit=capitalUsageLimit,
                                                                 enterlotSize=enterlotSize, exitlotSize=exitlotSize, limitType=limitType, price=price)

    def getDeviationFromPrediction(self, currentPredictions, instrumentsManager):
        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        try:
            currentPrice = instrumentLookbackData.getFeatureDf(self.priceFeature).iloc[-1]
        except KeyError:
            logError('You have specified FairValue Execution Type but Price Feature Key does not exist')

        currentDeviationFromPrediction = currentPredictions.transpose() - currentPrice
        return currentDeviationFromPrediction

    def getBuySell(self, currentPredictions, instrumentsManager):
        currentDeviationFromPrediction = self.getDeviationFromPrediction(currentPredictions, instrumentsManager)
        return np.sign(currentDeviationFromPrediction)

    def enterCondition(self, currentPredictions, instrumentsManager):
        currentDeviationFromPrediction = self.getDeviationFromPrediction(currentPredictions, instrumentsManager)
        return np.abs(currentDeviationFromPrediction) > (self.enter_threshold)

    def exitCondition(self, currentPredictions, instrumentsManager):
        currentDeviationFromPrediction = self.getDeviationFromPrediction(currentPredictions, instrumentsManager)
        return np.abs(currentDeviationFromPrediction) < (self.exit_threshold)

    def hackCondition(self, currentPredictions, instrumentsManager):
        return pd.Series(False, index=currentPredictions.index)

    # def getExecutions(self, time, instrumentsManager, capital):
    # 	# TODO:
    # 	marketFeaturesDf = instrumentsManager.getDataDf()
    # 	currentMarketFeatures = marketFeaturesDf.iloc[-1]
    # 	currentPredictions = marketFeaturesDf['prediction'].iloc[-1]
    # 	logInfo(str(currentPredictions))
    # 	currentDeviationFromPredictions = {}
    # 	currentProbabilityPredictions = {}
    # 	for instrumentId in currentPredictions.keys():
    # 		instrument = instrumentsManager.getInstrument(instrumentId)
    # 		if instrument is None:
    # 			continue
    # 		try:
    # 			currentPrice = instrument.getDataDf()[self.priceFeature].iloc[-1]
    # 		except KeyError:
    # 			logError('You have specified FairValue Execution Type but Price Feature Key does not exist')

    # 		currentDeviationFromPrediction = currentPredictions[instrumentId]/currentPrice
    # 		currentProbabilityPredictions[instrumentId] = currentDeviationFromPrediction/2

    # 	executions = []
    # 	executions += self.exitPosition(instrumentsManager, currentProbabilityPredictions)
    # 	executions += self.enterPosition(instrumentsManager, currentProbabilityPredictions, capital)
    # 	return executions
