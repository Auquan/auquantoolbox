
class Model(object):
    """
    Base class for a training model
    """
    def __init__(self, params):
        self._params = params
        self._model = None

    def fit(self, X, y):
        raise NotImplementedError

    def reTrain(self, X, y):
        raise NotImplementedError

    def predict(self, X):
        raise NotImplementedError

    def evaluate(self, X, y):
        raise NotImplementedError
