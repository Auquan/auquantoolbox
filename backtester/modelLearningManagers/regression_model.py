import pandas as pd
try:        # Python 3.x
    import _pickle as pickle
except ImportError:
    try:    # Python 2.x
        import cPickle as pickle
    except ImportError:
        import pickle
from backtester.modelLearningManagers.training_model_manager import TrainingModelManager
from backtester.constants import *
from backtester.logger import *

class RegressionModel(TrainingModelManager):
    """
    """
    def __init__(self, systemParams):
        super(RegressionModel, self).__init__(systemParams)

    def getMetrics(self):
        raise NotImplementedError
