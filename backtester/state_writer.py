import csv
import os

class StateWriter:

    def __init__(self, parentFolderName, runName):
        self.__runName = runName
        if not os.path.exists(parentFolderName):
            os.mkdir(parentFolderName, 0o755)
        self.__folderName = parentFolderName + '/' + 'runLog_' + runName
        if not os.path.exists(self.__folderName):
            os.mkdir(self.__folderName, 0o755)
        self.__openFiles = []
        self.__marketFeaturesFilename = None
        self.__marketFeaturesWriter = None
        self.__instrumentIdToWriters = {}

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

    def writeLastFeatures(self, writer, df):
        lastFeatures = df.iloc[-1]
        timeOfUpdate = lastFeatures.name
        featureValues = lastFeatures.values
        toSaveRow = [timeOfUpdate] + list(featureValues)
        writer.writerow(toSaveRow)

    def writeCurrentState(self, instrumentManager):
        marketFeaturesDf = instrumentManager.getDataDf()
        if self.__marketFeaturesWriter is None:
            self.__marketFeaturesFilename = self.__folderName + '/marketFeatures.csv'
            marketFeaturesFile =  open(self.__marketFeaturesFilename, 'wb')
            self.__openFiles.append(marketFeaturesFile)
            self.__marketFeaturesWriter = csv.writer(marketFeaturesFile)
            self.writeColumns(self.__marketFeaturesWriter, marketFeaturesDf)
        self.writeLastFeatures(self.__marketFeaturesWriter, marketFeaturesDf)
        instrumentsDict = instrumentManager.getAllInstrumentsByInstrumentId()
        for instrumentId in instrumentsDict:
            instrument = instrumentsDict[instrumentId]
            instrumentFeaturesDf = instrument.getDataDf()
            if instrumentId not in self.__instrumentIdToWriters:
                instrumentFeaturesFilename = self.__folderName + '/' + instrumentId + '_features.csv'
                instrumentFeaturesFile = open(instrumentFeaturesFilename, 'wb')
                self.__openFiles.append(instrumentFeaturesFile) 
                self.__instrumentIdToWriters[instrumentId] = csv.writer(instrumentFeaturesFile)
                self.writeColumns(self.__instrumentIdToWriters[instrumentId], instrumentFeaturesDf)
            instrumentFeaturesWriter = self.__instrumentIdToWriters[instrumentId]
            self.writeLastFeatures(instrumentFeaturesWriter, instrumentFeaturesDf)
