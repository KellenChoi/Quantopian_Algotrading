####### only work on quantopian platform #########

### Research  

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## get_pricing()
## The get_pricing function provides access to 12 years of US Equity pricing data: returns a pandas object
mcdon = get_pricing('MCD',
                    start_date='2017-01-01', 
                    end_date = '2017-02-01', 
                    frequency='minute')
mcdon.head()
mcdon.info()
# Can only go about 12 years back
# which is really all you need for algo trading, 
# going back further probably is more noise than signal.
mcdon = get_pricing('MCD',
                    start_date='2005-01-01', 
                    end_date = '2017-01-01', 
                    frequency='daily')
mcdon['close_price'].plot()  ## plotting close prices
mcdon['close_price'].pct_change(1).hist(bins=100,figsize=(6,4))  ## histogram of daily returns


## symbols()  :  returns the security object for a ticker symbol
mcdon_eq_info = symbols('MCD')
type(mcdon_eq_info)

# getting info of the security
for key in mcdon_eq_info.to_dict():
    print(key)
    print(mcdon_eq_info.to_dict()[key])
    print('\n')


## get_fundamentals() : provides programmatic access to the Quantopian fundamental database

# Have to do this first in the notebook:
fundamentals = init_fundamentals()

# Market Cap
my_query = query(fundamentals.valuation.market_cap)
my_funds = get_fundamentals(my_query,'2017-01-01')
my_funds.info()

# Basically just returns the market cap of everything
# for 2017-01-01
my_funds.head()

# What you usualy do is filter by other qualities after the query!
# Only get companies worth 500 billion or more (that's a lot of dough!)
big_companies = (query(fundamentals.valuation.market_cap).
                 filter(fundamentals.valuation.market_cap > 500000000000) )
                 
my_big_funds = get_fundamentals(big_companies,'2017-07-19')
my_big_funds  # 7.824930e+11 .......
7.82 * 10**11
