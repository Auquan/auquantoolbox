from sklearn import neural_network
from backtester.predefinedModels.model_template import Model
from backtester.constants import *
from backtester.logger import *

class MultiLayerPerceptronClassification(Model):

    def __init__(self, params):
        super(MultiLayerPerceptronClassification, self).__init__(params)
        hidden_layer_sizes = params.get('hidden_layer_sizes', (100,))
        activation = params.get('activation', 'relu')
        solver = params.get('solver', 'adam')
        alpha = params.get('alpha', 0.0001)
        learning_rate = params.get('learning_rate', 'constant')
        learning_rate_init = params.get('learning_rate_init', 0.001)
        power_t = params.get('power_t', 0.5)
        max_iter = params.get('max_iter', 200)
        shuffle = params.get('shuffle', True)
        random_state = params.get('random_state', None)
        tol = params.get('tol', 1e-4)
        warm_start = params.get('warm_start', False)
        momentum = params.get('momentum', 0.9)
        nesterovs_momentum = params.get('nesterovs_momentum', True)
        early_stopping = params.get('early_stopping', False)
        validation_fraction = params.get('validation_fraction', 0.1)
        beta_1 = params.get('beta_1', 0.9)
        beta_2 = params.get('beta_2', 0.999)
        epsilon = params.get('epsilon', 1e-8)
        self._model = neural_network.MLPClassifier(hidden_layer_sizes = hidden_layer_sizes,
                                                   activation = activation, solver = solver, alpha = alpha,
                                                   learning_rate = learning_rate,
                                                   learning_rate_init = learning_rate_init, power_t = power_t, max_iter = max_iter,
                                                   shuffle = shuffle, random_state = random_state, tol = tol,
                                                   warm_start = warm_start, momentum = momentum, nesterovs_momentum = nesterovs_momentum,
                                                   early_stopping = early_stopping, validation_fraction = validation_fraction,
                                                   beta_1 = beta_1, beta_2 = beta_2, epsilon = epsilon)

    def fit(self, X, y):
        self._model.fit(X, y)

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
