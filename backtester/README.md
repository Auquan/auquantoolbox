# **How it works?** #

## Trading System ##
The main system that runs your backtest. Raw data (tick or end of day data) for instruments are sent to the trading system. At every such update of data before updating the state of that instrument in the system, the trading system does the following things:
* Checks whether it is time to update the features and execute. It updates features at a frequency determined by trading parameters.  
* If it is, it first loops over all instruments and updates the features for each instrument (specified by trading parameters). Each instrument stores its features, which can be later extracted out.  
* Then, the trading system computes all the market features (specified by trading parameters). 
The system also stores such market features at every update features interval. 
One market feature which needs to be provided by the user is prediction which outputs the value of whatever we are planning to trade  
* Then the trading system looks at the prediction value and passed it to an execution system, 
whose job is to convert the prediction into possible positions to be taken for various instruments.  
* These are then passed into the orderPlacer, whose duty is try and place the order. 
It also reads confirmation of the orders which are placed (if they got placed) and updates with fees used for placing the orders. 
These change in position of instruments is relayed back to the instruments.  

## DataSource ##
Emits instrument updates into the trading system. Its job is to convert any sort of data from external sources to Instrument Updates. We have a different instrument update for each type of instrument.

## InstrumentFeatures ##
A Feature for the instrument. 

## MarketFeatures ##
A Feature for the market

## ExecutionSystem ##
Takes a prediction value and converts it into possible positions to be taken for each type of instrument. It takes into account current positions and confidence factor of the prediction.

## OrderPlacer ##
Manages placing and confirming of orders.

# **Glossary:** #

**Instrument:** An Asset to trade. Right now we support stocks, futures, and options
**InstrumentUpdate**: An update to an instrument.