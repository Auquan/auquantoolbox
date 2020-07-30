**Note**: This the documentation for the current version toolbox released by Auquan. The old, stripped down version (installed as auquanToolbox, has been deprecated). [You can see the current toolbox repository here](https://links.auquan.com/auquantoolbox) - if you face any bugs, please open an issue on the github repository or email us at: toolbox@auquan.com

**Welcome to Auquan Toolbox**

[Auquan](http://www.auquan.com) provides a backtesting toolbox to develop your trading algorithms. The toolbox is free and open source which you can use to create and backtest strategies.

**Table of Contents**

[TOC]

# **Demo Video** #
You can watch a [quick video demo]((https://www.youtube.com/watch?v=YHdb8w3oRw0)) for the toolbox below

[![Alt text](https://i.ytimg.com/vi/IMtqDzZoiNk/hqdefault.jpg)](https://www.youtube.com/embed/YHdb8w3oRw0)

# **Installation Guide** #

1. Install Python and dependent packages  
Our toolbox is compatible with both Python 2.7( there are currently some issues with Python 3, we'll fix them shortly). The easiest way to install Python is through Anaconda since it will reliably install all the necessary dependencies. Download [Anaconda](http://continuum.io/downloads) and follow the instructions on the [installation page](http://docs.continuum.io/anaconda/install).   Once you have Python, you can then install the toolbox.

2. Get the Auquan Toolbox
    There are multiple ways to install the toolbox for the competition.
    * **Via pip**: The easiest way and the most recommended way is via pip. Just run the following command: `pip install -U auquan_toolbox`. If we publish any updates to the toolbox, the same command `pip install -U auquan_toolbox` will also automatically get the new version of the toolbox. **Note: Mac users**, if you face any issues with installation, try using `pip install --user auquan_toolbox`  
    * **Via git**: Clone/Download this repository.

        git clone https://{your_username}@bitbucket.org/auquan/auquantoolbox.git

3. Download [this sample file](https://links.auquan.com/sampleParams) and navigate to the place where you downloaded it (if you cloned the repo, the file is already present). Go inside that folder and run the following code to make sure everything is setup properly.

        python my_trading_params.py

4. Use *my_trading_params.py* as a template which contains skeleton functions (with explanation) that need to be filled in to create your own trading strategy. Copy that template to another file and then start implementing the methods in that file. You can use *pair_trading_params.py* and *meanreversion_trading_params.py* as motivation.

# **How does the toolbox work?** #

Any security you want to trade with the toolbox is called an *instrument*. Right now, the toolbox supports stock and future instruments. All the parameters for the toolbox are supplied in class `MyTradingParams()`.

## Quick Setup ##
To get started quickly with the toolbox, you need to

1. Get Historical Data
2. Specify Features to be created from the Data
3. Create a prediction function using above features to make your prediction for the market

The toolbox can handle everything else for you. You can do the above by modifying the following functions:

### Getting Data - DataSource ####
Data Source parses data from external sources (csv, log file, html file etc) and loads and converts it into a toolbox compatible form. You need to specify the instrumentID's that you need data for and start and end date for data in in `getDataParser()` function.
```python
def getDataParser(self):
        instrumentIds = ['IBM', 'AAPL', 'MSFT']
        startDateStr = '2017/05/10'
        endDateStr = '2017/06/09'
        return YahooStockDataSource(cachedFolderName='yahooData',
                                     instrumentIds=instrumentIds,
                                     startDateStr=startDateStr,
                                     endDateStr=endDateStr)
```
Current choices for datasource are:
* [YahooStockDataSource](https://links.auquan.com/yahooDataSource) - Stock data from Yahoo (daily data)
* [NSEStockDataSource](https://links.auquan.com/nseDataSource) - Stock data from NSE (daily data)
* AuquanDataSource - Data from US stock database of 500 biggest stocks maintained by Auquan.

### Specifying Features - Instrument, Market and Custom Features ###
You can manipulate historical data by creating features. Features are called by specifying config dictionaries. You have to:

1. Create one config dictionary per feature.

    **Feature config Dictionary has the following keys:**
  > *featureId:* string representing the feature you want to use  
  > *featureKey:* {optional} string representing key to access value of this feature. If not present, use featureId  
  > *params:* {optional} A dictionary with which contains other parameters, if needed by the feature  

2. Return an array of all feature config dictionaries as market features or instrument features. Specify the instrument features in function `getInstrumentFeatureConfigDicts()` and market features in function `getMarketFeatureConfigDicts()`. Instrument features are calculated per instrument (for example position, fees, moving average of instrument price). The toolbox auto-loops through all instruments to calculate features for you. Market features are calculated for whole trading system (for example portfolio value).

    **Example**: If you want to use the moving_sum feature and calculate this for all instruments, your *`getInstrumentFeatureConfigDicts()`* function should be:
```python
  def getInstrumentFeatureConfigDicts(self):
        msDict = {'featureKey': 'ms_5',
                'featureId': 'moving_sum',
                'params': {'period': 5,
                'featureName': 'basis'}}
        return [msDict]
```

You can now use this feature by calling it's featureKey, 'ms_5'.      
Full list of features with featureId and params is available [here](#).

***Custom Features - Optional***

To use your own custom features, you need to create them separately. Follow the example of [this template](https://links.auquan.com/customFeature). Specifically, you'll have to:

* Create a new class for the feature and implement your logic. You can copy the template from [this file](https://links.auquan.com/customFeature).
    Example: If you were implementing a new InstrumentFeature
```python
class MyCustomFeatureClassName(Feature):
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):
        return 5
```

* Modify function `getCustomFeatures()` to return a dictionary with   
  > *key:* featureId to access this feature (Make sure this doesn't conflict with any of the pre defined feature Ids)  
  > *value:* Your custom Class Name which computes this feature. The class should be an instance of Feature

    Eg. to use the feature we create above via featureId='my_custom_feature_identifier',  
```python
def getCustomFeatures(self):
        return {'my_custom_feature_identifier': MyCustomFeatureClassName}
```

* Now you can create a dict for this feature in `getInstrumentFeatureConfigDicts()`. Dict format is:
```python
  customFeatureDict = {'featureKey': 'my_custom_feature_key',
                         'featureId': 'my_custom_feature_identifier',
                          'params': {'param1': 'value1'}}
```

Use this feature by calling it's featureKey, 'my_custom_feature_key'


### Prediction Function ###
Combine all the features to create the desired prediction function. Fill the funtion `getPrediction()` to return the prediction for instrument you are trading.

Here you can call your previously created features by referencing their featureId. For example, I can call my moving sum and custom feature as:
```python
def getPrediction(self, time, currentMarketFeatures, instrumentManager):

        # holder for all the instrument features
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()

        ms5Data = lookbackInstrumentFeatures.getFeatureDf('ms_5')
        # dataframe for a historical instrument feature (ms_5 in this case).   
        # The index is the timestamps of atmost lookback data points.
        # The last row of this data frame would contain the features
        # which are being calculated in this update cycle or for this time.
        # The second to last row (if exists) would have the features for the previous
        # time update.
        # The columns of this dataframe are the stock symbols/instrumentIds.

        ms5 = ms5Data.iloc[-1]

        # This returns the value of the feature at the last time update
        # Returns a series with index as all the instrumentIds.

        customData = lookbackInstrumentFeatures.getFeatureDf('my_custom_feature_key')
        custom = customData.iloc[-1]
        predictions = ms5 / custom
        return predictions
```

Predictions can be of many types. You can calculate(predict) the *FairValue* of a parameter, for example price. You can predict the probability that price will increase in the future. You can predict the ratio of price of two securities. You can predict the ranking of a basket of securities. Output of the prediction function is used by the toolbox to make further trading decisions via the [execution system](#). Choice of execution system depends on the type of prediction made.

## Final Metrics ##
The system returns the following final metrics:

1. *Total PnL:* Total Profit(or Loss) from your strategy as a % of initial capital
2. *Annualized Return:* The yearly average % Profit(or Loss) from your trading strategy
3. *Annualized Volatility:* The standard deviation of daily returns of the model in a year. Volatility is used as a measure of risk, therefore higher vol implies riskier model.
4. *Sharpe Ratio:* The reward/risk ratio or risk adjusted returns of the strategy, calculated as Annualized Return/Annualized Volatility
5. *Sortino Ratio:* Returns adjusted for downside risk, calculated as Annualized Return/Annualized Volatility of Negative Returns
6. *Max Drawdown:* Largest drop in Pnl or maximum negative difference in total portfolio value. It is calculated as the maximum high to subsequent low difference before a new high is reached.
7. *Win/Loss, Average Profit/Loss:* Sum(or Avergae) of Profits from trades that results in profits/Sum(or Average) of losses from trades that results in losses
8. *% Profitability* = % of total trades that resulted in profits
9. *Return on Capital* = Total Profit(or Loss) from your strategy as a % of max capital used

Other Metrics can be supported if needed.

## Importing a trained model ##

If you would like to write your own custom datasource/execution system or you want to import a pre-trained ML model, you can do so in the manner below.
Here we store a file `training_execution_system.py` on github. Then we specify the path to file, and the code downloads the file as `fileName` and imports the required class from it.

```python

import urllib

path_to_file = 'https://raw.githubusercontent.com/Auquan/quant-quest-2/master/training_execution_system.py'
fileName = 'training_execution_system.py'
if not os.path.isfile(fileName):
    urllib.urlretrieve (path_to_file, fileName)

from training_execution_system import TrainingExecutionSystem

```

## Under the Hood - Trading System ##
This is the main system that runs your backtest. All the parameters for the trading system are supplied in class `MyTradingParams()`

Raw data (intraday tick data or end of day data) is read from the datasource for all instruments and sent to the trading system. At every such update of data, the trading system does the following things and then updates the state of that instrument in the system :  

* Checks whether it is time to update the features and execute. It updates features at a frequency determined by trading parameters.  
* If it is, it first loops over all instruments and updates the features for each instrument (specified by trading parameters). Each instrument stores its features, which can be later extracted out.  
* Then, the trading system computes all the market features (specified by trading parameters).
  The system also stores such market features at every update features interval.
  An example of market feature is 'prediction' which the user needs to provide - This feaure specifies our prediction probability that the specified instrument is a buy  
* Then the trading system looks at the prediction value and passes it to an execution system. This converts uses the prediction value (and current capital, risk limits etc) to decide what positions should he trading system take for various instruments.  
* Trade executions generated by Execution System are then passed into the orderPlacer, which tries to place these orders into the market.

Trading System also keeps checking for confirmation of orders which are placed. It updates instrument positions for trades that are confirmed.

For trading system to work, following need to be specified:

### DataSource ###
[Read Above](#)

### Benchmark ###
The market instrument to benchmark your strategy's perfromancy. Strategies that perform better than the benchmark are considered successful.
*Make sure that you specify the benchmark instrumentID in list of instruments to get data for.*

### Starting Capital ###
The initial amount of money you're putting into your trading system. This is set to 1 million notional by default.

### Frequency Of Feature Updates ###
Frequency of updates to features. Any updates within this frequncy to instruments do not trigger feature updates.
Consequently any trading decisions that need to take place happen with the same frequency
This is important when you are working with frequently updating data - for example intraday tick data

### PriceFeatureKey ###
You may have multiple measures of price for an instrument at the same time, for example open price, close price etc. Specify which price to use for pnl calculations. By default, this is set to *'close'* for daily calculations.

### Lookback Size ###
How far back do you want the historical data for your calculations.
The historical market features and instrument features are only stored upto this amount. The more data you request, the slower your system will be.

### Instrument Features, Market Features and Custom Features ###
[Read Above](#)

### Prediction Function ###
[Read Above](#)

### ExecutionSystem ###
Takes a prediction value and converts it into possible trades for each instrument. It takes into account current positions, risk limits, current capital and value of the prediction.

All execution systems take the following arguments:

* 'longLimit': Max long position. No buys if instrument position == longLimit, can be specified as dollar or lot size
* 'shortLimit': Max short position. No sells if instrument position == shortLimit, can be specified as dollar or lot size
* 'capitalUsageLimit': Minimum capital threshold, specified as % of initial capital. No trades if currentCapital/initialCapital < capitalUsageLimit
* 'lotSize': Size to trade per trade, can be specified as dollar or lot size
* 'limitType': 'D' for dollar(monetary) limit, 'L' for lot size limit
* 'price': Feature to use as price

Right now we support following executions:

System  | Description | Parameters | Snippet
:-------------: | ------------- | ------------- | -------------  
*SimpleExecutionSystem*  | Simplest type, takes prediction in the form of probability that price will go up. Instruments with probability of price increasing above *enter_threshold* are bought and below *(1-enter_threshold)* are sold. Instrument positions with probability predictions values between *(1-exit_threshold)* and *exit_threshold* are closed | 'enter_threshold', 'exit_threshold', 'longLimit', 'shortLimit', 'capitalUsageLimit', 'lotSize', 'limitType', 'price' |
*SimpleExecutionSystemWithFairValue*  | Takes prediction in the form of FairValue of price. Instruments with CurrentPrice - FairValue > *enter_threshold_deviation* are sold and FairValue - CurrentPrice > *enter_threshold_deviation* are bought. Instrument positions with abs(CurrentPrice - FairValue) < *exit_threshold_deviation* are closed | 'enter_threshold_deviation', 'exit_threshold_deviation', 'longLimit', 'shortLimit', 'capitalUsageLimit', 'lotSize', 'limitType', 'price'
*PairExecutionSystem*, *PairExecutionSystemWithFairValue*| Behaves the same as above two, except predictions are made on ratio of prices between two instruments(pair) | 'pair', 'pairRatio','enter_threshold_deviation', 'exit_threshold_deviation', 'longLimit', 'shortLimit', 'capitalUsageLimit', 'lotSize', 'limitType', 'price'

### OrderPlacer ###
Execution System decided what trades you want to do, order placer actually makes those trades (place an order), and also reads confirmations of orders being placed.
For Backtesting, you can just use the BacktestingOrderPlacer, which places the order and automatically trades at 'PriceFeatureKey' price at the same time.

# **ML Training System**
To make creation and testing of ML models easy for you, we are providing you with a ML model creation suite. This is a beta feature, so please bear with us while we iron out the bugs!

### Installation ###

Get the toolbox by typing the following commands in your terminal:
```
pip uninstall auquan_toolbox
pip install -U auquan_toolbox_beta --no-cache-dir
```

For ML Training system to work, following need to be specified:

### DataSource ###
Similar to Trading System above.

### DataSplit Ratio ###
A list specifying the percentage of Training, Validation and Test Data. Eg [6,2,2]. The model is trained and validated on Training and Validation data respectively and then backtested for trading on Test Data.

### InstrumentFeatureConfigDicts###
Similar to Trading System above.

### CustomFeatures ###
Similar to Trading System above.

### Target Variable ###
The Variable you want to predict. This can be one or many variables. They can be specified as one of the features created above (with a shift) or loaded from a file as below:
```python
getTargetVariableConfigDicts(self):
        Y = {'featureKey' : 'Y', #Use a feature loaded from datasource
             'featureId' : '',
             'params' : {}}
        tv = {'featureKey' : 'direction_tv',  ##Create a target variable from a feature
                  'featureId' : 'direction',
                  'params' : {'period' : 5,
                              'featureName' : 'ma_5',
                              'shift' : 5}}
        return {INSTRUMENT_TYPE_STOCK : [tv]}
```

### FeatureSelectionConfigDicts ###
Use this to specify the methods to be used for feature engineering. For example, you can choose to reduce the overall set of features by keeping only those features which display a certain minimum correlation to target Variable. Current Available methods are:
```python
def getFeatureSelectionConfigDicts(self):
        corr = {'featureSelectionKey': 'corr',
                'featureSelectionId' : 'pearson_correlation',
                'params' : {'startPeriod' : 0,
                            'endPeriod' : 60,
                            'steps' : 10,
                            'threshold' : 0.1,
                            'topK' : 2}}

        genericSelect = {'featureSelectionKey' : 'gus',
                         'featureSelectionId' : 'generic_univariate_select',
                         'params' : {'scoreFunction' : 'f_classif',
                                     'mode' : 'k_best',
                                     'modeParam' : 'all'}}

        rfecvSelect = {'featureSelectionKey': 'rfecv',
                       'featureSelectionId': 'rfecv_selection',
                       'params' : {'estimator' : 'LinearRegression',
                       'estimator_params' : {},
                       'step' : 1,
                       'cv' : None,
                       'scoring' : None,
                       'n_jobs' : 2}}

        return {INSTRUMENT_TYPE_STOCK : [genericSelect]}
```
### FeatureTransformationConfigDicts ###
The methods you want to use to normalize or transform features. Current available methods are:
```python
def getFeatureTransformationConfigDicts(self):
        stdScaler = {'featureTransformKey': 'stdScaler',
                     'featureTransformId' : 'standard_transform',
                     'params' : {}}

        minmaxScaler = {'featureTransformKey' : 'minmaxScaler',
                        'featureTransformId' : 'minmax_transform',
                        'params' : {'low' : -1,
                                    'high' : 1}}
        pcaScaler = {'featureTransformKey' : 'pcaScaler',
                      'featureTransformId' : 'pca_transform',
                      'params' : {'n_comp' : 6,
                                  'copy' : True,
                                  'whiten' : False,
                                  'svd' : 'full',
                                  'itr_power' : 'auto',
                                  'random_state' : None}}
        return {INSTRUMENT_TYPE_STOCK : [stdScaler]}
```
### Model Config Dicts ###
The ML models you want to train. Current available models are:
```python
def getModelConfigDicts(self):
        regression_model = {'modelKey': 'linear_regression',
                     'modelId' : 'linear_regression',
                     'params' : {}}

        mlp_regression_model = {'modelKey': 'mlp_regression',
                     'modelId' : 'mlp_regression',
                     'params' : {}}

        classification_model = {'modelKey': 'logistic_regression',
                     'modelId' : 'logistic_regression',
                     'params' : {}}

        mlp_classification_model = {'modelKey': 'mlp_classification',
                     'modelId' : 'mlp_classification',
                     'params' : {}}

        svm_model = {'modelKey': 'svm_model',
                     'modelId' : 'support_vector_machine',
                     'params' : {}}
        return {INSTRUMENT_TYPE_STOCK : [classification_model]}
```

### Prediction Function ###
You do not have to specify a prediction function. The toolbox automatically creates a prediction function using the features and trained model from above.
