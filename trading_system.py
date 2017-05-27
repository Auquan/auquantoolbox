import time
from logger import *
from instruments_collection import InstrumentCollection


class TradingSystem:
    '''
    tsParams: Instance of TradingSystemParameters
    '''

    def __init__(self, tsParams):
        self.tsParams = tsParams
        self.instrumentColl = InstrumentCollection()
        self.featuresUpdateTime = None
        self.totalTimeUpdating = 0  # for tracking perf
        self.totalUpdates = 0

    def processInstrumentUpdate(self, instrumentUpdate):
        instrumentIdToUpdate = instrumentUpdate.getInstrumentId()
        instrumentToUpdate = self.instrumentColl.getInstrument(instrumentIdToUpdate)
        instrumentToUpdate.update(instrumentUpdate)
        self.tryUpdateFeatures(instrumentUpdate.getTimeOfUpdate())

    def tryUpdateFeatures(timeOfUpdate):
        shouldUpdateFeatures = False
        if self.featuresUpdateTime is None:
            shouldUpdateFeatures = True
        elif timeOfUpdate >= (self.featuresUpdateTime + self.tsParams.getFrequencyOfFeatureUpdates):
            shouldUpdateFeatures = True
        if shouldUpdateFeatures:
            self.featuresUpdateTime = timeOfUpdate
            # tracking perf
            start = time.time()
            self.updateFeatures(timeOfUpdate)
            end = time.time()
            diffms = (end - start) * 1000
            self.totalTimeUpdating = self.totalTimeUpdating + diffms
            self.totalUpdates = self.totalUpdates + 1
            logInfo('Update: %d, Time: %.2f, Average: %.2f' % (self.totalUpdates, diffms, self.totalTimeUpdating / self.totalUpdates))

    def updateFeatures(timeOfUpdate):
        for instrumentId in self.instrumentsDict:
            instrument = self.instrumentsDict[instrumentId]
            instrument.updateFeatures(timeOfUpdate)

    def startTrading(self):
        dataParser = self.tsParams.getDataParser()
        instrumentUpdates = dataParser.emitInstrumentUpdate()
        for instrumentUpdate in instrumentUpdates:
            self.processInstrumentUpdate(instrumentUpdate)
