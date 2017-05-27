from marketFeature import MarketFeature


class FutureMarketFeature(MarketFeature):

    def compute(self, evalTime, future, optionDict):
        return future.getFutureVal()
