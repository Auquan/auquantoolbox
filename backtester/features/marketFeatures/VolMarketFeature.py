from marketFeature import MarketFeature
import numpy as np


def shouldUpdateOption(opt, currentFutureVal):
        return (np.abs(opt.k - currentFutureVal) < 300)


def atm_vol(x, y, order):
    delta = 0.5
    if order == 2:
        p = np.polyfit(x, y, 1)
        atmvol = p[0] * delta + p[1]
    else:
        p = np.polyfit(x, y, 2)
        atmvol = p[0] * delta**2 + p[1] * delta + p[2]
    return atmvol


class VolMarketFeature(MarketFeature):

    def compute(self, evalTime, future, optionDict):
        delta_arr = []
        vol_arr = []
        for instrumentId in optionDict:
            opt = optionDict[instrumentId]
            if not shouldUpdateOption(opt, future.getFutureVal()):
                continue
            opt.get_price_delta()
            price, delta = opt.calc_price, opt.delta
            if abs(delta) < 0.75:
                if (delta < 0):
                    delta = 1 + delta
                delta_arr.append(delta)
                vol_arr.append(opt.vol)

        # Calculate ATM Vol
        if len(delta_arr) > 0:
            return atm_vol(delta_arr, vol_arr, 2)
        else:
            return 0
            # TODOMOD: Fix this
            # temp_df['Vol'] = lastMarketDataDf['Vol']