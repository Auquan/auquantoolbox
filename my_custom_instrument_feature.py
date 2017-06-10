from backtester.instrumentFeatures.instrument_feature import InstrumentFeature


class MyCustomInstrumentFeature(InstrumentFeature):

    @classmethod
    def validateInputs(cls, featureParams, currentFeatures, instrument):
        # Implement this if you want to check for inputs, whether this function can run.
        return True

    '''
    Computes the value of your feature.
    featureParams: A dictionary of parameter and parameter values your features computation might depend on.
                   You define the structure for this. just have to make sure these parameters are provided when
                   you wanted to actually use this feature in getInstrumentFeatureConfigDicts in TradingSystemParameters
    featureKey: Name of the key this will feature will be mapped against.
    currentFeatures: Dictionary with featurekey: featureValue of the features which have been already calculated in this update
                     cycle. The features are computed sequentially in order of how they appear in getInstrumentFeatureConfigDicts.
    instrument: The instrument for which we are computing the features for right now.
    '''
    @classmethod
    def compute(cls, featureParams, featureKey, currentFeatures, instrument):
        bookData = instrument.getCurrentBookData() # Current Book Data For the Instrument. This is the last update to the instrument
        instrumentType = instrument.getInstrumentType() # type of instrument: eg. INSTRUMENT_TYPE_STOCK, INSTRUMENT_TYPE_FUTURE
        param1Value = featureParams['param1'] # Custom parameter which can be used as input to computation of this feature
        lookbackInstrumentFeatures = instrument.getLookbackFeatures() # LookbackData: stores historical instrument features
        lookbackInstrumentFeaturesDf = lookbackInstrumentFeatures.getData() # dataframe for historical instrument features, 
                                                                            # columns will be featureKeys for different features
        return 0
