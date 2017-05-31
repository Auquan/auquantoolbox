class InstrumentFeatureConfig:

    def __init__(self, configDict):
        # TODO: validate
        self.__featureKey = configDict['featureKey']
        self.__featureIdentifier = configDict['featureId']
        self.__featureParams = configDict['params']

    def getFeatureKey(self):
        return self.__featureKey

    def getFeatureId(self):
        return self.__featureIdentifier

    def getFeatureParams(self):
        return self.__featureParams
