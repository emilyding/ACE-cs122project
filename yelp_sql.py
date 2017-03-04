import sqlite3
import itertools
import copy 
import csv
import string
import math

def get_city_ratings(city_ratings_file = "city_ratings.csv"):
    '''
    Gets average city ratings from csv file. NOTE: must run get_city_ratings
    from yelp_constants.py
    '''
    city_ratings = {}
    data_csv = csv.reader(open(city_ratings_file, newline=''), delimiter=',')
    all_city_rating = 0
    
    for index, row in enumerate(data_csv):
        if index != 0:
            city_ratings[row[0]] = float(row[1])
            all_city_rating = all_city_rating + float(row[1])

    all_city_rating = all_city_rating / len(city_ratings.keys())
    city_ratings["avg"] = all_city_rating

    return city_ratings

city_ratings = get_city_ratings("city_ratings.csv")


def get_top_cities(query, database):
    '''
    Returns top cities for a cuisine, normalized by avg city ratings so that
    reviews across cities are comparable
    '''
    # Dict mapping city names to avg city ratings
    city_ratings

    connection = sqlite3.connect(database)
    c = connection.cursor()
    
    search_string = '''SELECT city, AVG(rating) as avg_rating 
    FROM restaurant
    JOIN cuisines
    ON restaurant.id = cuisines.id
    WHERE cuisines.cuisine = ?
    GROUP BY city
    '''
    
    params = []
    cuisine = query["cuisine"]
    params.append(cuisine)

    results = c.execute(search_string, params)
    result_table = results.fetchall()

    connection.commit()
    c.connection.close()

    top_cities_table = []

    for row in result_table:
        row = list(row)

        # Normalizes ratings across cities
        row[1] = row[1] * city_ratings["avg"] / city_ratings[row[0]]
        top_cities_table.append(row)
    
    top_cities_table.sort(key=lambda x: x[1], reverse = True)
    
    if "limit" in query:
        print("here")
        return top_cities_table[:query["limit"]]
        
    else:
        print("there")
        return top_cities_table
        
    
def get_top_cuisines(query, database):
    '''
    Get top cuisines for a city, discounts restaurants with < 10 reviews and > 5 restaurants
    Required: city name
    Optional: price ceiling, limit of # cuisines returned

    Inputs:
        - query (dict): maps possible queries (city, price) to list of user inputs
          example query:
          query = {"city": "chicago",
                   "price": "$$$",
                   "limit": 10}
        - database
    '''
    connection = sqlite3.connect(database)
    c = connection.cursor()

    search_string = '''SELECT cuisine, AVG(price) as avg_price, AVG(rating) as avg_rating, 
    COUNT(*) as num_restaurants, SUM(reviews) as num_reviews
    FROM restaurant
    JOIN cuisines
    ON restaurant.id = cuisines.id
    WHERE city = ?
    AND reviews > 10
    '''
    
    params = []
    city = query["city"]
    params.append(city)

    # If user specified price ceiling, adjusts table to return cuisines
    # below this average price
    if "price" in query:
        search_string += '''AND price <= ?'''
        price_length = len(query["price"])
        print(price_length)
        params.append(price_length)

    if "worst" in query:
        search_string += '''GROUP BY cuisine
        ORDER BY rating ASC
        '''

    else:
        search_string += '''GROUP BY cuisine
        ORDER BY rating DESC
        '''

    # If user wanted top n results, limits # results to n
    if "limit" in query:
        search_string += '''LIMIT ?;'''
        params.append(query["limit"])
    else:
        search_string += ''';'''
    
    results = c.execute(search_string, params)
    result_table = results.fetchall()

    # Formats prices and ensures cuisines have > 5 restaurants
    format_price_table = []
    for entry in result_table:
        # Turns prices from floats (rounded up since they will always be capped by 
        # price ceiling) to dollar sign characters
        entry = list(entry)
        entry[1] = math.ceil(entry[1]) * "$"

        # Restricts to cuisines with > 5 restaurants
        if entry[3] > 5:
            format_price_table.append(entry)

    connection.commit()
    c.connection.close()

    return (["Cuisine", "Price", "Rating", "# Restaurants", "Total Reviews"], format_price_table)


def all_cuisines(query, database):
    '''
    Get all cuisine types for a city from database

    Inputs:
        - query (dict): maps city name to all available cuisines
            example query:
            query = {"city": "chicago"}
        - database

    Output:
        - alphabetized list of cuisines
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()
    
    search_string = '''SELECT DISTINCT cuisine
    FROM cuisines
    JOIN restaurant
    ON restaurant.id = cuisines.id
    WHERE city = ?
    '''
    
    params = []
    city = query["city"]
    params.append(city)

    results = c.execute(search_string, params)
    result_table = results.fetchall()
    cuisine_table = []

    # Take out of form [("cuisine",)] to form ['cuisine']
    for result in result_table:
        cuisine_table.append(result[0])

    connection.commit()
    c.connection.close()

    return sorted(cuisine_table)


def do_calculations(inputs):
    words
    return results