import sqlite3
import csv
import string
import math

def get_top_cities(query, database = "yelp_adjusted.db"):
    '''
    Returns top cities for a cuisine, normalized by avg city ratings so that
    reviews across cities are comparable
    Inputs:
        - query (dict): maps city name to all available cuisines
            example query:
            query = {"cuisine": "Mexico"}
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
        return result_table[:query["limit"]]
    else:
        return result_table
        
    
def get_top_cuisines(query, database = "yelp_adjusted.db"):
    '''
    Get top cuisines for a city (or worst if "worse" is specified), 
    restricts to restaurants with >= 5 reviews and cuisines with >= 5 restaurants
    
    Required: city name
    Optional: price ceiling, limit of # cuisines returned

    Inputs:
        - query (dict): maps possible queries (city, price) to list of user inputs
          example_query = {"city": "chicago",
                           "price": "$$$",
                           "limit": 10,
                           "worst": True}
        - database name
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
    city = query["city"]
    params.append(city)

    # If user specified price ceiling, adjusts table to return cuisines
    # below this average price
    if "price" in query:
        search_string += '''AND price <= ?'''
        price_length = len(query["price"])
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

def price_ratings(query, database = "yelp_adjusted.db"):
    '''
    Gets avg ratings for each star category for a city, normalized

    Inputs:
        - query (dict): contains desired city name
            example query:
            query = {"city": "chicago"}
        - database

    Output:
        - dictionary mapping dollar signs to avg ratings
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()
    
    search_string = '''SELECT price, AVG(rating) as avg_rating 
    FROM restaurant
    WHERE city = ?
    AND reviews > 10
    GROUP BY price
    COLLATE NOCASE
    '''
    
    params = []
    city = query["city"]
    params.append(city)

    results = c.execute(search_string, params)
    result_table = results.fetchall()

    format_price_table = {}

    for entry in result_table:
        entry = list(entry)
        if entry[0]:
            # Turns price from float to $
            entry[0] = math.ceil(float(entry[0])) * "$"

            # Normalizes ratings across cities
            entry[1] = entry[1] * city_ratings["avg"] / city_ratings[city]
            format_price_table[entry[0]] = entry[1]

    connection.commit()
    c.connection.close()

    return format_price_table

def all_cuisines(query, database = "yelp_adjusted.db"):
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
    COLLATE NOCASE
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