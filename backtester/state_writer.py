import csv
import os
import sys


class StateWriter:

    def __init__(self, parentFolderName, runName, onlyMarket=False):
        self.__runName = runName
        if not os.path.exists(parentFolderName):
            os.mkdir(parentFolderName, 0o755)
        self.__folderName = parentFolderName + '/' + 'runLog_' + runName
        if not os.path.exists(self.__folderName):
            os.mkdir(self.__folderName, 0o755)
        self.__openFiles = []
        self.__marketFeaturesFilename = None
        self.__marketFeaturesWriter = None
        self.__predictionFeaturesFilename = None
        self.__predictionFeaturesWriter = None
        self.__instrumentIdToWriters = {}
        self.__onlyMarket = onlyMarket

    def getMarketFeaturesFilename(self):
        return self.__marketFeaturesFilename

    def getFolderName(self):
        return self.__folderName

    def closeStateWriter(self):
        for file in self.__openFiles:
            file.close()

    def writeColumns(self, writer, df):
        featureKeys = list(df.columns)
        toSaveColumns = ['time'] + featureKeys
        writer.writerow(toSaveColumns)

    def writePredictionColumns(self, writer, list):
        toSaveColumns = ['time'] + list
        writer.writerow(toSaveColumns)

    def writeLastFeatures(self, writer, df):
        if len(df) == 0:
            return
        lastFeatures = df.iloc[-1]
        timeOfUpdate = lastFeatures.name
        featureValues = lastFeatures.values
        toSaveRow = [timeOfUpdate] + list(featureValues)
        writer.writerow(toSaveRow)

    def writeInstrumentColumns(self, writer, instrumentId, instrumentLookbackData):
        featureKeys = instrumentLookbackData.getInstrumentFeatures()
        toSaveColumns = ['time'] + featureKeys
        writer.writerow(toSaveColumns)

    def writeLastInstrumentFeatures(self, time, writer, instrumentId, instrumentLookbackData):
        toSaveRow = [time]
        for featureKey in instrumentLookbackData.getInstrumentFeatures():
            featureDataDf = instrumentLookbackData.getFeatureDf(featureKey)
            lastInstrumentFeature = featureDataDf[instrumentId].iloc[-1]
            toSaveRow.append(lastInstrumentFeature)
        writer.writerow(toSaveRow)

    def writeCurrentState(self, time, instrumentManager):
        marketFeaturesDf = instrumentManager.getDataDf()
        if self.__marketFeaturesWriter is None:
            self.__marketFeaturesFilename = self.__folderName + '/marketFeatures.csv'
            if sys.version_info >= (3,):
                marketFeaturesFile = open(self.__marketFeaturesFilename, 'w', encoding='utf8', newline='')
            else:
                marketFeaturesFile = open(self.__marketFeaturesFilename, 'wb')
            self.__openFiles.append(marketFeaturesFile)
            self.__marketFeaturesWriter = csv.writer(marketFeaturesFile)
            self.writeColumns(self.__marketFeaturesWriter, marketFeaturesDf)
        self.writeLastFeatures(self.__marketFeaturesWriter, marketFeaturesDf)

        instrumentsDict = instrumentManager.getAllInstrumentsByInstrumentId()
        b = []
        for instrumentId in instrumentsDict:
            b.append(instrumentId)

        if self.__predictionFeaturesWriter is None:
            self.__predictionFeaturesFilename = self.__folderName + '/predictions.csv'
            if sys.version_info >= (3,):
                predictionFeaturesFile = open(self.__predictionFeaturesFilename, 'w', encoding='utf8', newline='')
            else:
                predictionFeaturesFile = open(self.__predictionFeaturesFilename, 'wb')
            self.__openFiles.append(predictionFeaturesFile)
            self.__predictionFeaturesWriter = csv.writer(predictionFeaturesFile)
            self.writePredictionColumns(self.__predictionFeaturesWriter, b)

        if self.__onlyMarket:
            return

        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        toSavePredictionRow = [time]
        for instrumentId in instrumentsDict:
            if instrumentId not in self.__instrumentIdToWriters:
                instrumentFeaturesFilename = self.__folderName + '/' + instrumentId + '_features.csv'
                if sys.version_info >= (3,):
                    instrumentFeaturesFile = open(instrumentFeaturesFilename, 'w', encoding='utf8', newline='')
                else:
                    instrumentFeaturesFile = open(instrumentFeaturesFilename, 'wb')
                self.__openFiles.append(instrumentFeaturesFile)
                self.__instrumentIdToWriters[instrumentId] = csv.writer(instrumentFeaturesFile)
                self.writeInstrumentColumns(self.__instrumentIdToWriters[instrumentId], instrumentId, instrumentLookbackData)
            instrumentFeaturesWriter = self.__instrumentIdToWriters[instrumentId]
            self.writeLastInstrumentFeatures(time, instrumentFeaturesWriter, instrumentId, instrumentLookbackData)
            featureDataDf = instrumentLookbackData.getFeatureDf('prediction')
            lastPrediction = featureDataDf[instrumentId].iloc[-1]
            toSavePredictionRow.append(lastPrediction)
        self.__predictionFeaturesWriter.writerow(toSavePredictionRow)
