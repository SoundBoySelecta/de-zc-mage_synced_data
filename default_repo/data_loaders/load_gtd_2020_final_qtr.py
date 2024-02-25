import pandas as pd
# import parquet-tools

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
    periods = []
    for i in range(1, 13):
        if len(str(i)) == 1:
            periods.append(f'2022-{str(i).zfill(2)}')
        else:
            periods.append(f'2022-{i}')
    for period in periods:
        url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{period}.parquet'
        print(url)
    url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-01.parquet'
    df = pd.read_parquet(url)
    print(df.shape)
#     #Create an empty list to store all df
#     dfs = {}
#     for month in months:
#         url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_{month}.csv.gz'
        
#         df_name = f'gtd_{month}'
#         dfs[df_name] =  pd.read_csv(url, compression='gzip', dtype=taxi_dtypes, parse_dates=parse_dates)

#    # Assert all 3 dfs align in length of columns
#     assert len(set([df.shape[1] for df in dfs.values()])) == 1, "Column lengths in each dataframes are not equal"
   
#     #Concatenate all dataframes
#     gtd_2020_final_qtr = pd.concat(list(dfs.values()))



    
    # return gtd_2020_final_qtr

  
# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'