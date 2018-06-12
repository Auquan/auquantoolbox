from itertools import chain
import pandas as pd
import time, json
from datetime import timedelta
from backtester.features.feature_config import FeatureConfig
from backtester.instrument_data_manager import InstrumentDataManager
from backtester.constants import *
from backtester.logger import *


class FeatureManager(object):
    """
    """
    def __init__(self, systemParams, dataParser, chunkSize, fingerprintFile='stock_data'):
        self.systemParams = systemParams
        self.__dataParser = dataParser
        self.__chunkSize = chunkSize
        self.__fingerprintFile = fingerprintFile
        self.__bookDataFeatures = dataParser.getBookDataFeatures()
        instrumentFeatureConfigs = systemParams.getFeatureConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        instrumentFeatureKeys = map(lambda x: x.getFeatureKey(), instrumentFeatureConfigs)
        featureKeys = list(chain(self.__bookDataFeatures, instrumentFeatureKeys))
        maxPeriod = self.parseFeatureConfigs(instrumentFeatureConfigs)
        self.__instrumentDataManger = InstrumentDataManager(dataParser, featureKeys, systemParams.instrumentIds,
                                                            featureFolderName='features', lookbackSize=maxPeriod)
        self.__totalIter = 0
        self.__perfDict = {}
        for featureKey in featureKeys:
            self.__perfDict[featureKey] = 0

    def getSystemParamas(self):
        return self.systemParams

    def getInstrumentDf(self, instrumentId, useFile=True, chunkSize=None):
        return self.__instrumentDataManger.getInstrumentDataByInstrument(instrumentId, useFile, chunkSize)

    def getFeatureDf(self, featureKey):
        return self.__instrumentDataManger.getInstrumentDataChunkByFeature(featureKey)

    def parseFeatureConfigs(self, featureConfigList):
        maxPeriod = 0
        for featureConfig in featureConfigList:
            featureParams = featureConfig.getFeatureParams()
            maxPeriod = max(maxPeriod, featureParams.get('period', 0))
        if maxPeriod == 0:
            return None
        return maxPeriod

    def computeInstrumentFeatures(self, instrumentIds, writeFeatures=True):
        instrumentBookData = self.__dataParser.emitAllInstrumentUpdates()
        for bookDataFeature in self.__bookDataFeatures:
            featureDf = pd.concat([instrumentBookData[instrumentId].getBookDataByFeature(bookDataFeature) for instrumentId in instrumentIds], axis=1)
            featureDf.columns = instrumentIds
            self.__instrumentDataManger.addFeatureValueForAllInstruments(bookDataFeature, featureDf)

        # NOTE: copy in pd.concat is set to True. Check what happens when it is False

        featureConfigs = self.systemParams.getFeatureConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        featureGenerator = self.__instrumentDataManger.getSimulator(self.__chunkSize)
        for chunkNumber, timeUpdates in featureGenerator:
            self.__totalIter = self.__totalIter + 1
            for bookDataFeature in self.__bookDataFeatures:
                self.__instrumentDataManger.updateInstrumentDataChunk(bookDataFeature)
            for featureConfig in featureConfigs:
                start = time.time()
                featureKey = featureConfig.getFeatureKey()
                featureParams = featureConfig.getFeatureParams()
                featureId = featureConfig.getFeatureId()
                featureCls = FeatureConfig.getClassForFeatureId(featureId)
                featureDf = featureCls.computeForInstrumentData(updateNum=chunkNumber,
                                                                featureParams=featureParams,
                                                                featureKey=featureKey,
                                                                featureManager=self)
                self.__instrumentDataManger.addFeatureValueChunkForAllInstruments(featureKey, featureDf)
                end = time.time()
                diffms = (end - start) * 1000
                self.__perfDict[featureKey] = self.__perfDict[featureKey] + diffms
                logPerf('Avg time for feature: %s : %.2f' % (featureKey, self.__perfDict[featureKey] / self.__totalIter))
            self.__instrumentDataManger.transformInstrumentData()
            if writeFeatures:
                self.__instrumentDataManger.writeInstrumentData()
            self.__instrumentDataManger.dumpInstrumentDataChunk()
        if not self.__instrumentDataManger.checkDataIntegrity(chunkNumber):
            logWarn("Some data is missing! Check logs")
        if self.__chunkSize is None:
            self.__instrumentDataManger.cleanup()
        else:
            self.__instrumentDataManger.cleanup(delInstrumentData=True)
        self.__instrumentDataManger.saveInstrumentDataFingerprint(self.__fingerprintFile)
