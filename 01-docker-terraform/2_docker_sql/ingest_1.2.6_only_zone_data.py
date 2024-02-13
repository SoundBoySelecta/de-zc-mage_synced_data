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
    # trip_table_name = params.trip_table_name
    zone_table_name = params.zone_table_name
    # trip_file_name = 'ny_green_taxi_trip.gz'
    zone_file_name = 'ny_taxi_zone.csv'
    # trip_data_url = params.trip_data_url
    zone_data_url = params.zone_data_url

# download taxi trip data make sure on pd.read_read to add arg compression='gzip'
# os.system(f'wget {trip_data_url} --output-document={trip_file_name}')
# download taxi zone data make sure on pd.read_read to
# NOT add arg compression='gzip'
    os.system(f'wget {zone_data_url} --output-document={zone_file_name}')


# Setup connection to db
    engine = create_engine(
        f'postgresql://{user}:{password}@{host}:{port}/{db}')

# Connect to db
    engine.connect()


# Import zone data into pandas
    df_zone_data = pd.read_csv(filepath_or_buffer=zone_file_name)

    print(
        f'Dataframe rows: {df_zone_data.shape[0]}, Dataframe columns: {df_zone_data.shape[1]}')

# Insert into new zone table zone data.
    df_zone_data.to_sql(name=zone_table_name, con=engine, if_exists='replace')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Ingest csv data to postgres.')

    parser.add_argument('--host', help='hostname for postgres')
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    # parser.add_argument(
    #     '--trip_table_name', help='trip table to be written to in postgres')
    parser.add_argument(
        '--zone_table_name', help='zone table to be written to in postgres')
    # parser.add_argument('--trip_data_url', help='url for the gz file')
    parser.add_argument('--zone_data_url', help='url for the gz file')

    args = parser.parse_args()

    main(args)
