from base_execution_system import BaseExecutionSystem, InstrumentExection
from backtester.logger import *
import numpy as np

class SimpleExecutionSystem(BaseExecutionSystem):
	def __init__(self, enter_threshold=0.7, exit_threshold=0.55, longLimit=10, shortLimit=10, lotSize=1):
		self.enter_threshold = enter_threshold
		self.exit_threshold = exit_threshold
		self.longLimit = longLimit
		self.shortLimit = shortLimit
		self.lotSize = lotSize

	def getLongLimit(self, instrumentId):
		if isinstance(self.longLimit, dict):
			return self.longLimit[instrumentId]
		else:
			return self.longLimit

	def getShortLimit(self, instrumentId):
		if isinstance(self.shortLimit, dict):
			return self.shortLimit[instrumentId]
		else:
			return self.shortLimit

	def getLotSize(self, instrumentId):
		if isinstance(self.lotSize, dict):
			return self.lotSize[instrumentId]
		else:
			return self.lotSize

	def getExecutions(self, time, instrumentsManager):
		# TODO:
		marketFeaturesDf = instrumentsManager.getDataDf()
		currentMarketFeatures = marketFeaturesDf.iloc[-1]
		currentPredictions = marketFeaturesDf['prediction'].iloc[-1]
		print(currentPredictions)
		executions = []
		executions += self.exitPosition(instrumentsManager, currentPredictions)
		executions += self.enterPosition(instrumentsManager, currentPredictions)
		return executions
	
	def exitPosition(self, instrumentsManager, currentPredictions):
		executions = []
		instruments = instrumentsManager.getAllInstrumentsByInstrumentId().values()
		for instrument in instruments:
			position = instrument.getCurrentPosition()
			if position == 0:
				continue
			# take Profits
			if self.exitCondition(instrumentsManager, instrument, currentPredictions):
				instrumentExec = InstrumentExection(instrument.getInstrumentId(), np.abs(position), -np.sign(position))
				executions.append(instrumentExec)

			#hack
			elif self.hackCondition(instrumentsManager):
				instrumentExec = InstrumentExection(instrument.getInstrumentId(), np.abs(position), -np.sign(position))
				executions.append(instrumentExec)
		return executions

	def enterPosition(self, instrumentsManager, currentPredictions):
		executions = []
		for instrumentId in currentPredictions.keys():
			instrument = instrumentsManager.getInstrument(instrumentId)
			if instrument is None:
				continue
			#Dont add if already at limit
			if self.atPositionLimit(instrumentsManager, instrument):
				continue
			#Enter position if condition met
			if self.enterCondition(instrumentsManager, instrument, currentPredictions):
				print(instrumentId, self.getLotSize(instrumentId),np.sign(currentPredictions[instrumentId] - 0.5))
				instrumentExec = InstrumentExection(instrumentId, 
													self.getLotSize(instrumentId), 
													np.sign(currentPredictions[instrumentId] - 0.5))
				executions.append(instrumentExec)
		return executions

	def enterCondition(self, instrumentsManager, instrument, currentPredictions):
		instrumentId = instrument.getInstrumentId()
		probBuy = currentPredictions[instrumentId]
		return np.abs(probBuy - 0.5) > (self.enter_threshold - 0.5)

	def atPositionLimit(self, instrumentsManager, instrument):
		position = instrument.getCurrentPosition()
		instrumentId = instrument.getInstrumentId()
		if (position > self.getLongLimit(instrumentId)) or (position < -self.getShortLimit(instrumentId)):
			logInfo('At Position Limit for %s'%instrumentId)
			return True
		return False

	def exitCondition(self, instrumentsManager, instrument, currentPredictions):
		instrumentId = instrument.getInstrumentId()
		probBuy = currentPredictions[instrumentId]
		return np.abs(probBuy - 0.5) < (self.exit_threshold - 0.5)

	def hackCondition(self, instrumentsManager):
		return False