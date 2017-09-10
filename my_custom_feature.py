from backtester.features.feature import Feature

'''
Use this class as a base if you want to make your own feature which you want to use in your strategy.
'''

class MyCustomFeature(Feature):

    '''
    Computing for Lookback data. Generic for instrument and market.
    IMPLEMENT THIS AND THIS ONLY IF YOUR FEATURE CAN BE USED BOTH AS A MARKET FEATURE AND INSTRUMENT FEATURE
    featureParams: A dictionary of parameter and parameter values your features computation might depend on.
                   You define the structure for this. just have to make sure these parameters are provided when
                   you wanted to actually use this feature in getMarketFeatureConfigDicts in TradingSystemParameters
    featureKey: Name of the key this will feature will be mapped against.
    currentFeatures: Dictionary with featurekey: featureValue of the (market or instrument) features which have been already calculated in this update
                     cycle. The features are computed sequentially in order of how they appear in your config.
    lookbackDataDf: Dataframe to hold lookback data for the features (could be either instrument or market features)
    '''
    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        raise NotImplementedError
        return None

    '''
    Computing for Instrument.
    IMPLEMENT THIS ONLY IF YOUR FEATURE CAN BE USED ONLY AS INSTRUMENT FEATURE
    IF YOUR FEATURE CAN BE BOTH MARKET OR INSTRUMENT, DO NOT IMPLEMENT THIS FUNCTION AT ALL. JUST IMPLEMENT computeForLookbackData
    '''
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):
        bookData = instrument.getCurrentBookData() # Current Book Data For the Instrument. This is the last update to the instrument
        instrumentType = instrument.getInstrumentType() # type of instrument: eg. INSTRUMENT_TYPE_STOCK, INSTRUMENT_TYPE_FUTURE
        param1Value = featureParams['param1'] # Custom parameter which can be used as input to computation of this feature
        lookbackInstrumentFeaturesDf = instrument.getDataDf() # dataframe for historical instrument features, 
                                                                            # columns will be featureKeys for different features
        return 0

    '''
    Computing for Market.
    IMPLEMENT THIS ONLY IF YOUR FEATURE CAN BE USED ONLY AS MARKET FEATURE
    IF YOUR FEATURE CAN BE BOTH MARKET OR INSTRUMENT, DO NOT IMPLEMENT THIS FUNCTION AT ALL. JUST IMPLEMENT computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        param1Value = featureParams['param1'] # Custom parameter which can be used as input to computation of this feature
        lookbackMarketFeaturesDf = instrumentManager.getDataDf() # dataframe for historical market features,
                                                                    # columns will be featureKeys for different features
        allInstruments = instrumentManager.getAllInstrumentsByInstrumentId() # Dictionary with keys as instrumentId, value as instrument
        # Way to loop over all instruments
        for instrumentId in allInstruments:
            instrument = allInstruments[instrumentId]
        specificInstrument = instrumentManager.getInstrument('instrumentId') # Way to get a specific instrument given instrument id.
        return 0
