import pandas as pd
from backtester.modelLearningManagers.training_model_manager import TrainingModelManager
from backtester.constants import *
from backtester.logger import *

class ClassificationModel(TrainingModelManager):
    """
    """
    def __init__(self, systemParams):
        super(ClassificationModel, self).__init__(systemParams)

    def getMetrics(self):
        raise NotImplementedError
