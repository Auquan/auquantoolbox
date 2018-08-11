from sklearn.preprocessing import StandardScaler
from backtester.transformers.transformer import Transformer
from backtester.logger import *


class StandardTransform(Transformer):

    def __init__(self, params):
        super(StandardTransform, self).__init__(params)

    def transform(self, data):
        if self._transformer is None:
            withMean = self._params.get('with_mean', True)
            withStd = self._params.get('with_std', True)
            self._transformer = StandardScaler(with_mean=withMean, with_std=withStd)
            return self._transformer.fit_transform(data)
        return self._transformer.transform(data)

    def partialTransform(self, data):
        # TODO: Use partial_fit to fit and transform in chunks
        raise NotImplementedError

    def getTransformerAttributes(self):
        return {'scale' : self._transformer.scale_, 'mean' : self._transformer.mean_, 'var' : self._transformer.var_}
