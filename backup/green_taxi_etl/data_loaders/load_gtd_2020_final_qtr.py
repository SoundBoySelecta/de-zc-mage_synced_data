import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    #Specify schema for dataframe 
    taxi_dtypes = {
        'VendorID': 'Int64',
        'store_and_fwd_flag': 'str',
        'RatecodeID': 'Int64',
        'PULocationID': 'Int64',
        'DOLocationID': 'Int64',
        'passenger_count': 'Int64',
        'trip_distance': 'float64',
        'fare_amount': 'float64',
        'extra': 'float64',
        'mta_tax': 'float64',
        'tip_amount': 'float64',
        'tolls_amount': 'float64',
        'ehail_fee': 'float64',
        'improvement_surcharge': 'float64',
        'total_amount': 'float64',
        'payment_type': 'float64',
        'trip_type': 'float64',
        'congestion_surcharge': 'float64'
    }
    # date columns to parse 
    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']
    
    # Establish months
    months = ["2020-10", "2020-11", "2020-12"]

    #Create an empty list to store all df
    dfs = {}
    for month in months:
        url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_{month}.csv.gz'
        
        df_name = f'gtd_{month}'
        dfs[df_name] =  pd.read_csv(url, compression='gzip', dtype=taxi_dtypes, parse_dates=parse_dates)

   # Assert all 3 dfs align in length of columns
    assert len(set([df.shape[1] for df in dfs.values()])) == 1, "Column lengths in each dataframes are not equal"
   
    #Concatenate all dataframes
    gtd_2020_final_qtr = pd.concat(list(dfs.values()))
    
    return gtd_2020_final_qtr

  
@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
