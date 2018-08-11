class Transformer(object):

    def __init__(self, params):
        self._params = params
        self._transformer = None

    def getTransformer(self):
        return self

    def partialTransform(self, data):
        raise NotImplementedError
        return None

    def transform(self, data):
        raise NotImplementedError
        return None

    def getTransformerAttributes(self):
        raise NotImplementedError
        return None
