import pandas as pd
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
        self.model = {}
        self.selectedFeatures = {}
        self.transformers = {}

    def trainAndBacktest(self,chunkSize=None, onlyAnalyze=False, shouldPlot=True, makeInstrumentCsvs=True):
        print('Loading ModelLearningSystem')
        mlSystem = ModelLearningSystem(self.mlsParams, chunkSize=chunkSize)
        print('ModelLearningSystem Loaded, Training Model')
        mlSystem.runModels()
        print('Model Trained, Modifying TS Params')

        # Change start and end date in tsParams
        # Backtester will run the trading system only in between these dates
        print('Setting Dates in TS Params')
        self.tsParams.setDates({'startDate':self.mlsParams.startDateStr['test'], 'endDate':self.mlsParams.endDateStr['test']})

        self.featureTransformationManager = mlSystem.getFeatureTransformationManager()
        self.trainingModelManager = mlSystem.getTrainingModelManager()
        self.loadModels(self.tradingFunction.getTargetVariableKey) ## THIS Should come from mlsParams
        self.tsParams.setAdditionalCustomFeatures({'prediction': MLSTrainingPredictionFeature})
        
        print('Loaded Configs, Loading Backtester and Data')
        tradingSystem = TradingSystem(self.tsParams)
        print('Loaded Backtester and Data Loaded, Backtesting')
    # Set onlyAnalyze to True to quickly generate csv files with all the features
    # Set onlyAnalyze to False to run a full backtest
    # Set makeInstrumentCsvs to False to not make instrument specific csvs in runLogs. This improves the performance BY A LOT
        tradingSystem.startTrading(onlyAnalyze=onlyAnalyze, shouldPlot=shouldPlot, makeInstrumentCsvs=makeInstrumentCsvs)

    def loadModels(self, targetVariableKey):
        for instrumentId in self.mlsParams.getInstrumentIds():
            fileName = os.path.join(self.mlsParams.modelDir, instrumentId + '_' + targetVariableKey + '.pkl')
            with open(fileName, 'rb') as f:
                modelData = pickle.load(f)
                # Model which has methods - fit, predict, reTrain and evaluate
                self.model[instrumentId] = modelData.getModel()
                # selectFeatures is the list of important feature keys
                self.selectedFeatures[instrumentId] = modelData.getModelFeatures()
                # transformers is the ordered dictionary of scalers or transformers
                self.transformers[instrumentId] = modelData.getModelTransformers()
            self.trainingModelManager.addModel(self.model[instrumentId], instrumentId)


    def getPrediction(self, time, updateNum, instrumentManager, predictions):
        # holder for all the instrument features for all instruments
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()
        for instrumentId in self.mlsParams.getInstrumentIds():
            X = []
            for feature in self.selectedFeatures[instrumentId]:
                X.append(lookbackInstrumentFeatures.getFeatureDf(feature)[instrumentId].iloc[-1].values)
            X = np.array(X)
            self.featureTransformationManager.transformFeaturesUsingTransformers(X, self.transformers[instrumentId])
            X = self.featureTransformationManager.getTransformedData()
            predictions[instrumentId] = self.trainingModelManager.predict(X, instrumentId)[instrumentId]
        return predictions


class MLSTrainingPredictionFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        tf = featureParams['function']
        predictions = pd.Series(0.5, index = instrumentManager.getAllInstrumentsByInstrumentId())
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()
        for instrumentId in MLandBacktestSystem.mlsParams.getInstrumentIds():
            X = []
            for feature in MLandBacktestSystem.selectedFeatures[instrumentId]:
                X.append(lookbackInstrumentFeatures.getFeatureDf(feature)[instrumentId].iloc[-1].values)
            X = np.array(X)
            MLandBacktestSystem.featureTransformationManager.transformFeaturesUsingTransformers(X, self.transformers[instrumentId])
            X = MLandBacktestSystem.featureTransformationManager.getTransformedData()
            predictions[instrumentId] = MLandBacktestSystem.trainingModelManager.predict(X, instrumentId)[instrumentId]
        return predictions
