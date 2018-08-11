from sklearn import feature_selection
from backtester.featureSelection.feature_selection import FeatureSelection
from backtester.logger import *

class GenericUnivariateSelect(FeatureSelection):
    """
    ## USER GUIDE ##
    Mode and their required params
    1. Mode = 'percentile' =>  param = float (default = 1e-05)
    2. Mode = 'fpr' (False positive rate) =>  param = float (default = 0.05)
    3. Mode = 'fdr' (False discovery rate) =>  param = float (default = 0.05)
    4. Mode = 'fwe' (Family-wise error rate) =>  param = float (default = 0.05)
    5. Mode = 'k_best' (Select best K) =>  param = int or 'all' (default = 'all')
    """

    # Defaults
    SCORE_FUNCTION = 'f_regression'
    MODE = 'k_best'
    MODE_PARAM = 'all'
    DEFAULT_MODE_PARAM_DICT = {'percentile' : 1e-05,
                               'k_best' : 'all',
                               'fpr' : 0.05,
                               'fdr' : 0.05,
                               'fwe' : 0.05}

    @classmethod
    def computeInteractionScore(cls, variableDf1, variableDf2):
        handler = getattr(feature_selection, cls.SCORE_FUNCTION)
        scoreFunction = feature_selection.GenericUnivariateSelect(handler, mode=cls.MODE, param=cls.MODE_PARAM)
        scoreFunction.fit(variableDf1, variableDf2)
        return scoreFunction.get_support(indices=True), scoreFunction.scores_, scoreFunction.pvalues_

    @classmethod
    def extractImportantFeatures(cls, targetVariableKey, featureKeys, params, dataManager):
        cls.SCORE_FUNCTION = params.get('scoreFunction', cls.SCORE_FUNCTION)
        cls.MODE = params.get('mode', cls.MODE)
        cls.MODE_PARAM = params.get('modeParam', cls.DEFAULT_MODE_PARAM_DICT[cls.MODE])
        targetVariableDf = dataManager.getTargetVariableDf(targetVariableKey)
        featureDf = dataManager.getFeatureDf(featureKeys)
        featureIndices, scores, pvalues = cls.computeInteractionScore(featureDf, targetVariableDf)
        # print(scores, pvalues)
        return featureDf.columns[featureIndices].tolist()
