\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\###########################\
\### Yelp Data Assembly ####\
\###########################\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

Files in this folder are used to scrape, aggregate, and build databases for the
information used in our aggregator. A full listing of all files, as well as
explanations of their purpose, can be found below. Please note that each .py file
includes summary information and usage instructions at the beginning of the file as well.

.py Files:
find_yelp_data.py
aggregate_city_data.py
build_yelp_databases.py
find_starbucks.py
distance_finder.py

.csv Files:
all_restaurants.csv
city_ratings.csv
starbucks_locations.csv
starbucks_index.csv

.db Files:
yelp_raw.db
yelp_adjusted.db

.7z Files:
city_level_data.7z


Python Files:

find_yelp_data.py: Code in this file uses user-supplied Yelp API credentials to
create a csv holding all necessary restaurant information for a particular city.
The data zipped into city_level_data.7z was created with this function. 

aggregate_city_data.py: Code in this file converts all city-level Yelp data in
a single folder to an aggregated csv. Misc. data cleaning is also done here. 
all_restaurants.csv is produced by this file.

build_yelp_databases.py: Code in this file constructs 2 SQL databases (yelp_raw.db
and yelp_adjusted.db) and a csv (city_ratings.csv) from the all_restaurants.csv file.

find_starbucks.py: Code in this file constructs starbucks_locations.csv, which
holds the city and lat, long pair for every Starbucks in each of the cities in
our dataset. 

distance_finder.py: Code in this file maps the Starbucks lat, long pairs for
each city onto a 3d plane and calculates the median minimum distance between 
Starbucks for each Starbucks in the city. 

Zip Files:

city_level_data.7z: This zip file holds a folder with each city's individual csv.


If a user wanted to construct our databases from scratch, the following steps would be necessary:
- Run find_yelp_data.py for all cities of interest
- Run aggregate_city_data.py in the folder the previous results were saved to
- Run build_yelp_databases.py on the all_restaurants.csv file to produce the databases
- Run find_starbucks.py in the folder find_yelp_data.py saved results to
- Run distance_finder.py on the csv produced by find_starbucks.py