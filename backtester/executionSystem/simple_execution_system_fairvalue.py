from simple_execution_system import SimpleExecutionSystem
from backtester.logger import *
import numpy as np

class SimpleExecutionSystemWithFairValue(SimpleExecutionSystem):
	def __init__(self, enter_threshold_deviation=0.07, exit_threshold_deviation=0.05, longLimit=10, \
				shortLimit=10, capitalUsageLimit = 0,lotSize=1, limitType='L',price=''):
		super(SimpleExecutionSystemWithFairValue, self).__init__(enter_threshold=enter_threshold_deviation, 
    				 exit_threshold=exit_threshold_deviation, 
    				 longLimit=longLimit, shortLimit=shortLimit,
    				 capitalUsageLimit = capitalUsageLimit, 
    				 lotSize=lotSize, limitType=limitType,price=price)

	def getBuySell(self, instrument, currentPredictions):
		instrumentId = instrument.getInstrumentId()
		try:
			currentPrice = instrument.getDataDf()[self.price].iloc[-1]
			fairValue = currentPredictions[instrumentId]
			currentDeviationFromPrediction = fairValue/currentPrice
			return -np.sign(currentDeviationFromPrediction) 
		except KeyError:
			logError('You have specified FairValue Execution Type but Price Feature Key does not exist')

	def enterCondition(self, instrumentsManager, instrument, currentPredictions):
		instrumentId = instrument.getInstrumentId()
		try:
			currentPrice = instrument.getDataDf()[self.price].iloc[-1]
			fairValue = currentPredictions[instrumentId]
			currentDeviationFromPrediction = fairValue/currentPrice
			return np.abs(currentDeviationFromPrediction) > (self.enter_threshold)
		except KeyError:
			logError('You have specified FairValue Execution Type but Price Feature Key does not exist')
		

	def exitCondition(self, instrumentsManager, instrument, currentPredictions):
		instrumentId = instrument.getInstrumentId()
		try:
			currentPrice = instrument.getDataDf()[self.price].iloc[-1]
			fairValue = currentPredictions[instrumentId]
			currentDeviationFromPrediction = fairValue/currentPrice
			return np.abs(currentDeviationFromPrediction) < (self.exit_threshold)
		except KeyError:
			logError('You have specified FairValue Execution Type but Price Feature Key does not exist')

	def hackCondition(self, instrumentsManager):
		return False

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
	# 			currentPrice = instrument.getDataDf()[self.price].iloc[-1]
	# 		except KeyError:
	# 			logError('You have specified FairValue Execution Type but Price Feature Key does not exist')

	# 		currentDeviationFromPrediction = currentPredictions[instrumentId]/currentPrice
	# 		currentProbabilityPredictions[instrumentId] = currentDeviationFromPrediction/2

	# 	executions = []
	# 	executions += self.exitPosition(instrumentsManager, currentProbabilityPredictions)
	# 	executions += self.enterPosition(instrumentsManager, currentProbabilityPredictions, capital)
	# 	return executions