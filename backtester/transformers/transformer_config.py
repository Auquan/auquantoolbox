from backtester.configurator import Configurator
from backtester.transformers.transformer import Transformer
from backtester.logger import *
from backtester.transformers.standard_transform import StandardTransform
from backtester.transformers.minmax_transform import MinMaxTransform
from backtester.transformers.pca_transform import PCATransform


featureTransformationIdToClassDict = {'standard_transform' : StandardTransform,
                                      'minmax_transform' : MinMaxTransform,
                                      'pca_transform' : PCATransform
                                     }


class FeatureTransformationConfig(Configurator):
    """
    Configures feature transformation dicts
    """

    customIdToClassDict = {}

    def __init__(self, configDict):
        super(FeatureTransformationConfig, self).__init__()

        if 'featureTransformId' not in configDict:
            logError('featureTransformId missing in config dictionary %s', configDict['featureTransformKey'])
            # TODO:  Raise appropriate error
        self._identifier = configDict['featureTransformId']

        self._key = configDict.get('featureTransformKey', self._identifier)
        self._params = configDict.get('params', {})

    @classmethod
    def setupCustomFeatureTransformationMethods(cls, customIdToClass):
        FeatureTransformationConfig.customIdToClassDict.update(customIdToClass)

    @classmethod
    def getClassForFeatureTransformationId(cls, featureTransformId):
        if featureTransformId in FeatureTransformationConfig.customIdToClassDict:
            return FeatureTransformationConfig.customIdToClassDict[featureTransformId]
        return cls.getClassForId(featureTransformId, featureTransformationIdToClassDict, Transformer)
