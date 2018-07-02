from sklearn import linear_model
from backtester.predefinedModels.model_template import Model
from backtester.constants import *
from backtester.logger import *


class LinearRegression(Model):
    """
    Simple least squares Linear Regression
    Useful params:
    - 'normalize' : boolean, normalizes the input data if set to True during fit
    - 'nCPUs' : integer, number of CPU cores
    - 'sampleWeight' : numpy array, individual weights of each sample
    """
    def __init__(self, params):
        super(LinearRegression, self).__init__(params)
        normalize = params.get('normalize', False)
        nCPUs = params.get('nCPUs', -1)
        self._model = linear_model.LinearRegression(normalize=normalize, n_jobs=nCPUs)

    def fit(self, dataManager):
        sampleWeight = self._params.get("sampleWeight", None)
        features = dataManager.getFeaures()
        targetVariable = dataManager.getTargetVariable()
        self._model.fit(features, targetVariable, sample_weight=sampleWeight)

    def reTrain(self, dataManager):
        # same as fit in this case
        self.fit(dataManager)

    def predict(self, dataManager):
        features = dataManager.getFeaures()
        return self._model.predict(features)

    def evaluate(self, dataManager):
        sampleWeight = self._params.get("sampleWeight", None)
        features = dataManager.getFeaures()
        targetVariable = dataManager.getTargetVariable()
        return self._model.score(features, targetVariable, sample_weight=sampleWeight)
