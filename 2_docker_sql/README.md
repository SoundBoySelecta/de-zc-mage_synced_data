1.2.1 Welcome to docker
Used docker many times but for newbies:
download docker desktop for associated os, follow instructions for
docker hello-world, which if u get working, then docker is working and
you just created a small webserver with docker welcome html page.
Basically understand what docker is, as much as people explain it,
my understanding was wrong for a while, it isnt isolated enviroments
but isolated processes, it still depends on host os, so obviously
as host os crashes everything crashes. Versus a vm, if the host os
crashes, all vm guest os crashes, however if a guest os crashes
other guest os dont crash, there lies an advantage, maybe not so
much in cloud instances where there is redundancy. One thing I am still
researching is the parent layer is said not to neccessarily be an os
layer, but some have termed it can be solely bare distributions
(collection of files) or libs, that actually feed off host os/kernel.
Im still not convinced as Ive always see some flavor of linux
in STDOUT.


1.2.2 Ingesting NY Taxi Data to Postgres
ingest.ipynb
To verify the docker postgres image works and for ease of interaction
using jupyter notebooks, we manually insert data into postgres.

1.2.3 Connecting pgAdmin and Postgres
We create a new container running pgadmin which provides a nicer UI that
PGCLI and its further containerized

1.2.4 Dockerizing the ingestion script
ingest.py
Dockerfile
docker build -t taxi_ingest:v001


We automate the ingestion process, once we verify manually it worked.
Instructions to create the an image that a container will be run off,
will be contained and detailed in a Dockerfile saved in the working dir.
**** Remember one thing, anytime the ingest script is modified the image has
to be rebuilt, because the image contains the ingestion script in its last state.


1.2.5 Running Postgres and pgAdmin with Docker-Compose
1) Docker compose used to setup multiple containers in one go,
similar to Infrastructure as code. The settings are composed in a .yaml file.
Basically instead of running multiple terminals with the commands
docker run -it [environment vars] [image]
You put all commands and arguments (image, env, vol, ports) under its associated
setting in a yaml file in the same directory as you woud a docker file (WORKDIR),
name the service which serves multiple proccesses under "services:",
in our example "pg-database", which sets up two processes a postgresql server
and a pgadmin interface.
2) Docker compose comes preinstalled with Docker Desktop, except of Linux
OS versions, requiring a manual download.
3)Command is [Docker compose up], [Docker compose up -d], [Docker compose down]
which looks for the docker-compose.yaml file with instructions in the working directory
it is run from, then instantiates as it would normally with docker run multiple
containers.
4) Docker compose auto creates a network for the containers to work with,
defaults the name as '{working directory}_default'. If u want to name the
network use name: same level of the services key or -p projectname when u run
docker compose up

1.2.6 SQL Refresher
To simplify things I duplicated the the docker file and the ingest script
renamed respectively
Dockerfile_1.2.6_only_zone_data
ingest_1.2.6_only_zone_data.py

The modification to the dockerfile was:

COPY ingest_1.2.6_only_zone_data.py ingest_1.2.6_only_zone_data.py
ENTRYPOINT ["python", "ingest_1.2.6_only_zone_data.py"]

The modification for the new ingestion script was that it omits
all trip data, which I did to simply confirming the zone data pipline from
file to postgres. I confirmed the zone table (ny_taxi_zones) was inserted into
Postgres
with pgadmin.

A) Now merging the two data pipeline is needed with the below mods:
1) Edit name to ingest_1.2.6.py of script to include the taxi zone data
(remember its a csv not gzip).
2) duplicate the docker file and name it Dockerfile_1.2.6
3) edit line 9 ENTRYPOINT to ["python", "ingest_1.2.6.py"]
4) rebuild image with:
    ```
    docker build -f Dockerfile_1.2.6 -t taxi_ingest:v002 .
    added or differentiated:
    trip_table_name = params.trip_table_name
    zone_table_name = params.zone_table_name
    trip_file_name = 'ny_green_taxi_trip.gz'
    zone_file_name = 'zone.csv'
    trip_data_url = params.trip_data_url
    zone_data_url = params.zone_data_url
    ```

    Six parameters we have add or modify: a x 2, b x 2, c x 2
    In ingestion script:
    a) modify the ArgumentParser to add:
    zone data url which which will need a zsh variable as before
    --> parser.add_argument('--zone_data_url', help='url for the csv file')

    --> passed argument --zone_data_url=${zone_data_url}
     b) Differentiate the two tables and modify ingest.py line
    parser.add_argument(
        '--trip_table_name', help='trip table to be written to in postgres')
    parser.add_argument(
        '--zone_table_name', help='zone table to be written to in postgres')
    In zsh:
    c) modify the present url to differentiate the two different urls
    represented by the 2 diff zsh vars:
        i) export trip_data_url='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz'
        to view: echo $trip_data_url
        -->parser.add_argument('--trip_data_url', help='url for the gz file')
        --> passed argument --trip_data_url=${trip_data_url}

        ii) export zone_data_url='https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv'
        to view variable: echo $zone_data_url
    -->parser.add_argument('--zone_data_url', help='url for the csv file')
        --> passed argument --zone_data_url=${zone_data_url}

Confirmed both tables are in postgres thru pgadmin.

5) Verify tables with a simple query

    ```
    SELECT *
    FROM ny_green_taxi_trips
    LIMIT 10
    ```

    ```
    SELECT *
    FROM ny_taxi_zones
    LIMIT 10
    ```

6) Join trip and zone data tables on common id(s), there is 2 columns in trips than need represented but 2 columns respectively in the zones table. So
   technically we need a few joins.
    a) First way:

        ```

            SELECT
            CONCAT(zdo."Borough", '/', zdo."Zone") AS dropoff_location,
            CONCAT(zpu."Borough", '/', zpu."Zone") AS pickup_location,
            trips.trip_type,
            trips.total_amount,
            trips.trip_distance AS distance,
            trips.lpep_pickup_datetime AS pickup_time,
            trips.lpep_dropoff_datetime AS dropoff_time
            FROM
            ny_green_taxi_trips AS trips
            JOIN ny_taxi_zones AS zpu
            ON trips."PULocationID" = zpu."LocationID"
            JOIN ny_taxi_zones AS zdo
            ON trips."DOLocationID" = zdo."LocationID"
            LIMIT 100

        ```

    b) Second way:

        ```

            SELECT
            CONCAT(zdo."Borough", '/', zdo."Zone") AS dropoff_location,
            CONCAT(zpu."Borough", '/', zpu."Zone") AS pickup_location,
            trips.trip_type,
            trips.total_amount,
            trips.trip_distance AS distance,
            trips.lpep_pickup_datetime AS pickup_time,
            trips.lpep_dropoff_datetime AS dropoff_time
            FROM
            ny_green_taxi_trips AS trips
            JOIN ny_taxi_zones AS zpu
            ON trips."PULocationID" = zpu."LocationID"
            JOIN ny_taxi_zones AS zdo
            ON trips."DOLocationID" = zdo."LocationID"

        ```

    c) Save query as a table:
        i) joined_trip_zone_data_2019_09_1st_way:

        ```

            CREATE TABLE joined_trip_zone_data_2019_09_1st_way AS
            SELECT
            CONCAT(zdo."Borough", '/', zdo."Zone") AS dropoff_location,
            CONCAT(zpu."Borough", '/', zpu."Zone") AS pickup_location,
            trips.trip_type,
            trips.total_amount,
            trips.trip_distance AS distance,
            trips.lpep_pickup_datetime AS pickup_time,
            trips.lpep_dropoff_datetime AS dropoff_time
            FROM
            ny_green_taxi_trips AS trips,
            ny_taxi_zones AS zpu,
            ny_taxi_zones AS zdo
            WHERE
            trips."PULocationID" = zpu."LocationID" AND
            trips."DOLocationID" = zdo."LocationID"

        ```

        ii) joined_trip_zone_data_2019_09_2nd_way:

        ```

            CREATE TABLE joined_trip_zone_data_2019_09_2nd_way AS
            SELECT
            CONCAT(zdo."Borough", '/', zdo."Zone") AS dropoff_location,
            CONCAT(zpu."Borough", '/', zpu."Zone") AS pickup_location,
            trips.trip_type,
            trips.total_amount,
            trips.trip_distance AS distance,
            trips.lpep_pickup_datetime AS pickup_time,
            trips.lpep_dropoff_datetime AS dropoff_time
            FROM
            ny_green_taxi_trips AS trips
            JOIN ny_taxi_zones AS zpu
            ON trips."PULocationID" = zpu."LocationID"
            JOIN ny_taxi_zones AS zdo
            ON trips."DOLocationID" = zdo."LocationID"

        ```

    d)  Verify counts of record on each table

        ```

            SELECT COUNT(*)
            FROM joined_trip_zone_data_2019_09_1st_way

        ```

        ```

            SELECT COUNT(*)
            FROM joined_trip_zone_data_2019_09_2nd_way

        ```

    e) Do a few tests:
        i)Checking for records with Location ID not in the zones table



        ii) Checking for Location IDs in the zones table not in the yellow taxi table




