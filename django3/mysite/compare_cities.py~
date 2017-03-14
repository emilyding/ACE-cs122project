# City Comparison

'''
This file produces a list of tuples comparing the relative quality between
different cuisine types in a pair of cities.

Usage: Call compare_cuisines with two cities of interest, as well as paths to
the database used and the list of valid cuisine tags. Filtering by price is
also possible

Example call: compare_cuisines({'city': 'Chicago'}, {'city': 'Kansas City'}, 
    database = "yelp_raw.db", cuisines = "cuisines_tags.csv")
'''

import sqlite3
import csv
import re
from find_yelp_data import find_cuisines 

def compare_cuisines(city1, city2, database = "yelp_raw.db", cuisines = "cuisines_tags.csv"):
    '''
    Creates a list of tuples with restaurant comparisons.

    Inputs:
        - city1: The first city of interest
        - city2: The second city of interest
        - database: Location of yelp data
        - cuisines: Location of csv containing cuisine information

    Returns:
        - A list of tuples containing comparison information
    '''

    with open(cuisines, 'r') as f:
        reader = csv.reader(f)
        cuisine_list = list(reader)

    # Extract cuisine information in usable form
    cuisine_tags = []
    for item in cuisine_list:
        search = re.search(r'^.*(?=\s\()', item[0]).group()
        cuisine_tags.append(search)

    # Find cuisine averages from each city and convert to dictionary
    city1_averages = dict(find_average_cuisine_scores(city1, database))
    city2_averages = dict(find_average_cuisine_scores(city2, database))

    cuisines_compared = []

    # Limit comparisons to results appearing in both cuisine lists
    for cuisine in cuisine_tags:
        if cuisine in city1_averages and cuisine in city2_averages:
            cuisine_difference = city1_averages[cuisine] - city2_averages[cuisine]
            cuisines_compared.append((cuisine, city1_averages[cuisine], 
                city2_averages[cuisine],  cuisine_difference))

    return cuisines_compared


def find_average_cuisine_scores(city, database):
    '''
    Return a list of average rating for each cuisine in a city with 3 or more
    restaurants. 

    Inputs:
        - city: The city of interest
        - database: SQL database storing restaurant information
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()

    search_string = '''SELECT cuisine, AVG(rating) as avg_rating, COUNT(*) as num_restaurants
    FROM restaurant
    JOIN cuisines
    ON restaurant.id = cuisines.id
    WHERE city = ?
    COLLATE NOCASE    
    '''
    
    params = []
    city = city["city"].lower()
    params.append(city)

    # If user specified price ceiling, adjusts table to return cuisines
    # below this average price
    if "price" in city:
        search_string += '''AND price <= ?'''
        price_length = len(city["price"])
        params.append(price_length)

    search_string += '''
    GROUP BY cuisine;
    '''
    
    results = c.execute(search_string, params)
    result_list = results.fetchall()

    # Restrict to cuisines with at least 3 restaurants
    trimmed_entries = []
    for entry in result_list:
        if entry[2] >= 3:
            trimmed_entries.append((entry[0], entry[1]))

    connection.commit()
    c.connection.close()

    return trimmed_entries
