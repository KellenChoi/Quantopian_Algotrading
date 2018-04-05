#######  only work on Quantopian platform ##########

#### Basic Algorithm Methods
## Algorithmically test our earlier optimized tech portfolio strategy with Quantopian!

### initialize()
## initialize() is called exactly once when our algorithm starts and requires context as input.

### handle_data()
## called once at the end of each minute and requires context and data as input

##### Tech Stock Optimized Portfolio #########
## note: handle_data() is readjusting portfolio every minute!!
def initialize(context):
    # Reference to Tech Stocks
    context.aapl = sid(24)
    context.csco = sid(1900)
    context.amzn = sid(16841)
    
def handle_data(context, data):
    # Position our portfolio optimization!
    order_target_percent(context.aapl, .27)
    order_target_percent(context.csco, .20)
    order_target_percent(context.amzn, .53)
    

### Grabbing current data
## data.current()
# to retrieve the most recent value of a given field(s) for a given asset(s)
# two arguments: the asset or list of assets, and the field or list of fields being queried
def initialize(context):
    # Reference to Tech Stocks
    context.techies = [sid(16841),sid(24),sid(1900)]

def handle_data(context, data):
    # Position our portfolio optimization!
    tech_close = data.current(context.techies,'close')
    print(type(tech_close)) # Pandas Series
    print(tech_close) # Closing Prices 

## note: data.is_stale(sid(#))
# to check if the results of data.current() where generated at the current bar (the timeframe) or were forward filled from a previous time


#### Checking for trading
## data.can_trade()
#  determine if an asset(s) is currently listed on a supported exchange and can be ordered
#  a single argument: an asset or a list of assets
def initialize(context):
    # Reference to amazn
    context.amzn = sid(16841)
    
def handle_data(context, data):
    # This insures we don't hit an exception!
    if data.can_trade(sid(16841)):
        order_target_percent(context.amzn, 1.0)
        
        
 ##### Checking historical data
 ## data.history()
 ## the returned data is adjusted for splits, mergers, and dividends as of the current simulation date
 def initialize(context):
    # AAPL, MSFT, and SPY
    context.assets = [sid(24), sid(1900), sid(16841)]

def before_trading_start(context,data):
    price_history = data.history(context.assets,fields="price", bar_count=5, frequency="1d")
                                      ## returns the prices for the previous 4 days and the current price
    print(price_history)



##### Scheduling
## schedule_function()
# indicate when you want other functions to occur
# must take context and data as parameters
def initialize(context):
    context.appl = sid(49051)

    # At ebginning of trading week
    # At Market Open, set 10% of portfolio to be apple
    schedule_function(open_positions, date_rules.week_start(), time_rules.market_open())
    
    # At end of trading week
    # 30 min before market close, dump all apple stock.
    schedule_function(close_positions, date_rules.week_end(), time_rules.market_close(minutes=30))

def open_positions(context, data):
    order_target_percent(context.appl, 0.10)

def close_positions(context, data):
    order_target_percent(context.appl, 0)



##### Portfolio Information
def initialize(context):
    context.amzn = sid(16841)
    context.ibm = sid(3766)

    schedule_function(rebalance, date_rules.every_day(), time_rules.market_open())
    schedule_function(record_vars, date_rules.every_day(), time_rules.market_close())

def rebalance(context, data):
    # Half of our portfolio long on amazn
    order_target_percent(context.amzn, 0.50)
    # Half is shorting IBM
    order_target_percent(context.ibm, -0.50)

def record_vars(context, data):

    # Plot the counts
    record(amzn_close=data.current(context.amzn,'close'))
    record(ibm_close=data.current(context.ibm,'close'))
    
    
    
##### Slippage
### Slippage is where a simulation estimates the impact of orders on the fill rate and execution price they receive
### Fill rates are dependent on the order size and current trading volume of the ordered securit
### The volume_limit determines the fraction of a security's trading volume that can be used by your algorithm

set_slippage(slippage.VolumeShareSlippage(volume_limit=0.025, price_impact=0.1))


##### Commision
### set the cost of trades, we can specify a commission model in initialize() using set_commission()

set_commission(commission.PerShare(cost=0.0075, min_trade_cost=1))

## Slippage and commission models can have an impact on the performance of a backtest. 
## The default models used by Quantopian are fairly realistic, and it is highly recommended that you use them.










