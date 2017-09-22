from backtester.features.feature import Feature
from backtester.financial_fn import ma


class RSIFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getDataForFeatureForAllInstruments(featureParams['featureName'])
        data_upside = data.sub(data.shift(1), fill_value=0)
        data_downside = data_upside.copy()
        data_downside[data_upside > 0] = 0
        data_upside[data_upside < 0] = 0
        avg_upside = ma(data_upside, featureParams['period'])[-1]
        avg_downside = - ma(data_downside, featureParams['period'])[-1]
        rs = avg_upside / avg_downside

        return 100 - (100 * avg_downside / (avg_downside + avg_upside))

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        data_upside = data.sub(data.shift(1), fill_value=0)
        data_downside = data_upside.copy()
        data_downside[data_upside > 0] = 0
        data_upside[data_upside < 0] = 0
        if len(data.index) > 0:
            avg_upside = ma(data_upside, featureParams['period'])[-1]
            avg_downside = - ma(data_downside, featureParams['period'])[-1]
            rs = avg_upside / avg_downside
        else:
            return 0

        return 100 - (100 * avg_downside / (avg_downside + avg_upside))
