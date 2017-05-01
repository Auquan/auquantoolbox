import useful_fn as utils


class Future:

    def __init__(self, futureInstrument):
        self.date = futureInstrument.date
        self.time = futureInstrument.time
        self.futureSymbol = futureInstrument.instrumentId
        firstBookData = futureInstrument.bookData[0]
        self.futureVal = utils.get_vwap(firstBookData['bidVol'],
                                        firstBookData['bidPrice'],
                                        firstBookData['askPrice'],
                                        firstBookData['askVol'])
