# **Quick Startup Guide** #
Override the different functions according to your need in my_trading_params.py and run
python my_trading_params.py.
If you want to supply different trading params, create a new class that inherits from TradingSystemParameters.py

# **How it works?** #

## Trading System ##
The main system that runs your backtest. Raw data (tick or end of day data) for instruments are sent to the trading system. At every such update of data, the trading system does the following things:
* Checks whether it is time to update the features and execute. It updates features at a frequency determined by trading parameters.
* If it is, it first loops over all instruments and updates the features for each instrument (specified by trading parameters). Each instrument stores its features, which can be later extracted out.
* Then, the trading system computes all the market features (specified by trading parameters). The system also stores such market features at every update features interval.
* After this, 

## DataSource ##

## InstrumentFeatures ##

## MarketFeatures ##

## ExecutionSystem ##

## OrderPlacer ##


# **Glossary:** #

**Instrument:** An Asset to trade. Right now we support stocks, futures, and options
**InstrumentUpdate**: An update to an instrument.