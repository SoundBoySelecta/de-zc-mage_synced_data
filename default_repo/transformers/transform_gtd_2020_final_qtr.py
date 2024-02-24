

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    
    Columns for reference:
    'VendorID', 'lpep_pickup_datetime', 'lpep_dropoff_datetime', 'store_and_fwd_flag', 'RatecodeID', 'PULocationID', 'DOLocationID',
    'passenger_count', 'trip_distance', 'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'ehail_fee', 'improvement_surcharge',
    'total_amount', 'payment_type', 'trip_type', 'congestion_surcharge'
    """
    # Specify your transformation logic here
    # Passenger_count and trip distance with zeros removed
    passenger_count_greater_than_zero = data['passenger_count'] > 0
    trips_distance_greater_than_zero = data['trip_distance'] > 0
    # Overwrite original dataframe
    data =  data[passenger_count_greater_than_zero & trips_distance_greater_than_zero]

    # Create a year column from  lpep_pickup_datetime by convertingto a date.
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    #print(dir(dt))
    print(data.dtypes)
    return data

# 1601512279000
# 1601510400000

# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'
