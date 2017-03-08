# 02/09/2017
# Construct SQL Database from fake data
# Camille

import sqlite3
import itertools
import copy 


def make_two_tables(database, data_table):
    '''
    Given a target database name, creates a database and a table to store
    data.
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()

    # Delete existing table
    c.execute("""DROP TABLE IF EXISTS restaurant;""")
    c.execute("""DROP TABLE IF EXISTS cuisines;""")


    create_restaurant_table = """
        CREATE TABLE restaurant ( 
        id INTEGER PRIMARY KEY, 
        city VARCHAR(20),
        site VARCHAR(20), 
        price INTEGER, 
        reviews INTEGER,
        stars INTEGER
        );"""
    
    create_cuisine_table = """
        CREATE TABLE cuisines (
        id INTEGER,
        cuisine VARCHAR(20)
        );"""

    c.execute(create_restaurant_table)
    c.execute(create_cuisine_table)

    add_restaurant_data = '''INSERT INTO restaurant VALUES (?, ?, ?, ?, ?, ?)'''
    add_cuisine_data = '''INSERT INTO cuisines VALUES (?, ?)'''

    restaurant_sql = []
    cuisine_sql = []

    for entry in data_table:
        # Append restaurant entry except cuisine to restaurant_sql
        restaurant_entry = entry[:5]
        restaurant_entry.append(entry[6])
        restaurant_sql.append(restaurant_entry)
        
        for cuisine_type in entry[5]:
            cuisine_sql.append([entry[0], cuisine_type])

    c.executemany(add_restaurant_data, restaurant_sql)
    c.executemany(add_cuisine_data, cuisine_sql)
    
    connection.commit()
    c.connection.close()

    
def get_ratings(query, database):
    '''
    Get user-requested data from database

    Inputs:
        - query (dict): maps possible queries (city, price) to list of user inputs
        - database
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()

    header = ["ID", "City", "Source", "Price", "# Reviews", "Cuisine Tags", "Stars"]
    
    search_string = '''SELECT city, cuisine, price, AVG(stars) as rating, 
    COUNT(*) as num_restaurants
    FROM restaurant
    JOIN cuisines
    ON restaurant.id = cuisines.id
    WHERE city = ?
    GROUP BY cuisine
    ORDER BY rating DESC
    '''
    params = []
    city = query["city"]
    params.append(city)

    if "limit" in query:
        search_string += '''LIMIT ?;'''
        params.append(query["limit"])
    else:
        search_string += ''';'''

    # Things to consider: how to do prices?
    
    results = c.execute(search_string, params)
    result_table = results.fetchall()

    connection.commit()
    c.connection.close()

    return (["City", "Cuisine", "Price", "Rating", "# Restaurants"], result_table)




def do_calculations(inputs):
    words
    return results


################ Helper Functions #######################

# Code suggestion: http://stackoverflow.com/questions/464864/how-to-get-all-possible-combinations-of-a-list-s-elements
def map_cuisines(cuisine_list, max_tag_length):
    '''
    Using a list of all appearing cuisines, and the longest number of tags on
    a single restaurant, returns a table mapping a unique id to all cuisine 
    combinations.
    '''

    id_table = []
    uniq_id = 100000

    # Number of combinations with n cuisines and up to m tags each:
    # summation from k = 1 to k = m of n!/[k!*(n-k)!]
    for i in range(max_tag_length + 1):
        for subset in itertools.combinations(cuisine_list, i):
            id_table.append([uniq_id, subset])
            uniq_id += 1

    return id_table

def translate_tags(data, id_table):
    '''
    Given a data table, translate cuisine tags into id codes.
    '''

    sql_data = copy.deepcopy(data)
    for entry in sql_data:
        entry[5] = lookup_cuisine_id(id_table, entry[5])

    return sql_data

def find_all_cuisines(data):
    '''
    Given a data table, finds all valid cuisine tags and the largest number
    appearing for a single restaurant.
    '''
    cuisine_list = []
    max_tag_length = 0

    for entry in data:
        for tag in entry[5]:
            if tag not in cuisine_list:
                cuisine_list.append(tag)
        if len(entry[5]) > max_tag_length:
            max_tag_length = len(entry[5])

    cuisine_list.sort()

    return (cuisine_list, max_tag_length)

def lookup_cuisine_id(id_table, desired_tags):
    '''
    Given an id_table and a list of desired cuisine tags, returns the
    corresponding id. Input should be a list or a tuple
    '''

    desired_tags = sorted(desired_tags)
    desired_tags = tuple(desired_tags)

    for entry in id_table:
        if entry[1] == desired_tags:
            return entry[0]

def lookup_cuisines(id_table, cuisine_id):
    '''
    Given a cuisine id, return the corresponding cuisine tags. Input should be
    an integer
    '''

    for entry in id_table:
        if entry[0] == cuisine_id:
            return entry[1]