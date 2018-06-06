


class FeatureManager(object):
    """docstring FeatureManager ."""
    def __init__(self, systemParams, instrumentIds):
        self.systemParams = systemParams
        # self.__instrumentsDict = {}
        # instrumentFeatureConfigs = systemParams.getFeatureConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        # instrumentFeatureKeys = map(lambda x: x.getFeatureKey(), instrumentFeatureConfigs

    def getSystemParamas(self):
        return self.systemParams

    def getDataDf(self):
        pass

    def computeInstrumentFeatures(self, instrumentId, dataSource):
        instrumentDataDf = dataSource.emitAllInstrumentUpdates() # TODO: make it an iterator

        featureConfigs = self.systemParams.getFeatureConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        featureConfigKeys = [featureConfig.getFeatureKey() for featureConfig in featureConfigs]
        for featureConfig in featureConfigs:
            featureKey = featureConfig.getFeatureKey()
            featureId = featureConfig.getFeatureId()
            featureKey = featureConfig.getFeatureKey()
            featureParams = featureConfig.getFeatureParams()
            featureCls = FeatureConfig.getClassForFeatureId(featureId)
