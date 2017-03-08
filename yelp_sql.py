import sqlite3
import csv
import string
import math
import matplotlib.pyplot as plt
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
        return result_table[:query["limit"]]
    else:
        return result_table[:10]
        
    
def get_top_cuisines(query, database = "yelp_adjusted.db"):
    '''
    Get top cuisines for a city (or worst if "worse" is specified), 
    restricts to restaurants with >= 5 reviews and cuisines with >= 5 restaurants
    
    Required: city name
    Optional: price ceiling, limit of # cuisines returned (default 10), worst (boolean specifying
        best or worst cuisines)

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
    city = query["city"]
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

    if "worst" in query and query["worst"]:
        result_table.sort(key = lambda x: x[2])
    else:
        result_table.sort(key = lambda x: x[2], reverse = True)

    # Formats prices and ensures cuisines have > 5 restaurants
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
            entry[1] = math.ceil(entry[1]) * "$"

            # Restricts to cuisines with > 5 restaurants
            if entry[3] > 5:
                special = special_cuisine(entry[0], entry[2])
                entry.append(special)
                format_price_table.append(entry)
                count += 1

    connection.commit()
    c.connection.close()

    return (["Cuisine", "Price", "Rating", "# Restaurants", "Total Reviews", "Relative Rating"], 
        format_price_table)


def price_ratings(query, database = "yelp_adjusted.db"):
    '''
    Gets normalized avg ratings for each price category for a city
    Creates and saves two plots: graph of avg ratings by price category, pie chart
    showing number of restaurants in each price category

    Inputs:
        - query (dict): contains desired city name
            example query:
            query = {"city": "chicago"}
        - database

    Output:
        - dictionary mapping dollar signs to list [avg rating, # restaurants]
        - price_ratings_city.png
        - price_restaurants_city.png
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()
    
    search_string = '''SELECT price, AVG(rating) as avg_rating, 
    COUNT(*) as num_restaurants 
    FROM restaurant
    WHERE city = ?
    COLLATE nocase
    AND reviews > 10
    GROUP BY price
    '''
    
    params = []
    city = query["city"]
    params.append(city)

    results = c.execute(search_string, params)
    result_table = results.fetchall()

    format_price_table = {}

    for entry in result_table:
        if entry[0]:
            # Turns price from float to $
            price = math.ceil(float(entry[0])) * "$"
            format_price_table[price] = [entry[1], entry[2]]

    connection.commit()
    c.connection.close()

    prices = []
    ratings = []
    num_restaurants = []
    total = 0
    price_keys = sorted(format_price_table.keys())
    
    for price in price_keys:
        prices.append(price)
        ratings.append(format_price_table[price][0])
        num_restaurants.append(format_price_table[price][1])
        total += format_price_table[price][1]

    # Visualizes price to ratings graph
    plt.xlabel('Price')
    plt.ylabel('Avg Rating')
    plt.title('Price to Ratings in ' + query["city"].capitalize())

    max_price = len(format_price_table.keys())
    x_ticks = []

    # Creates $ labels (if not escaped with \, creates error)
    for i in range(max_price):
        x_ticks.append((i + 1) * "\$")

    x = [i + 1 for i in range(max_price)]

    plt.xticks(x, x_ticks)
    plt.plot(x, ratings, 'ro')
    plt.axis([0, 5, min(ratings) - .1, max(ratings) + .1])

    # Saves price to ratings graph for "city" as "price_ratings_city.png"
    plt.savefig('price_ratings_' + query["city"].replace(' ', '').lower() + '.png')
    plt.close('all')

    # Visualizes number of restaurants per price bracket as a pie graph
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    plt.pie(num_restaurants, labels=x_ticks, colors=colors, 
        autopct=lambda p: '{:.0f}'.format(p * total / 100), startangle=0)
    plt.axis('equal')

    # Saves price to num_restaurants for "city" as "price_restaurants_city.png"
    plt.savefig('price_restaurants_' + query["city"].replace(' ', '').lower() + '.png')
    plt.close('all')

    return format_price_table

def all_cuisines(query, database = "yelp_adjusted.db"):
    '''
    Get all cuisine types with >= 5 restaurants for a city from database

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
        if result[1] > 4:
            cuisine_table.append(result[0])

    connection.commit()
    c.connection.close()

    return sorted(cuisine_table)

def special_cuisine(cuisine, rating, database = "yelp_adjusted.db"):
    '''
    Returns a value measuring whether a cuisine is unusually highly/lowly
    rated based on data from other cities
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
    if math.fabs(rating - mean) <= sd:
        color = "average"
    elif rating - mean > 0:
        color = "good"
    else:
        color = "below"

    return color