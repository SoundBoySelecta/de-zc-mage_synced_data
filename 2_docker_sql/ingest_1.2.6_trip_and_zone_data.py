# Import needed libraries
import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import sys
import os


def main(params):
    # initialize paramters
    host = params.host
    user = params.user
    password = params.password
    port = params.port
    db = params.db
    trip_table_name = params.trip_table_name
    zone_table_name = params.zone_table_name
    trip_file_name = 'ny_green_taxi_trip.gz'
    zone_file_name = 'ny_taxi_zone.csv'
    trip_data_url = params.trip_data_url
    zone_data_url = params.zone_data_url

# Download taxi trip data make sure on pd.read_read to add arg compression='gzip'
    os.system(f'wget {trip_data_url} --output-document={trip_file_name}')
# Download taxi zone data make sure on pd.read_read to
# NOT add arg compression='gzip'
    os.system(f'wget {zone_data_url} --output-document={zone_file_name}')


#Setup connection to db
    engine = create_engine(
        f'postgresql://{user}:{password}@{host}:{port}/{db}')

# Connect to db
    engine.connect()


# Import zone data into pandas
    df_zone_data = pd.read_csv(filepath_or_buffer=zone_file_name)


# View Shape
    print(
        f'Imported zone data -->Dataframe rows:{df_zone_data.shape[0]},\
        Dataframe columns:{df_zone_data.shape[1]}')

#Insert into new zone table zone data.
    df_zone_data.to_sql(name=zone_table_name, con=engine, if_exists='replace')

# Create a column list and remove 100% null value columns (ehail_fee)
    keep_cols = ['VendorID',
                 'lpep_pickup_datetime',
                 'lpep_dropoff_datetime',
                 'store_and_fwd_flag',
                 'RatecodeID',
                 'PULocationID',
                 'DOLocationID',
                 'passenger_count',
                 'trip_distance',
                 'fare_amount',
                 'extra',
                 'mta_tax',
                 'tip_amount',
                 'tolls_amount',
                 'improvement_surcharge',
                 'total_amount',
                 'payment_type',
                 'trip_type',
                 'congestion_surcharge']

# Import trip data into pandas (chunks needed since large file,
#more to simulate batch processing as 400k is managable)
# Create iterable to import in chunks, this does not create a df,
# but an iterable object
    trip_data_iterable_in_100k_chunks = pd.read_csv( \
        filepath_or_buffer=trip_file_name, iterator=True, chunksize=100000, \
        parse_dates=['lpep_pickup_datetime', 'lpep_dropoff_datetime'], \
        usecols=keep_cols, compression='gzip')
# Iterate over the first 100K rows (this is a df)
    df_trip_data_in_100k_chunks = next(trip_data_iterable_in_100k_chunks)

# Verify shape (Remember original csv had 20 columns, we dropped the 'ehail_fee' which was empty)
    print(
        f'Imported first chunk of trip data -->:\
        Dataframe rows:{df_trip_data_in_100k_chunks.shape[0]},\
        Dataframe columns:{df_trip_data_in_100k_chunks.shape[1]}')

# # *****THIS IS NOT NEEDED****, schema in the sense of table definition is automatic,
# # when using df.to_sql, no need for DDL with pd.io.sql.get_schema()
# # Create a DDL statement for a new sql table from the dataframe with the associated
# # data types of that system provide name for table "ny_green_taxi",
# # remember this command doesnt actually create the table.
#     # pd.io.sql.get_schema(df_trip_data_in_100k_chunks,
#     #                      name=table_name, con=engine)

# Insert into tables the first 100k rows.
    df_trip_data_in_100k_chunks.to_sql(
        name=trip_table_name, con=engine, if_exists='replace')

# Add the rest of the data in 100k row chunks in a loop
    while True:
        t_start = time()
        df_trip_data_in_100k_chunks = next(trip_data_iterable_in_100k_chunks)
        df_trip_data_in_100k_chunks.to_sql(
            name=trip_table_name, con=engine, if_exists='append')
        t_end = time()
        print('Inserted another chunk, took %.3f second' % (t_end - t_start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Ingest csv data to postgres.')

    parser.add_argument('--host', help='hostname for postgres')
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument(
        '--trip_table_name', help='trip table to be written to in postgres')
    parser.add_argument(
        '--zone_table_name', help='zone table to be written to in postgres')
    parser.add_argument('--trip_data_url', help='url for the gz file')
    parser.add_argument('--zone_data_url', help='url for the gz file')

    args = parser.parse_args()

    main(args)

