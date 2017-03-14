import sqlite3
import csv
import string
import math
import matplotlib.pyplot as plt
import statistics as stat
import numpy as np
import pandas as pd
from pandas.tools.plotting import table
from textwrap import wrap

def cuisine_highlights(database = "yelp_adjusted.db"):
    '''
    Gets best cuisines across cities
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()
    
    search_string = '''SELECT cuisine, AVG(rating), SUM(reviews) as num_reviews
    FROM restaurant
    JOIN cuisines
    ON restaurant.id = cuisines.id
    WHERE reviews > 10
    GROUP BY cuisine
    '''

    results = c.execute(search_string)
    result_table = results.fetchall()
    result_table.sort(key = lambda x: x[1], reverse = True)
    best_table = result_table[:10]
    worst_table = result_table[-10:]

    connection.commit()
    c.connection.close()

    # Make dataframe of top 10 cuisines
    best_frame = pd.DataFrame(best_table, 
        columns=["Cuisine", "Rating", "# Reviews"])
    best_frame = best_frame.round(2)
    best_list = best_frame.values.tolist()

    # Make dataframe of worst 10 cuisines
    worst_frame = pd.DataFrame(worst_table, 
        columns=["Cuisine", "Rating", "# Reviews"])
    worst_frame = worst_frame.round(2)
    worst_list = worst_frame.values.tolist()

    graph_cuisine_highlights(best_frame, worst_frame)


def graph_cuisine_highlights(best_frame, worst_frame):
    # Creates bar graph of top cuisines
    low = best_frame["Rating"].min() - .05
    high = best_frame["Rating"].max() + .05

    # Visualizes price to ratings bar graph
    plt.xlabel("Cuisines")
    plt.ylabel("Avg Rating")
    plt.title("Top 10 Cuisines")

    x_ticks = best_frame["Cuisine"].tolist()

    x = [i + .5 for i in range(10)]

    plt.figure(figsize=(13,5))
    plt.xticks(x, x_ticks, rotation = 16)
    plt.bar(x, best_frame["Rating"])
    plt.axis([0, 10.75, low, high])

    # Saves price to ratings graph for "city" as "price_ratings_city.png"
    plt.savefig("best_cuisines.png")
    plt.close("all")

    # Creates bar graph of worst cuisines
    low = worst_frame["Rating"].min() - .05
    high = worst_frame["Rating"].max() + .05

    # Visualizes price to ratings bar graph
    plt.xlabel("Cuisines")
    plt.ylabel("Avg Rating")
    plt.title("10 Worst Cuisines")

    x_ticks_unformatted = worst_frame["Cuisine"].tolist()
    x_ticks = []
    for tick in x_ticks_unformatted:
        tick.replace("American", "American\n")
        tick.replace("Conveyor", "Conveyor\n")
        x_ticks.append(tick)

    x = [i + .5 for i in range(10)]

    plt.figure(figsize=(10,8))
    plt.gcf().subplots_adjust(bottom=0.25)
    plt.xticks(x, x_ticks, rotation = 'vertical', horizontalalignment = 'left')
    plt.gca().tick_params(axis='x', pad=10)
    #plt.setp(plt.gca().get_xticklabels(), horizontalalignment='left')
    plt.bar(x, worst_frame["Rating"])
    plt.axis([0, 10.75, low, high])

    # Saves price to ratings graph for "city" as "price_ratings_city.png"
    plt.savefig("worst_cuisines.png")
    plt.close("all")


def price_ratings(database = "yelp_raw.db"):
    '''
    Gets avg ratings for each price category for all cities
    Creates and saves two plots: graph of avg ratings by price category, pie chart
    showing number of restaurants in each price category
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()
    
    search_string = '''SELECT price, AVG(rating) as avg_rating, 
    COUNT(*) as num_restaurants, SUM(reviews) as num_reviews
    FROM restaurant
    WHERE reviews > 10
    GROUP BY price
    '''

    results = c.execute(search_string)
    result_table = results.fetchall()

    format_price_table = []

    for entry in result_table:
        if entry[0]:
            # Turns price from float to $
            price = math.ceil(float(entry[0])) * "$"
            format_price_table.append([price, entry[1], entry[2], entry[3] / entry[2]])

    connection.commit()
    c.connection.close()

    result_frame = pd.DataFrame(format_price_table, columns=["Price", "Rating", "# Restaurants", "Avg Reviews Per Restaurant"])
    result_frame = result_frame.round(2)
    length = len(result_frame.index)

    # Creates bar chart of normalized ratings for top cities
    low = result_frame["Rating"].min() - .2
    high = result_frame["Rating"].max() + .2

    # Visualizes price to ratings bar graph
    plt.xlabel("Price")
    plt.ylabel("Avg Rating")
    plt.title("Avg Rating by Price Bracket")
    total = result_frame["# Restaurants"].sum()

    max_price = length
    x_ticks = []

    # Creates $ labels (if not escaped with \, creates error)
    for i in range(max_price):
        x_ticks.append((i + 1) * "\$")

    x = [i + 1 for i in range(max_price)]

    plt.xticks(x, x_ticks)
    plt.plot(x, result_frame["Rating"], 'ro')
    plt.axis([0, 5, low, high])

    # Saves price to ratings graph for "city" as "price_ratings_city.png"
    plt.savefig("price_ratings_all_cities.png")
    plt.close("all")

    # Visualizes number of restaurants per price bracket as a pie graph
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    plt.pie(result_frame["# Restaurants"], labels=x_ticks, colors=colors, 
        autopct=lambda p: '{:.0f}'.format(p * total / 100), startangle=0)
    plt.axis('equal')

    # Saves price to num_restaurants graph asfor "city" as "price_restaurants_city.png"
    plt.savefig("price_restaurants_all_cities.png")
    plt.close('all')

    # Creates bar chart of avg # reviews per restaurant per price bracket
    low = result_frame["Avg Reviews Per Restaurant"].min() - 10
    high = result_frame["Avg Reviews Per Restaurant"].max() + 10

    # Visualizes price to ratings bar graph
    plt.xlabel("Price")
    plt.ylabel("Avg Reviews per Restaurant")
    plt.title("Avg Reviews / Restaurant per Price Bracket")

    x = [i + 1 for i in range(length)]

    plt.xticks(x, x_ticks)
    plt.plot(x, result_frame["Avg Reviews Per Restaurant"], 'ro')
    plt.axis([0, length + 1, low, high])

    # Saves price to ratings graph for "city" as "price_ratings_city.png"
    plt.savefig("price_reviews_all_cities.png")
    plt.close("all")

    return format_price_table

def star_reviews(database = "yelp_raw.db"):
    '''
    Gets avg ratings for each star category for all cities
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()
    
    search_string = '''SELECT rating, COUNT(*) as num_restaurants, SUM(reviews) as num_reviews
    FROM restaurant
    WHERE reviews > 10
    GROUP BY rating
    '''
    
    results = c.execute(search_string)
    result_table = results.fetchall()

    connection.commit()
    c.connection.close()

    # Gets average # reviews per restaurant
    for index, result in enumerate(result_table):
        avg_num_reviews = result[2] / result[1]
        result_table[index] = [result[0], result[1], avg_num_reviews]
    
    result_frame = pd.DataFrame(result_table, 
        columns=["Rating", "# Restaurants", "Avg Reviews Per Restaurant"])
    result_frame = result_frame.round(2)
    result_list = result_frame.values.tolist()
    
    # Undoes the side effect of calling values to list, which turns # Restaurants
    # into floats
    for index, result in enumerate(result_list):
        result[1] = int(result[1])
        result_list[index] = result

    length = len(result_frame.index)

    # Creates bar chart of avg # reviews per restaurant per rating across cities
    low = result_frame["Avg Reviews Per Restaurant"].min() - 10
    high = result_frame["Avg Reviews Per Restaurant"].max() + 10

    # Visualizes price to ratings bar graph
    plt.xlabel("Rating")
    plt.ylabel("Avg Reviews per Restaurant")
    plt.title("Avg Reviews / Restaurant per Rating")

    x_ticks = result_frame["Rating"].values.tolist()
    x = [i + 1 for i in range(length)]

    plt.xticks(x, x_ticks)
    plt.plot(x, result_frame["Avg Reviews Per Restaurant"], 'ro')
    plt.axis([0, length + 1, low, high])

    # Saves price to ratings graph for "city" as "price_ratings_city.png"
    plt.savefig("star_reviews_all_cities.png")
    plt.close("all")

    # Visualizes number of restaurants per price bracket as a pie graph
    total = result_frame["# Restaurants"].sum()
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    plt.pie(result_frame["# Restaurants"], labels=x_ticks, colors=colors, 
        autopct=lambda p: '{:.0f}'.format(p * total / 100), startangle=0)
    plt.axis('equal')

    # Saves price to num_restaurants graph asfor "city" as "price_restaurants_city.png"
    plt.savefig("star_restaurants_all_cities.png")
    plt.close('all')

    return result_list