from sklearn.preprocessing import MinMaxScaler
from backtester.transformers.transformer import Transformer
from backtester.logger import *


class MinMaxTransform(Transform):

    def __init__(self, params):
        super(MinMaxTransform, self).__init__(params)

    def transform(self, dataManager):
        if self._transformer is None:
            lowerBound = self._params.get('low', 0)
            upperBound = self._params.get('high', 1)
            self._transformer = StandardScaler(with_mean=(lowerBound, upperBound))
            return self._transformer.fit_transform(dataManager.getInstrumentData())
        self._transformer.transform(dataManager.getInstrumentData())

    def partialTransform(self, dataManager):
        # TODO: Use partial_fit to fit and transform in chunks
        raise NotImplementedError

    def getTransformerAttributes(self):
        return {'scale' : self._transformer.scale_, 'min' : self._transformer.min_, 'data_range' : self._transformer.data_range_}
