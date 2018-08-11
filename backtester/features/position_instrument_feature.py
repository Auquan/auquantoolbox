from backtester.features.feature import Feature


class PositionInstrumentFeature(Feature):

   '''
   Computing for Instrument. By default defers to computeForLookbackData
   '''

   @classmethod
   def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
       instrumentsDict = instrumentManager.getAllInstrumentsByInstrumentId()
       if len(instrumentsDict) == 0:
           raise ValueError('instrumentDict is empty')
           print ("AAAAA")
           #logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
           return None
       positionDict = {}
       for instrumentId in instrumentsDict:
           positionDict[instrumentId] = instrumentManager.getInstrument(instrumentId).getCurrentPosition()
       return positionDict

