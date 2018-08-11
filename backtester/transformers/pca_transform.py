from sklearn.decomposition import PCA
from backtester.transformers.transformer import Transformer
from backtester.logger import *


class PCATransform(Transformer):

    def __init__(self, params):
        super(PCATransform, self).__init__(params)

    def transform(self, data):
        if self._transformer is None:
            n_components = self._params.get('n_comp', None)
            copy = self._params.get('copy', True)
            whiten = self._params.get('whiten', False)
            svd_solver = self._params.get('svd', 'auto')
            iterated_power = self._params.get('itr_power', 'auto')
            random_state = self._params.get('random_state', None)
            self._transformer = PCA(n_components, copy, whiten, svd_solver, iterated_power, random_state)
            return self._transformer.fit_transform(data)
        return self._transformer.transform(data)

    def partialTransform(self, data):
        # TODO: Use partial_fit to fit and transform in chunks
        raise NotImplementedError

    def getTransformerAttributes(self):
        return {'mean' : self._transformer.mean_, 'explained_variance' : self._transformer.explained_variance_,
                'noise_variance' : self._transformer.noise_variance_, 'singular_values' : self._transformer.singular_values_}
