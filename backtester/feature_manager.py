from itertools import chain
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

    def getDataDf(self):
        pass

    def computeInstrumentFeatures(self):
        instrumentBookData = self.__dataParser.emitAllInstrumentUpdates()
        for bookDataFeature in self.__bookDataFeatures:
            featureDf = pd.concat([instrumentBookData[instrumentId].getBookDataByFeature(bookDataFeature) for instrumentId in instrumentBookData])
            self.__instrumentDataManger.addBookDataFeatureValueForAllInstruments(bookDataFeature, featureDf)

        # TODO: delete instrumentBookData to free memory

        featureConfigs = self.systemParams.getFeatureConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        # featureConfigKeys = [featureConfig.getFeatureKey() for featureConfig in featureConfigs]
        for instrumentDataChunk in instrumentDataGenerator:

        for featureConfig in featureConfigs:
            featureKey = featureConfig.getFeatureKey()
            featureParams = featureConfig.getFeatureParams()
            featureId = featureConfig.getFeatureId()
            featureCls = FeatureConfig.getClassForFeatureId(featureId)
            featureDf = featureCls.computeForInstrumentData(featureParams=featureParams,
                                                             featureKey=featureKey,
                                                             instrumentDataManager=self.__instrumentDataManger)
            self.__instrumentDataManger.addFeatureValueForAllInstruments(featureKey, featureDf)
