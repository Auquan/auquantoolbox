class Transformer(object):

    def __init__(self, params):
        self._params = params
        self._transformer = None

    def getTransformer(self):
        return self

    def partialTransform(self, dataManager):
        raise NotImplementedError
        return None

    def transform(self, dataManager):
        raise NotImplementedError
        return None

    def getTransformerAttributes(self):
        raise NotImplementedError
        return None
