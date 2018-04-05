##### 20 days MA & above and below 2 times the 20 day rolling std, 100% of porsition
#### Johnson and Johnson: sid(4151)

# Setup our variables
def initialize(context):
    context.jj = sid(4151)

    schedule_function(check_bands,date_rules.every_day())
        
def check_bands(context, data):
    
    cur_price = data.current(context.jj,'price')
    
    # Load historical data for the stocks
    prices = data.history(context.jj,'price', 20 , '1d')
    
    avg = prices.mean()
    std = prices.std()
    lower_band = avg - 2*std
    upper_band = avg + 2*std
    
    if cur_price <= lower_band:
        order_target_percent(context.jj, 1.0)
        print('Buying')
        print('Current price is: ' + str(cur_price))
        print("Lower band is: "+str(lower_band))
        
        
    elif cur_price >= upper_band:
        order_target_percent(context.jj, -1.0)
        print('Shorting')
        print('Current price is: ' + str(cur_price))
        print("Upper band is: "+str(upper_band))
    else:
        pass
        
    record(upper=upper_band,
           lower=lower_band,
           mvag_20=avg,
           price=cur_price)
