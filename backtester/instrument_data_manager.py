from backtester.instrumentUpdates.instrument_update import InstrumentUpdate
from backtester.constants import *


class InstrumentDataManager(object):
    '''
    '''
    def __init__(self, dataParser, features, instrumentIds):
        self.__cachedFolderName = dataParser._cachedFolderName
        self.__datasetId = dataParser._dataSetId
        self.__instrumentDataByFeature = {feature : None for feature in features}


    def addFeatureValueForAllInstruments(self, featureKey):
        pass

    def getInstrumentData(self, instrumentId):
        pass

    def getBookDataFeatures(self):
        return list(self.__bookData.columns)
