from backtester.logger import *

class Configurator(object):
    """
    Base class to configure dicts
    """
    def __init__(self):
        self._identifier = None
        self._key = None
        self._params = None

    def getKey(self):
        return self._key

    def getId(self):
        return self._identifier

    def getParams(self):
        return self._params

    @classmethod
    def getClassForId(cls, identifier, idToClassDict, defaultClass):
        if identifier in idToClassDict:
            return idToClassDict[identifier]
        logError('%s not a valid feature Id. Use a predefined one or provide a custom implementation' % identifier)
        return defaultClass
