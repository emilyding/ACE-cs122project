# Yelp API Retriever

'''
This program extracts yelp restaurant data from a particular city, and both
creates a pandas dataframe and saves the information to a formatted csv file.
Each restaurant is saved with unique_id, name, cuisines, rating, price, 
# of reviews, city, address, zip code, phone number, latitude, and longitude.  

To use, call find_restaurants_in_city, after supplying yelp credentials and
saving a file destination for cuisine tags. 

'''

# Defaults for testing
#filepath = "yelp_cuisines.csv"
#f = yelp.search(term = "restaurant", price = "3", categories = "mexican", location='chicago', limit=1)
# sample_cuisines = ["afghani", "austrian"]

# Imports
from yelp.api.v3 import Yelp
import pandas as pd
import numpy as np
import csv
import re

# Load Yelp credentials
# OAuth credential placeholders that must be filled in by users.
# You can find them on
# https://www.yelp.com/developers/v3/manage_app
app_id = 'rVkxCbS3vszyTTHgSdPRJA'
app_secret = 'xB5UJmXyLKyYTO4uKUl1TluKTGiiCnYnaCjCiv2dyvSc6Jfuh0s1xm4g27NbNZRA'
yelp = Yelp(
    app_id,
    app_secret,
)

def find_restaurants_in_city(city, filepath):
    '''
    Finds all restauarants within a city, and creats a csv and pandas dataframe
    with all relevant information

    Inputs:
        - city: The city of interest
        - filepath: Location of cuisine tag csv
    '''

    # Create blank lists and set defaults
    info_list = []
    used_cuisines = []
    unique_id = 100000
    cuisine_tags = find_cuisines(filepath)
    #cuisine_tags = ["afghani", "arabian", "burmese"]

    # For each cuisine tag, search all matching restaurants
    for tag in cuisine_tags:
        return_dict = yelp.search(term = "restaurant", categories = tag, 
            location = city, limit = 50)
        
        # If fewer than 1000 entries, chunk
        if return_dict["total"] <= 1000:
            (info_list, unique_id) = add_restaurants(return_dict, info_list, 
                used_cuisines, tag, city, unique_id)

        # Otherwise, try to filter by price
        else:
            return_dict = yelp.search(term = "restaurant", categories = tag, 
                price = "1", location = city, limit = 50)
            (info_list, unique_id) = add_restaurants(return_dict, info_list, 
                used_cuisines, tag, city, unique_id)
            return_dict = yelp.search(term = "restaurant", categories = tag, 
                price = "2", location = city, limit = 50)
            (info_list, unique_id) = add_restaurants(return_dict, info_list, 
                used_cuisines, tag, city, unique_id)
            return_dict = yelp.search(term = "restaurant", categories = tag, 
                price = "3", location = city, limit = 50)
            (info_list, unique_id) = add_restaurants(return_dict, info_list, 
                used_cuisines, tag, city, unique_id)
            return_dict = yelp.search(term = "restaurant", categories = tag, 
                price = "4", location = city, limit = 50)
            (info_list, unique_id) = add_restaurants(return_dict, info_list, 
                used_cuisines, tag, city, unique_id)

        # Append used cuisine, for filtering of future returns
        used_cuisines.append(tag)


    # Convert to pandas dataframe
    headers = (["Unique ID", "Name", "Cuisine", "Rating", "Price", "Review Count", 
    	"City", "Address", "Zip Code", "Phone", "Latitude", "Longitude"])
    df = pd.DataFrame(info_list, columns = headers)

    # Save to csv
    df.to_csv("yelp_{}.csv".format(city))

    return df

def find_cuisines(filepath):
    '''
    Reads a csv copied from yelp's category_list for v3, found here:
    https://www.yelp.com/developers/documentation/v3/category_list
    and converts to a usable list of string tags.

    Inputs:
        - filepath: Filepath for the location of the csv

    Returns:
        - cuisine_tags: A list of strings
    '''

    # Open csv
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        cuisine_list = list(reader)

    # Translate to usable form
    cuisine_tags = []
    for item in cuisine_list:
        search = re.search(r'\((.*?)\)', item[0]).group()[1:-1]

        # Creates exceptions for American (New) and American (Traditional) due
        # to their unique formatting
        if search == "New":
            search = "newamerican"
        if search == "Traditional":
            search = 'tradamerican'

        cuisine_tags.append(search)

    return cuisine_tags

def add_restaurants(return_dict, info_list, used_cuisines, tag, city, unique_id):
    '''
    Given a return_dict, chunks the results into usable groups of 50, and
    appends necessary information to info_list

    Inputs:
        - return_dict: Dictionary returned by the api call
        - info_list: A list of lists holding restaurant information
        - used_cuisines: A list of all cuisines already checked
        - tag: The cuisine being searched
        - city: The city of interest
        - unique_id: An integer assigning a unique identifier to each entry

    Returns:
        - info_list: Updated list of lists containing restaurant information
    '''

    # Chunks and counts
    chunk_count = (return_dict["total"] // 50) + 1

    # Yelp cuts off results at 1000, so searches cannot exceed (19*50) + 50
    if chunk_count > 19:
        chunk_count = 19
        
    # Creates sub-searches based on each chunk
    for i in range(chunk_count):
        return_dict = yelp.search(term = "restaurant", categories = tag, 
               location = city, limit = 50, offset = 50 * i)
        (info_list, unique_id) = append_restaurant_info(return_dict, info_list, used_cuisines, unique_id)

    return (info_list, unique_id)

def append_restaurant_info(return_dict, info_list, used_cuisines, unique_id):
    '''
    Given a call result, extracts information from each business and appends to
    a running info list.

    Inputs:
        - return_dict: Dictionary returned by the api call
        - info_list: A list of lists holding restaurant information
        - used_cuisines: A list of all cuisines already checked
        - unique_id: An integer assigning a unique identifier to each entry

    Returns:
        - info_list: Updated list of lists containing restaurant information
    '''

    for i in range(len(return_dict["businesses"])):
        # Creates necessary holding lists
        info_holding = []
        cuisine_holding = []
        cuisine_alias = []

        # Creates a list of cuisine tags, and ensures none have been used (prevents duplicates)
        for j in range(len(return_dict["businesses"][i]["categories"])):
            cuisine_alias.append(return_dict["businesses"][i]["categories"][j]["alias"])
        if not bool(set(cuisine_alias) & set(used_cuisines)):

            # Increment and append unique_id
            info_holding.append(unique_id)
            unique_id += 1

            info_holding.append(return_dict["businesses"][i]["name"])

            # Translates all cuisine tags into a single list, appends at once
            for j in range(len(return_dict["businesses"][i]["categories"])):
                cuisine_holding.append(return_dict["businesses"][i]["categories"][j]["title"])
            info_holding.append(cuisine_holding)

            info_holding.append(return_dict["businesses"][i]["rating"])

            # Appends price, unless key is absent
            try:
                info_holding.append(return_dict["businesses"][i]["price"])
            except KeyError:
                info_holding.append("N/A")

            info_holding.append(return_dict["businesses"][i]["review_count"])
            info_holding.append(return_dict["businesses"][i]["location"]["city"])

            # If address is present, appends
            if return_dict["businesses"][i]["location"]["address1"] != "":
                info_holding.append(return_dict["businesses"][i]["location"]["address1"])
            else:
                info_holding.append("N/A")

             # If zip code is present, appends
            if return_dict["businesses"][i]["location"]["zip_code"] != "":
                info_holding.append(return_dict["businesses"][i]["location"]["zip_code"])
            else:
                info_holding.append("N/A")

            # If phone number is present, appends
            if return_dict["businesses"][i]["phone"] != "":
                info_holding.append(return_dict["businesses"][i]["phone"])
            else:
                info_holding.append("N/A")

            # Check for latitude and longitude
            if return_dict["businesses"][i]["coordinates"]["longitude"] != "":
                info_holding.append(return_dict["businesses"][i]["coordinates"]["longitude"])
                info_holding.append(return_dict["businesses"][i]["coordinates"]["latitude"])
            else:
                info_holding.append("Mobile Business")
                info_holding.append("Mobile Business")

            info_list.append(info_holding)

            # Prints progress through city
            print('Finished {} Restaurant(s)'.format(len(info_list)))
            print(cuisine_holding)
        
    return info_list, unique_id