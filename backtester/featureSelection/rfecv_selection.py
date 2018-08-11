from sklearn import feature_selection
from sklearn.feature_selection import RFECV
from sklearn.svm import SVR
from backtester.featureSelection.feature_selection import FeatureSelection
from backtester.logger import *
from backtester.featureSelection import supervised_learning_estimator

class RecursiveFeatureSelectWithCrossValidation(FeatureSelection):
    """
    ## USER GUIDE ##
    """

    ESTIMATOR = 'SVR'
    ESTIMATOR_PARAMS = {'kernel': 'linear'}
    STEP = 1
    CV = None
    SCORING = None
    N_JOBS = 1

    @classmethod
    def computeInteractionScore(cls, variableDf1, variableDf2):
        estimatorCls = getattr(supervised_learning_estimator, cls.ESTIMATOR)
        estimator = estimatorCls(**cls.ESTIMATOR_PARAMS)
        selector = RFECV(estimator, step=cls.STEP, cv=cls.CV, scoring=cls.SCORING, n_jobs=cls.N_JOBS)
        selector.fit(variableDf1, variableDf2)
        return selector.get_support(indices="True"), selector.ranking_, selector.grid_scores_

    @classmethod
    def extractImportantFeatures(cls, targetVariableKey, featureKeys, params, dataManager):
        cls.ESTIMATOR=params.get('estimator', cls.ESTIMATOR)
        cls.ESTIMATOR_PARAMS=params.get('estimator_params', cls.ESTIMATOR_PARAMS)
        cls.STEP=params.get('step', cls.STEP)
        cls.CV=params.get('cv', cls.CV)
        cls.SCORING=params.get('scoring', cls.SCORING)
        cls.N_JOBS=params.get('n_jobs', cls.N_JOBS)
        targetVariableDf = dataManager.getTargetVariableDf(targetVariableKey)
        featureDf = dataManager.getFeatureDf(featureKeys)
        featureIndices, ranking, grid_score = cls.computeInteractionScore(featureDf, targetVariableDf)
        return featureDf.columns[featureIndices].tolist()
