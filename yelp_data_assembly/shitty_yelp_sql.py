# My own calls

import sqlite3
import csv
import string
import math
import matplotlib.pyplot as plt
import statistics as stat
import numpy as np
import pandas as pd
from pandas.tools.plotting import table

def build_starbucks_dictionary(filepath = 'starbucks_index.csv'):
    '''
    Given a filepath, constructs a dictionary mapping each city to the
    median minimum distance to another Starbucks. Used in get_summary_info.

    Inputs:
        - filepath: The location of the Starbucks distance csv

    Returns:
        - Dictionary mapping cities to the median min starbucks distance
    '''
    starbucks_mapper = {}

    with open(filepath) as holding:
        reader = csv.reader(holding)
        for row in reader:
        	if row[2] != "Median Distance":
        	   starbucks_mapper.update({row[1]: "{0:.2f}".format(float(row[2]))})

    return starbucks_mapper




def get_summary_info(database, city = {'city': 'Chicago'}):
    '''
    Takes in a city in a dictionary and returns each of the following:

    - Total number of restaurants in the city
    - Starbucks Index for the city
    - Average rating in the city (% of national rating; national rating)
    - Most reviewed restaurant
    - Best Restaurant (>100 reviews)
    - Worst Restaurant (>50 reviews)

    Returns like a tuple I guess, what am i a psychic
    '''

def find_total_restaurants(database = "yelp_raw.db", city = {'city': 'Chicago'}):
    '''
    Finds total number of restauarants
    '''
 
    connection = sqlite3.connect(database)
    c = connection.cursor()

    search_string = '''SELECT COUNT(*)
    FROM restaurant
    WHERE city = ?
    COLLATE NOCASE
    '''
    params = [city["city"].lower()]

    result = c.execute(search_string, params)
    result = result.fetchone()

    connection.commit()
    c.connection.close()

    return result[0]



def get_top_cuisines(query, database = "yelp_raw.db"):


    connection = sqlite3.connect(database)
    c = connection.cursor()

    search_string = '''SELECT cuisine, AVG(price) as avg_price, AVG(rating) as avg_rating, 
    COUNT(*) as num_restaurants, SUM(reviews) as num_reviews
    FROM restaurant
    JOIN cuisines
    ON restaurant.id = cuisines.id
    WHERE city = ?
    COLLATE NOCASE
    '''
    
    params = []
    city = query["city"].lower()
    params.append(city)

    # If user specified price ceiling, adjusts table to return cuisines
    # below this average price
    if "price" in query:
        search_string += '''AND price <= ?'''
        price_length = len(query["price"])
        params.append(price_length)

    search_string += '''
    GROUP BY cuisine;
    '''
    
    results = c.execute(search_string, params)
    result_table = results.fetchall()

    connection.commit()
    c.connection.close()

    if query["worst"]:
        result_table.sort(key = lambda x: x[2])
    else:
        result_table.sort(key = lambda x: x[2], reverse = True)

    # Formats prices and ensures cuisines have > 10 restaurants
    format_price_table = []
    
    if "limit" in query:
        limit = query["limit"]
    else:
        limit = 10
    count = 0
    
    for entry in result_table:
        if count < limit:
            # Turns prices from floats (rounded up since they will always be capped by 
            # price ceiling) to dollar sign characters
            entry = list(entry)
            entry[1] = math.ceil(entry[1]) * "\$"

            # Restricts to cuisines with > 10 restaurants
            if entry[3] > 10:
                # Get relative rating compared to other cities
                sd, mean = special_cuisine(entry[0])
                if math.fabs(entry[2] - mean) <= sd:
                    special = "average"
                elif entry[2] - mean > 0:
                    special = "good"
                else:
                    special = "bad"
                entry.append(special)
                format_price_table.append(entry)
                count += 1
        else:
            break

    result_frame = pd.DataFrame(format_price_table, 
        columns=["Cuisine", "Price", "Rating", "# Restaurants", "Total Reviews", "All Cities Comparison"])
    result_frame = result_frame.round(2)
    result_frame["Cuisine"] = result_frame["Cuisine"].str.title() # Capitalize city names
    length = len(result_frame.index)

    bar_frame = result_frame.head(min(limit, 10))

    # Creates bar chart of normalized ratings for top cities
    low = bar_frame["Rating"].min() - .2
    high = bar_frame["Rating"].max() + .2
    plt.ylim(low, high)

    x = [i for i in range(length)]
    plt.xlim(min(x) - .1, max(x) + .9)
    plt.bar(x, bar_frame["Rating"])
    plt.xticks(x, bar_frame["Cuisine"], rotation = 16)

    plt.ylabel('Rating')
    plt.title('Top Cuisines for ' + city.title())
    
    # Saves plot to top_cities_cuisine.png
    plt.savefig('top_cuisines_' + city + '.png')
    plt.close("all")
    
    result_frame.index = [i + 1 for i in range(length)]

    fig, ax = plt.subplots(figsize=(12, 5)) # set size frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis
    ax.set_frame_on(False)
    tabla = table(ax, result_frame, loc='center', colWidths=[0.17]*len(result_frame.columns))  # where df is your data frame
    tabla.auto_set_font_size(False) # Activate set fontsize manually
    tabla.set_fontsize(12) # if ++fontsize is necessary ++colWidths
    tabla.scale(1.2, 1.2) # change size table

    plt.savefig(city + "_table.png")
    plt.show()
    plt.close("all")

    return result_frame