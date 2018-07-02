
class Model(object):
    """
    Base class for a training model
    """
    def __init__(self, params):
        self._params = params
        self._model = None

    def fit(self, dataManager):
        raise NotImplementedError

    def reTrain(self, dataManager):
        raise NotImplementedError

    def predict(self, dataManager):
        raise NotImplementedError

    def evaluate(self, dataManager):
        raise NotImplementedError
