class Order:

    def __init__(self, instrumentId, tradePrice, vol, fees, time):
        self.instrumentId = instrumentId
        self.tradePrice = tradePrice
        self.volume = vol
        self.fees = fees
        self.time = time

    def isFuture(self):
        return "-" in self.instrumentId
