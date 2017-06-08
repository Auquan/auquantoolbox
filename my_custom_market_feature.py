from backtester.marketFeatures.market_feature import MarketFeature


class MyCustomMarketFeature(MarketFeature):

    @classmethod
    def validateInputs(cls, featureParams, currentMarketFeatures, instrumentManager):
        # Implement this if you want to check for inputs, whether this function can run.
        return True

    '''
    Computes the value of your feature.
    featureParams: A dictionary of parameter and parameter values your features computation might depend on.
                   You define the structure for this. just have to make sure these parameters are provided when
                   you wanted to actually use this feature in getMarketFeatureConfigDicts in TradingSystemParameters
    featureKey: Name of the key this will feature will be mapped against.
    currentMarketFeatures: Dictionary with featurekey: featureValue of the features which have been already calculated in this update
                           cycle. The features are computed sequentially in order of how they appear in getMarketFeatureConfigDicts.
    instrumentManager: Holder for all the instruments
    '''
    @classmethod
    def compute(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        param1Value = featureParams['param1'] # Custom parameter which can be used as input to computation of this feature
        lookbackMarketFeatures = instrumentManager.getLookbackMarketFeatures() # LookbackData: stores historical market features
        lookbackMarketFeaturesDf = lookbackMarketFeatures.getData() # dataframe for historical market features,
                                                                    # columns will be featureKeys for different features
        allInstruments = instrumentManager.getAllInstrumentsByInstrumentId() # Dictionary with keys as instrumentId, value as instrument
        # Way to loop over all instruments
        for instrumentId in allInstruments:
            instrument = allInstruments[instrumentId]
        specificInstrument = instrumentManager.getInstrument('instrumentId') # Way to get a specific instrument given instrument id.
        return 0
