from itertools import chain
import time
from backtester.features.feature_config import FeatureConfig
from backtester.instrument_data_manager import InstrumentDataManager


class FeatureManager(object):
    """
    """
    def __init__(self, systemParams, dataParser, chunkSize):
        self.systemParams = systemParams
        self.__dataParser = dataParser
        self.__chunkSize = chunkSize
        self.__bookDataFeatures = dataParser.getBookDataFeatures()
        instrumentFeatureConfigs = systemParams.getFeatureConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        instrumentFeatureKeys = map(lambda x: x.getFeatureKey(), instrumentFeatureConfigs)
        featureKeys = list(chain(self.__bookDataFeatures, instrumentFeatureKeys))
        self.__instrumentDataManger = InstrumentDataManager(dataParser, featureKeys, instrumentIds)

        self.__totalIter = 0
        self.__perfDict = {}
        for featureKey in featureKeys:
            self.__perfDict[featureKey] = 0

    def getSystemParamas(self):
        return self.systemParams

    def getInstrumentDf(self, instrumentId):
        return self.__instrumentDataManger.getInstrumentDataByInstrument(instrumentId)

    def getFeatureDf(self, featureKey):
        return self.__instrumentDataManger.getInstrumentDataChunkByFeature(featureKey)

    def computeInstrumentFeatures(self, writeFeatures=True):
        instrumentBookData = self.__dataParser.emitAllInstrumentUpdates()
        instrumentIds = self.__dataParser.getInstrumentIds()
        for bookDataFeature in self.__bookDataFeatures:
            featureDf = pd.concat([instrumentBookData[instrumentId].getBookDataByFeature(bookDataFeature) for instrumentId in instrumentIds], axis=1)
            featureDf.columns = instrumentIds
            self.__instrumentDataManger.addFeatureValueForAllInstruments(bookDataFeature, featureDf)

        # NOTE: copy in pd.concat is set to True. Check what happens when it is False

        featureConfigs = self.systemParams.getFeatureConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        # featureConfigKeys = [featureConfig.getFeatureKey() for featureConfig in featureConfigs]
        featureGenerator = self.__instrumentDataManger.getSimulator(self.__chunkSize)
        for chunkNumber, timeUpdates in featureGenerator:
            self.__totalIter = self.__totalIter + 1
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
                self.__instrumentDataManger.addFeatureValueForAllInstruments(featureKey, featureDf)
                end = time.time()
                diffms = (end - start) * 1000
                self.__perfDict[featureKey] = self.__perfDict[featureKey] + diffms
                logPerf('Avg time for feature: %s : %.2f' % (featureKey, self.__perfDict[featureKey] / self.__totalIter))
            self.__instrumentDataManger.transformInstrumentData()
            if writeFeatures:
                self.__instrumentDataManger.writeInstrumentData()
            self.__instrumentDataManger.dumpInstrumentDataChunk()
