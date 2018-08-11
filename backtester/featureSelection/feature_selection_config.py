from backtester.configurator import Configurator
from backtester.featureSelection.feature_selection import FeatureSelection
from backtester.logger import *
from backtester.featureSelection.correlation import PearsonCorrelation
from backtester.featureSelection.generic_univariate_select import GenericUnivariateSelect
from backtester.featureSelection.rfecv_selection import RecursiveFeatureSelectWithCrossValidation


featureSelectionIdToClassDict = {'pearson_correlation' : PearsonCorrelation,
                                 'generic_univariate_select' : GenericUnivariateSelect,
                                 'rfecv_selection' : RecursiveFeatureSelectWithCrossValidation
                                }


class FeatureSelectionConfig(Configurator):
    """
    Configures feature selection dicts
    """

    customIdToClassDict = {}

    def __init__(self, configDict):
        super(FeatureSelectionConfig, self).__init__()

        if 'featureSelectionId' not in configDict:
            logError('featureSelectionId missing in config dictionary %s', configDict['featureSelectionKey'])
            # TODO:  Raise appropriate error
        self._identifier = configDict['featureSelectionId']

        self._key = configDict.get('featureSelectionKey', self._identifier)
        self._params = configDict.get('params', {})

    @classmethod
    def setupCustomFeatureSelectionMethods(cls, customIdToClass):
        FeatureSelectionConfig.customIdToClassDict.update(customIdToClass)

    @classmethod
    def getClassForFeatureSelectonId(cls, featureSelectionId):
        if featureSelectionId in FeatureSelectionConfig.customIdToClassDict:
            return FeatureSelectionConfig.customIdToClassDict[featureSelectionId]
        return cls.getClassForId(featureSelectionId, featureSelectionIdToClassDict, FeatureSelection)
