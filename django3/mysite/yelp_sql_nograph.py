import sqlite3
import csv
import string
import math
import statistics as stat

def get_top_cities(query, database = "yelp_adjusted.db"):
    '''
    Returns top cities for a cuisine, normalized by avg city ratings so that
    reviews across cities are comparable

    Required: cuisine
    Optional: limit of # cities returned (default 10)

    Inputs:
        - query (dict): maps city name to all available cuisines
            example query:
            query = {"cuisine": "Mexican",
                     "limit": 20}

    Output:
        - list of tuples
          [0]: city name
          [1]: average rating
          [2]: number of restaurants of that cuisine in the city
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()
    
    search_string = '''SELECT city, AVG(rating) as avg_rating, 
    COUNT(*) as num_restaurants 
    FROM restaurant
    JOIN cuisines
    ON restaurant.id = cuisines.id
    WHERE cuisines.cuisine = ?
    COLLATE NOCASE
    GROUP BY city
    '''
    
    params = []
    cuisine = query["cuisine"]
    params.append(cuisine)

    results = c.execute(search_string, params)
    result_table = results.fetchall()

    connection.commit()
    c.connection.close()

    result_table.sort(key = lambda x: x[1], reverse = True)

    if "limit" in query:
        limit = query["limit"]
    else:
        limit = 10
    
    result_table = result_table[:limit]
    result_list = []
    for result in result_table:
        result = list(result)
        result[1] = round(result[1], 2)
        result[0] = result[0].title()
        result_list.append(result)

    return result_list
        
    
def get_top_cuisines(query, database = "yelp_raw.db"):
    '''
    Get top cuisines for a city (or worst if "worse" is specified), 
    restricts to restaurants with >= 5 reviews and cuisines with >= 10 restaurants
    
    Required: city name, price ceiling, limit of # cuisines returned (default 10), 
        worst (boolean specifying best or worst cuisines)

    Inputs:
        - query (dict): maps possible queries (city, price) to list of user inputs
          example_query = {"city": "chicago",
                           "price": "$$$",
                           "limit": 10,
                           "worst": True}
        - database name
    Ouput:
        - list of lists
          [0]: list of headers
          [1]: list of lists, each entry is one cuisine type
    '''

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

    if "limit" in query:
        limit = query["limit"]
    else:
        limit = 10

    result_table = result_table[:limit]
    result_list = []
    for result in result_table:
        result = list(result)
        result[1] = round(result[1], 2)
        result[0] = result[0].title()
        result_list.append(result)

    return result_list


def format_cuisine_table(limit, result_table):
    '''
    Formats prices and ensures cuisines have > 10 restaurants
    '''

    format_price_table = []
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
                sd, mean = cuisine_stats(entry[0])
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

    return format_price_table


def star_reviews(query, database = "yelp_raw.db"):
    '''
    Gets avg reviews per restaurant for each star category for a city

    Inputs:
        - query (dict): contains desired city name
            example query:
            query = {"city": "chicago"}
        - database

    Output:
        - list of lists: [rating, # restaurants, avg # reviews / restaurant]
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()
    
    search_string = '''SELECT rating, COUNT(*) as num_restaurants, SUM(reviews) as num_reviews
    FROM restaurant
    WHERE city = ?
    COLLATE NOCASE
    AND reviews > 10
    GROUP BY rating
    '''
    
    params = []
    city = query["city"]
    params.append(city)

    results = c.execute(search_string, params)
    result_table = results.fetchall()

    connection.commit()
    c.connection.close()

    # Gets average # reviews per restaurant
    for index, result in enumerate(result_table):
        avg_num_reviews = result[2] / result[1]
        avg_num_reviews = round(avg_num_reviews, 2)
        result_table[index] = [result[0], result[1], avg_num_reviews]

    return result_table


def price_ratings(query, database = "yelp_raw.db"):
    '''
    Gets avg ratings for each price category for a city
    Creates and saves two plots: graph of avg ratings by price category, pie chart
    showing number of restaurants in each price category

    Inputs:
        - query (dict): contains desired city name
            example query:
            query = {"city": "chicago"}
        - database

    Output:
        - list of lists: [price, avg rating, # restaurants, avg # reviews / restaurant]
        - price_ratings_city.png
        - price_restaurants_city.png
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()
    
    search_string = '''SELECT price, AVG(rating) as avg_rating, 
    COUNT(*) as num_restaurants, SUM(reviews) as num_reviews
    FROM restaurant
    WHERE city = ?
    COLLATE NOCASE
    AND reviews > 10
    GROUP BY price
    '''
    
    params = []
    city = query["city"]
    params.append(city)

    results = c.execute(search_string, params)
    result_table = results.fetchall()

    format_price_table = []

    for entry in result_table:
        if entry[0]:
            # Turns price from float to $
            price = math.ceil(float(entry[0])) * "$"
            format_price_table.append([price, entry[1], entry[2], entry[3] / entry[2]])

    connection.commit()
    c.connection.close()

    return format_price_table


def all_cuisines(query, database = "yelp_adjusted.db"):
    '''
    Get all cuisine types with >= 10 restaurants for a city from database

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
    
    search_string = '''SELECT DISTINCT cuisine, COUNT(*) as num_restaurants
    FROM cuisines
    JOIN restaurant
    ON restaurant.id = cuisines.id
    WHERE city = ?
    COLLATE NOCASE
    GROUP BY cuisine
    '''
    
    params = []
    city = query["city"]
    params.append(city)

    results = c.execute(search_string, params)
    result_table = results.fetchall()
    cuisine_table = []

    # Take out of form [("cuisine",)] to form ['cuisine']
    for result in result_table:
        print(result)
        if result[1] >= 10:
            cuisine_table.append(result[0])

    connection.commit()
    c.connection.close()

    return sorted(cuisine_table)


def cuisine_stats(cuisine, database = "yelp_adjusted.db"):
    '''
    Returns mean and standard deviation from a cuisine
    '''
    connection = sqlite3.connect(database)
    c = connection.cursor()
    
    search_string = '''SELECT AVG(rating) as avg_rating
    FROM cuisines
    JOIN restaurant
    ON restaurant.id = cuisines.id
    WHERE cuisine = ?
    GROUP BY city
    '''
    params = []
    params.append(cuisine)

    results = c.execute(search_string, params)
    result_table = results.fetchall()
    ratings_table = []

    # Take out of form [(rating,)] to form ['rating']
    for result in result_table:
        ratings_table.append(result[0])

    connection.commit()
    c.connection.close()

    sd = stat.stdev(ratings_table)
    mean = stat.mean(ratings_table)

    return sd, mean


def common_cuisines(query, database = "yelp_adjusted.db"):
    '''
    Returns most common cuisines with ratings

    Inputs:
        - query (dict): maps city name to all available cuisines
            example query:
            query = {"city": "Los Angeles"}

    Output:
        - list of lists of sorted most common cuisines
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()
    
    search_string = '''SELECT cuisine, AVG(rating) as avg_rating, 
    COUNT(*) as num_restaurants 
    FROM restaurant
    JOIN cuisines
    ON restaurant.id = cuisines.id
    WHERE city = ?
    COLLATE NOCASE
    GROUP BY cuisine
    '''
    
    params = []
    city = query["city"].lower()
    params.append(city)

    results = c.execute(search_string, params)
    result_table = results.fetchall()

    connection.commit()
    c.connection.close()
    
    full_result_list = []
    result_list = []

    for result in result_table:
        result = list(result)
        result[1] = round(result[1], 2)
        full_result_list.append(result)
        result_list.append(result[1:])
    full_result_list.sort(key = lambda x: x[2], reverse = True)
    result_list.sort(key = lambda x: x[1], reverse = True)

    return full_result_list[:5], result_list[:10]