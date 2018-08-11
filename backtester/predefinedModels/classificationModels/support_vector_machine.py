from sklearn import svm
from backtester.predefinedModels.model_template import Model
from backtester.constants import *
from backtester.logger import *

class SupportVectorMachine(Model):

    def __init__(self, params):
        super(SupportVectorMachine, self).__init__(params)
        C = params.get('C', 1.0)
        kernel = params.get('kernel', 'rbf')
        degree = params.get('degree', 3)
        gamma = params.get('gamma', 'auto')
        coef0 = params.get('coef0', 0.0)
        probability = params.get('probability', False)
        shrinking = params.get('shrinking', True)
        tol = params.get('tol', 1e-3)
        cache_size = params.get('cache_size', 200)
        class_weight = params.get('class_weight', 'balanced')
        max_iter = params.get('max_iter', -1)
        decision_function_shape = params.get('decision_function_shape', 'ovr')
        random_state = params.get('random_state', None)
        self._model = svm.SVC(kernel = kernel, degree = degree, gamma = gamma, coef0 = coef0, probability = probability,
                              shrinking = shrinking, tol = tol, cache_size = cache_size, class_weight = class_weight,
                              max_iter = max_iter, decision_function_shape = decision_function_shape,
                              random_state = random_state)

    def fit(self, X, y):
        sampleWeight = self._params.get('sampleWeight', None)
        self._model.fit(X, y, sample_weight=sampleWeight)

    def reTrain(self, X, y):
        # same as fit in this case
        self.fit(X, y)

    def predict(self, X, withProbability = False):
        if withProbability:
            return self._model.predict(X), self._model.predict_proba(X)
        return self._model.predict(X)

    def evaluate(self, X, y):
        sampleWeight = self._params.get('sampleWeight', None)
        return self._model.score(X, y, sample_weight=sampleWeight)
