from sklearn import linear_model
from backtester.predefinedModels.model_template import Model
from backtester.constants import *
from backtester.logger import *


class LogisticRegression(Model):
    """
    Simple Losgistic Regression
    Useful params:
    - 'penalty' : string, specify the norm used in rehularization
    - 'nCPUs' : integer, number of CPU cores
    - 'tol' : float, tolerance
    - 'classWeight' : dict, individual weights of each class
    - 'multiClass' : string, multi class option 'ovr', 'multinomial'
    - 'sampleWeight' : numpy array, individual weights of each sample
    """
    def __init__(self, params):
        super(LogisticRegression, self).__init__(params)
        penalty = params.get('penalty', 'l2')
        tol = params.get('tol', 1e-4)
        classWeight = params.get('classWeight', None)
        multiClass = params.get('multiClass', 'ovr')
        nCPUs = params.get('nCPUs', -1)
        self._model = linear_model.LogisticRegression(penalty=penalty, tol=tol, class_weight=classWeight,
                                                      multi_class=multiClass, n_jobs=nCPUs)

    def fit(self, X, y):
        sampleWeight = self._params.get("sampleWeight", None)
        self._model.fit(X, y, sample_weight=sampleWeight)

    def reTrain(self, X, y):
        # same as fit in this case
        self.fit(X, y)

    def predict(self, X, withProbability=False):
        if withProbability:
            return self._model.predict(X), self._model.predict_proba(X)
        return self._model.predict(X)

    def evaluate(self, X, y):
        sampleWeight = self._params.get("sampleWeight", None)
        return self._model.score(X, y, sample_weight=sampleWeight)
