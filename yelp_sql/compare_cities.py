# City Comparison

'''
This file produces a list of tuples comparing the relative quality between
different cuisine types in a pair of cities.

Usage: Call compare_cuisines with two cities of interest, as well as paths to
the database used and the list of valid cuisine tags. Filtering by price is
also possible

Example call: compare_cities('chicago', 'new york', database = "yelp_raw.db", 
cuisines = "cuisines_tags.csv", results = 5)
'''

import sqlite3
import csv
import re
from find_yelp_data import find_cuisines 
import pandas as pd 
import numpy as np 
import matplotlib as plt

def compare_cities(city1, city2, database = "yelp_adjusted.db", cuisines = "cuisines_tags.csv",
        results = 5):
    '''
    Compare the cuisines in two cities, creating a Pandas dataframe containing
    the relative strength of each city's cuisine, ranked. Also produces graphs
    displaying outlier information.

    Inputs:
        - city1: String of first city of interest
        - city2: String of second city of interest
        - database: SQL Database containing restaurant information
        - cuisines: Source file for cuisine information (adds efficiency to comparisons)
        - results: Number of results to display on graph

    Returns:
        - A graph showing relative cuisine ranking in each city, a pandas dataframe
    '''

    # Convert city input to dictionary
    city1 = {'city': '{}'.format(city1)}
    city2 = {'city': '{}'.format(city2)}

    cuisines_compared = compare_cuisines(city1, city2, database, cuisines)

    # Build Pandas dataframes
    headers = (["Cuisine", "{} Rating".format(city1['city'].title()), 
        "{} Rating".format(city2['city'].title()), "Difference"])
    df = pd.DataFrame(cuisines_compared, columns = headers)
    df = df.sort_values(["Difference"])
    
    # Make graphs
    make_graph(city1, city2, df, 'first', results)
    make_graph(city1, city2, df, "second", results)

    return df

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

def make_graph(city1, city2, df, favored, results):
    '''
    Creates a graph for the 5 cuisines with the largest differential favoring
    one of two cities.

    Inputs:
        - city1: Dictionary containing first city of interest
        - city2: Dictionary containing second city of interest
        - df: Pandas dataframe returned by comparison_tables
        - favored: Which city to 'favor' in the graph (i.e, show best cuisines from)
        - results: number of results to display

    Returns:
        - A graph showing relative cuisine ranking in each city
    '''
    
    # Choose parameters of graph based on which city is favored
    if favored == 'first':
        favored_city = city1['city'].title()
        entries = df.tail(n = results)
        # Sort from lowest to highest
        entries = entries.iloc[::-1]
    else:
        favored_city = city2['city'].title()
        entries = df.head(n = results)
    best_a = g.tail(n = results)
    
    # Construct lists of information to graph
    city_a_ratings = []
    city_b_ratings = []
    cuisines = []
    for rating in entries["{} Rating".format(city1['city'].title())]:
        city_a_ratings.append(rating)
    for rating in entries["{} Rating".format(city2['city'].title())]:
        city_b_ratings.append(rating)
    for cuisine in entries["Cuisine"]:
        cuisines.append('{}'.format(cuisine))
    
    # Create plot
    ind = np.arange(results) 
    width = 0.35       
    
    fig, ax = plt.subplots()
    first_city = ax.bar(ind, city_a_ratings, width, color='c')
    second_city = ax.bar(ind + width, city_b_ratings, width, color='m')
    
    # Add some text for labels, title and axes ticks
    ax.set_ylabel('Average Rating')
    ax.set_title('Cuisines with biggest improvement in {}'.format(favored_city))
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(cuisines, rotation = 30)
    ax.legend((first_city[0], second_city[0]), ('{}'.format(city1['city'].title()), '{}'.format(city2['city'].title())))
