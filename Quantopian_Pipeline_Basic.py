#### Pipeline: providing a uniform API for expressing computations on a diverse collection of datasets.
## Factors: a function from an asset and a moment in time to a numerical value
## Filters: used for describing sets of assets to include or exclude for some particular purpose
## Classifiers: categorical output. used for grouping assets for complex transformations on Factor outputs.

from quantopian.pipeline import Pipeline
def make_pipeline():
    return Pipeline()
    
pipe = make_pipeline()
from quantopian.research import run_pipeline
result = run_pipeline(pipe,'2017-01-01','2017-01-01')
result.head(10)
result.info()

# Data
from quantopian.pipeline.data.builtin import USEquityPricing
# Factors
from quantopian.pipeline.factors import BollingerBands,SimpleMovingAverage,EWMA
SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)


def make_pipeline():
    
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    
    return Pipeline(columns={
        '30 Day Mean Close':mean_close_30
    })
results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')
results.head(20)


def make_pipeline():
    
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    latest_close = USEquityPricing.close.latest
    
    return Pipeline(columns={
        '30 Day Mean Close':mean_close_30,
        'Latest Close':latest_close
    })
results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')
results.head(10)

### Combining Factors
def make_pipeline():
    
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    latest_close = USEquityPricing.close.latest
    
    percent_difference = (mean_close_10-mean_close_30) / mean_close_30
    
    return Pipeline(columns={
        'Percent Difference':percent_difference,
        '30 Day Mean Close':mean_close_30,
        'Latest Close':latest_close
    })
    
results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')
results.head()


### Filters
last_close_price = USEquityPricing.close.latest
close_price_filter = last_close_price > 20
close_price_filter

def make_pipeline():
    
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    latest_close = USEquityPricing.close.latest
    
    percent_difference = (mean_close_10-mean_close_30) / mean_close_30
    
    perc_diff_check = percent_difference > 0 
    
    return Pipeline(columns={
        'Percent Difference':percent_difference,
        '30 Day Mean Close':mean_close_30,
        'Latest Close':latest_close,
        'Positive Percent Diff': perc_diff_check
    })
    
results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')
results.head()

### Screens
def make_pipeline():
    
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    latest_close = USEquityPricing.close.latest
    
    percent_difference = (mean_close_10-mean_close_30) / mean_close_30
    
    perc_diff_check = percent_difference > 0 
    
    return Pipeline(columns={
                            'Percent Difference':percent_difference,
                            '30 Day Mean Close':mean_close_30,
                            'Latest Close':latest_close,
                            'Positive Percent Diff': perc_diff_check},
                    screen=perc_diff_check)

results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')
results.head()

### Reverse a screen
def make_pipeline():
    
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    latest_close = USEquityPricing.close.latest
    
    percent_difference = (mean_close_10-mean_close_30) / mean_close_30
    
    perc_diff_check = percent_difference > 0 
    
    return Pipeline(columns={
                            'Percent Difference':percent_difference,
                            '30 Day Mean Close':mean_close_30,
                            'Latest Close':latest_close,
                            'Positive Percent Diff': perc_diff_check},
                    screen=~perc_diff_check)
                    
                    
                    
results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')
results.head()

#### Combining Filters
def make_pipeline():
    
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    latest_close = USEquityPricing.close.latest
    
    percent_difference = (mean_close_10-mean_close_30) / mean_close_30
    
    perc_diff_check = percent_difference > 0 
    small_price = latest_close < 5
    
    final_filter = perc_diff_check & small_price
    
    return Pipeline(columns={
                            'Percent Difference':percent_difference,
                            '30 Day Mean Close':mean_close_30,
                            'Latest Close':latest_close,
                            'Positive Percent Diff': perc_diff_check},
                    screen=final_filter)
                    
results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')
results.head()  



### Masking: ignore certain assets
def make_pipeline():
    
    # Create Filters for Masks First
    latest_close = USEquityPricing.close.latest
    small_price = latest_close < 5
    
    # Pass in the mask
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10,mask=small_price)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30,mask=small_price)
    
    
    percent_difference = (mean_close_10-mean_close_30) / mean_close_30
    
    perc_diff_check = percent_difference > 0 
    
    
    final_filter = perc_diff_check
    
    return Pipeline(columns={
                            'Percent Difference':percent_difference,
                            '30 Day Mean Close':mean_close_30,
                            'Latest Close':latest_close,
                            'Positive Percent Diff': perc_diff_check},
                    screen=final_filter)
                    
results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')
results.head()  
len(results)


### Classifiers: for categorical output
from quantopian.pipeline.data import morningstar
from quantopian.pipeline.classifiers.morningstar import Sector

morningstar_sector = Sector()
exchange = morningstar.share_class_reference.exchange_id.latest
exchange

nyse_filter = exchange.eq('NYS')

def make_pipeline():
    
    # Create Filters for Masks First
    latest_close = USEquityPricing.close.latest
    small_price = latest_close < 5
    
    # Classifier
    nyse_filter = exchange.eq('NYS')
    
    # Pass in the mask
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10,mask=small_price)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30,mask=small_price)
    
    
    percent_difference = (mean_close_10-mean_close_30) / mean_close_30
    
    perc_diff_check = percent_difference > 0 
    
    
    final_filter = perc_diff_check & nyse_filter
    
    return Pipeline(columns={
                            'Percent Difference':percent_difference,
                            '30 Day Mean Close':mean_close_30,
                            'Latest Close':latest_close,
                            'Positive Percent Diff': perc_diff_check},
                    screen=final_filter)

results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')
results.head()
len(results)



### Pipelines in Quantopian IDE
from quantopian.pipeline import Pipeline
from quantopian.algorithm import attach_pipeline, pipeline_output

def initialize(context):
    my_pipe = make_pipeline()
    attach_pipeline(my_pipe, 'my_pipeline')

def make_pipeline():
    return Pipeline()

def before_trading_start(context, data):
    # Store our pipeline output DataFrame in context.
    context.output = pipeline_output('my_pipeline')

                    
