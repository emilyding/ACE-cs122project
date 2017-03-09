# Get Starbucks from cities

'''
This file retrieves latitude/longitude pairs for all Starbucks in each of the
cities available in the data, and saves to a csv. This data is used to construct
the "Starbucks index" of average minimum distance necessary to find another Starbucks
in each city.

Usage: Call get_all_starbucks with either the default parameters or custom locations.
Note that ingest_data.py must be in the same folder (or the import path must be changed)

This is cutting edge technology for caffeine addicts everywhere
'''

# Retrieve necessary imports
from ingest_data import find_all_cities
import glob
from yelp.api.v3 import Yelp
import pandas as pd
import numpy as np
import csv

# Load Yelp Credentials. Detailed explained in find_yelp_data.py
app_id = 'rVkxCbS3vszyTTHgSdPRJA'
app_secret = 'xB5UJmXyLKyYTO4uKUl1TluKTGiiCnYnaCjCiv2dyvSc6Jfuh0s1xm4g27NbNZRA'
yelp = Yelp(
    app_id,
    app_secret,
)


def get_all_starbucks(filepath = '*.csv', filename = "starbucks_locations.csv"):
    '''
    Create a csv of all the lat/long pairs for all Starbucks in each city

    Inputs:
        - filepath: The folder to search for city data files
        - filename: The name of the csv to hold Starbucks data

    Returns:
        - df: A pandas dataframe (a csv is also saved)
    '''

    # Construct a list of all cities used for the data
    #city_list = find_all_cities(filepath)
    city_list = ["topeka"]

    # Construct a blank list
    info_list = []

    for city in city_list:
        # Find total number of Starbucks in a city
        return_dict = yelp.search(term = "Starbucks", location = city, limit = 50)

        # Chunk results, as described in find_yelp_data.py
        chunk_count = (return_dict["total"] // 50) + 1
        if chunk_count > 19:
            chunk_count = 19

        # Creates necessary sub-searches
        for i in range(chunk_count):
            return_dict = yelp.search(term = "Starbucks", 
                location = city, limit = 50, offset = 50 * i)

            info_list = append_location_info(city, return_dict, info_list)

    # Convert to pandas dataframe
    headers = (["City", "Latitude", "Longitude", "Review Count"])
    df = pd.DataFrame(info_list, columns = headers)
    df_unique = df.drop_duplicates()
    del df_unique["Review Count"]

    # Save to csv
    df_unique.to_csv(filename)

    return df_unique


def append_location_info(city, return_dict, info_list):
    '''
    Use results from a search to retrieve latitude and longitude information
    for Starbucks returned by the search.

    Inputs:
        - city: The city being searched (used for labelling the eventual csv)
        - return_dict: The dictionary returned by the Yelp API call
        - info_list: The list to add location tuples to

    Returns:
        - info_list: An updated list of Starbucks locations
    '''

    for i in range(len(return_dict["businesses"])):
        # Create holding list
        info_holding = [city]

        # Check for latitude and longitude
        if return_dict["businesses"][i]["coordinates"]["longitude"] != "":
            info_holding.append(return_dict["businesses"][i]["coordinates"]["latitude"])
            info_holding.append(return_dict["businesses"][i]["coordinates"]["longitude"])
            info_holding.append(return_dict["businesses"][i]["review_count"]) 

            info_list.append(info_holding)

        # Update on progress
        print('Finished {} Starbucks'.format(len(info_list)))

    return info_list
      

