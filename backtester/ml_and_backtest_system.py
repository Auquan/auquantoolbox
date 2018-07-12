import os
import numpy as np
try:        # Python 3.x
    import _pickle as pickle
except ImportError:
    try:    # Python 2.x
        import cPickle as pickle
    except ImportError:
        import pickle
from backtester.model_learning_system import ModelLearningSystem
from backtester.trading_system import TradingSystem
from backtester.features.feature import Feature

class MLandBacktestSystem(object):

    def __init__(self, tsParams, mlsParams):
        self.tsParams = tsParams
        self.mlsParams = mlsParams
        self.models = {}
        self.selectedFeatures = {}
        self.transformers = {}

    def trainAndBacktest(self):
        mlSystem = ModelLearningSystem(self.mlsParams, chunkSize=None)
        mlSystem.runModels()
        self.loadModels(self.tsParams.getTargetVariableKey())
        self.setUpMLSTrainingPredictionFeature()

        print('Loaded Problem 1 Params, Loading Backtester and Data')
        tradingSystem = TradingSystem(self.tsParams)
        print('Loaded Backtester and Data Loaded, Backtesting')
    # Set onlyAnalyze to True to quickly generate csv files with all the features
    # Set onlyAnalyze to False to run a full backtest
    # Set makeInstrumentCsvs to False to not make instrument specific csvs in runLogs. This improves the performance BY A LOT
        tradingSystem.startTrading(onlyAnalyze=False, shouldPlot=True, makeInstrumentCsvs=True)

    def loadModels(self, targetVariableKey):
        for instrumentId in self.mlsParams.getInstrumentIds():
            fileName = os.path.join(self.mlsParams.modelDir, instrumentId + '_' + targetVariableKey + '.pkl')
            with open(fileName, 'rb') as f:
                modelData = pickle.load(f)
                # Models which has methods - fit, predict, reTrain and evaluate
                self.models[instrumentId] = modelData.getModel()
                # selectFeatures is the list of important feature keys
                self.selectedFeatures[instrumentId] = modelData.getModelFeatures()
                # transformers is the ordered dictionary of scalers or transformers
                self.transformers[instrumentId] = modelData.getModelTransformers()

    def setUpMLSTrainingPredictionFeature(self):
        MLSTrainingPredictionFeature.SELECTED_FEATURES = self.selectedFeatures
        MLSTrainingPredictionFeature.TRANSFORMERS = self.transformers
        MLSTrainingPredictionFeature.MODELS = self.models

    def getPrediction(self, time, updateNum, instrumentManager, predictions):
        # holder for all the instrument features for all instruments
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()
        for instrumentId in self.mlsParams.getInstrumentIds():
            X = []
            for feature in self.selectedFeatures[instrumentId]:
                X.append(lookbackInstrumentFeatures.getFeatureDf(feature)[instrumentId].iloc[-1].values)
            X = np.array(X)
            X = self.transformData(instrumentId, X)
            predictions[instrumentId] = self.models[instrumentId].predict(X)
        return predictions

class MLSTrainingPredictionFeature(Feature):
    SELECTED_FEATURES = {}
    TRANSFORMERS = {}
    MODELS = {}

    @classmethod
    def transformData(cls, instrumentId, X):
        transformers = cls.TRANSFORMERS.get(instrumentId, None)
        if transformers is None:
            return X
        transformers = transformers.values if isinstance(transformers, dict) else transformers
        for transformer in transformers:
            X = transformer.transform(X)
        return X

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        predictions = pd.Series(0.5, index = instrumentManager.getAllInstrumentsByInstrumentId())
        # holder for all the instrument features for all instruments
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()
        for instrumentId in instrumentManager.getAllInstrumentsByInstrumentId():
            X = []
            for feature in cls.SELECTED_FEATURES[instrumentId]:
                X.append(lookbackInstrumentFeatures.getFeatureDf(feature)[instrumentId].iloc[-1].values)
            X = np.array(X)
            X = cls.transformData(instrumentId, X)
            predictions[instrumentId] = cls.MODELS[instrumentId].predict(X)
        return predictions
