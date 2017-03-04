# City CSV Aggregator

'''
This program takes all yelp_data csv results from a given folder, standardizes
all data, reformats ID's, and appends to a single large pandas dataframe. 
Results are also saved to a csv.

Usage: Call "create_df" with default parameters, or parameters of your own
'''

'''
Note that a very small number of restaurants appear multiple times in the final
data, because they are present in more than one city. This occurs between cities
that are fairly close together (for example, Arlington and Washington DC), whose
"capture radii" overlap. (This is related to the challenge discussed in the find_yelp_data.py
notes). These cities are deliberately not removed - because comparison are being
made between cities, it is reasonable to think that an overlapping restaurant
might be frequented by patrons from either city, and is therefore representative
of either city's cuisine.
'''

# Import relevant modules
import csv
import time
import glob
import re
from operator import itemgetter
import pandas as pd
import numpy as np

def create_df(filepath = "all_restaurants.csv", city_filepath = '*.csv', initial_id = 100000):
    '''
    Creates a dataframe and saves a csv containing restauarant data from all
    valid cities.

    Inputs:
        - filepath: Destination to save csv file to
        - city_filepath: Destination to scan for valid cities
        - initial_id: Starting point for unique id assignments

    Returns:
        - full_df: Pandas dataframe containing all restaurants from all cities
    '''

    # Track run time
    start_time = time.clock()

    # Build city list
    cities = find_all_cities(city_filepath)

    # Create initial dataframe
    full_df_tuple = add_csv_to_df(cities[0], initial_id)
    full_df = full_df_tuple[1]
    unique_id = full_df_tuple[0]

    # Expand dataframe using remaining cities
    for city in cities[1:]:
        df_tuple = add_csv_to_df(city, unique_id)
        unique_id = df_tuple[0]
        full_df = full_df.append(df_tuple[1], ignore_index = True)

    # Save to csv
    full_df.to_csv("filepath")

    # Return run time
    print(time.clock() - start_time, "seconds")

    return full_df

def find_all_cities(filepath = '*.csv'):
    '''
    Finds all csv files in a given directory in the correct format, and trims
    their names to create a list of valid destination cities.

    Inputs:
        - filepath: Directory to search for csv files. Default is current folder

    Returns:
        - cities: A list of strings containing valid cities
    '''

    # Extract list of csv file names
    csvs = glob.glob(filepath)

    # Given proper name format, extract city name and add to list of valid cities
    city_list = []
    for file in csvs:
        if file[:4] == 'yelp':
            search = re.search(r"(?<=yelp_).*(?=.csv)", file).group()
            city_list.append(search)

    return city_list

def add_csv_to_df(city_name, unique_id):
    '''
    Given a csv file, adds all restaurants into a pandas dataframe.

    Note that some data cleaning/reformatting is done here, based on changes
    identified after data scraping. While some of these changes could be made to
    the find_yelp_data.py file, doing so would then require re-scraping all data,
    which takes upwards of a week to do (this function runs in 11 seconds)

    Inputs:
        - city_name: Name of the city to be added
        - unique_id: Running count of ID number associated with each restaurant

    Returns:
        - unique_id: Updated running count of ID number
        - df: A pandas dataframe containing all of the restaurants from the csv
    '''

    restauarant_list = []

    # Given a city, reads in relevant csv file and sorts by address
    with open("yelp_{}.csv".format(format(city_name)), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        sortedreader = sorted(reader, key=itemgetter(8))
        for row in sortedreader:

        	# Skip row of headers
            if row[8] != "Address":
            	# If first entry, append without checking duplicates
                if restauarant_list:
                	# If address and name are identical to previous entry, skip
                    if row[8] == restauarant_list[-1][8] and row[2] == restauarant_list[-1][2]:
                        pass
                    else:
                    	# Cut off first row (pandas indexing parameter)
                        row = row[1:]
                        row[0] = unique_id
                        unique_id += 1
                        # Insert a marker of source file
                        row.insert(1, city_name)
                        restauarant_list.append(row)
                else:
                    row = row[1:]
                    row[0] = unique_id
                    unique_id += 1
                    row.insert(1, city_name)
                    restauarant_list.append(row)

    # Create pandas dataframe with relevant headers
    headers = (["Unique ID", "City", "Name", "Cuisine", "Rating", "Price", "Review Count", 
        "Neighborhood", "Address", "Zip Code", "Phone", "Latitude", "Longitude"])
    df = pd.DataFrame(restauarant_list, columns = headers)

    return unique_id, df

