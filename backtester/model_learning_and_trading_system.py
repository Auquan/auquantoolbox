import os
try:        # Python 3.x
    import _pickle as pickle
except ImportError:
    try:    # Python 2.x
        import cPickle as pickle
    except ImportError:
        import pickle
from backtester.model_learning_system import ModelLearningSystem
from backtester.trading_system import TradingSystem
from backtester.model_learning_system_parameters import MLSTrainingPredictionFeature

class MLandTradingSystem(object):

    def __init__(self, tsParams, mlsParams):
        self.tsParams = tsParams
        self.mlsParams = mlsParams
        self.models = {}
        self.selectedFeatures = {}
        self.transformers = {}

    def trainAndBacktest(self, chunkSize=None, onlyAnalyze=False, shouldPlot=True, makeInstrumentCsvs=True, useTargetVaribleFromFile=True, useTimeFrequency=True):
        print('Loading ModelLearningSystem')
        mlSystem = ModelLearningSystem(self.mlsParams, chunkSize=None)
        print('ModelLearningSystem Loaded, Training Model...')
        mlSystem.runModels(useTargetVaribleFromFile, useTimeFrequency)
        print('Model Trained, Modifying TS Params')
        # Change start and end date in tsParams
        # Backtester will run the trading system only in between these dates
        print('Setting Dates in TS Params')
        self.tsParams.setDates({'startDate':self.mlsParams.startDateStr['test'], 'endDate':self.mlsParams.endDateStr['test']})

        # NOTE: Selecting the first target variable key only as trading system doesn't support multiple target variable keys
        self.loadModels(self.mlsParams.getTargetVariableKeys()[0])
        self.setUpMLSTrainingPredictionFeature()

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
