# SQL Database Constructor

'''
This program takes a csv containing Zagat data from all restaurants in Chicago and
surrounding areas, and constructs a SQL database storing the information. 

Usage: Call "go" with default parameters or preferred alternatives
'''

import sqlite3
import csv
import re
import time
from statistics import mean


def go(database = "zagat_raw.db", 
    source_file = "zagat_Chicago.csv"):
    '''
    Creates SQL database with raw review data, as well as a
    csv containing the average rating in each city.

    Inputs: 
        - database: The name of the SQL database for zagat data
        - source_file: The name of the csv where zagat data is located
    '''

    # Time is tracked for efficiency testing
    start_time = time.clock()

    # Collect data, build initial database
    zagat_data = zagat_csv(source_file)
    build_database(database, zagat_data)

    print(time.clock() - start_time, "seconds")

def zagat_csv(source_file):
    '''
    Creates data table from zagat data in csv. 

    Inputs:
        - source_file: The csv containing zagat data

    Returns:
        - zagat_data: A list of lists containing the data
    '''

    zagat_data = set()
    data_csv = csv.reader(open(source_file, newline='', encoding = 'ISO-8859-1'), delimiter=',')
    id_num = 1
    for row in data_csv:
        row = [id_num] + row
        zagat_data.add(tuple(row))
        id_num += 1
    
    # Skips the first row, which stores heading information
#    zagat_data = zagat_data[1:]

    return list(zagat_data)

def get_city_ratings(output_file, database):
    '''
    Get average city ratings from raw SQL database and save to csv. This information
    will be used to normalize restaurant reviews for the second database.

    Inputs:
        - output_file: The file to save average reviews to
        - database: The raw SQL database results are pulled from

    Returns:
        - result_table: A list of tuples of city and average review
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()
    
    # Restaurants with extremely few reviews can dramatically swing results,
    # both for average ratings for a cuisine, or average ratings in a city
    # (Most 5.0 and 1.0 restaurants, for example, have only 1 review)
    # Therefore, restaurants with fewer than 5 reviews are not used for
    # normalization
    search_string = '''SELECT city, AVG(rating) 
    FROM restaurant WHERE reviews > 4
    GROUP BY city
    '''

    results = c.execute(search_string)
    result_table = results.fetchall()

    connection.commit()
    c.connection.close()

    # Writes into the csv with name specified (default city_ratings.csv)
    with open(output_file, 'wt') as out:
        csv_out = csv.writer(out, lineterminator = '\n')
        csv_out.writerow(['City', 'Average Rating'])
        for row in result_table:
            csv_out.writerow(row)

    return result_table

def build_database(database, zagat_data):
    '''
    Given a target database name and a data source, creates a SQL database using
    two tables for restaurant and cuisine information, and loads relevant data into
    it.

    Inputs:
        - database: The name of the SQL database to be created
        - source_file: The name of the csv where zagat data is located
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()

    # Delete existing tables, if applicable
    c.execute("""DROP TABLE IF EXISTS zag_restaurant;""")

    create_restaurant_table = """
        CREATE TABLE zag_restaurant ( 
        id INTEGER, 
        name VARCHAR(30),
        rating INTEGER,
        address VARCHAR(30),
        city VARCHAR(20),
        zipcode INTEGER,
        lat FLOAT(25),
        lon FLOAT(25)
        );"""

    c.execute(create_restaurant_table)

    # Construct strings for inserting data
    add_restaurant_data = '''INSERT INTO zag_restaurant VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

    restaurant_sql = []

    # Collect relevant information, and clean up cuisine information
    for entry in zagat_data:
        restaurant_entry = [entry[0]] # Unique ID
        restaurant_entry.append(entry[1]) # Name
        restaurant_entry.append(entry[7]) # Rating
        restaurant_entry.append(entry[3]) # Address
        restaurant_entry.append(entry[4]) # City
        restaurant_entry.append(entry[5]) # Zip Code
        restaurant_entry.append(entry[8]) # Latitude
        restaurant_entry.append(entry[9]) # Longitude

        restaurant_sql.append(restaurant_entry)

    c.executemany(add_restaurant_data, restaurant_sql)
    
    connection.commit()
    c.connection.close()

def merge_data(database1 = "zagat_raw.db", database2 = "yelp_raw.db", output_database = "linked_data.db"):
    connection = sqlite3.connect(database1)
    c = connection.cursor()

    c.execute("DROP TABLE IF EXISTS restaurant;")
    c.execute("ATTACH DATABASE 'yelp_raw.db' AS yelp")

    c.execute("SELECT sql FROM yelp.sqlite_master WHERE type='table' AND name='restaurant'")
    c.execute("""
        CREATE TABLE restaurant ( 
        id INTEGER, 
        city VARCHAR(20),
        name VARCHAR(30),
        rating INTEGER,
        price VARCHAR(5), 
        reviews INTEGER,
        phone VARCHAR(15),
        neighborhood VARCHAR(20),
        lat FLOAT(25),
        lon FLOAT(25)
        );""")
    c.execute("INSERT INTO main.restaurant SELECT * FROM yelp.restaurant")   

    search_1 = '''SELECT name, rating
    FROM zag_restaurant
    LIMIT 10;'''
    search_2 = '''SELECT name, rating
    FROM restaurant
    LIMIT 10;'''
    search_string = '''SELECT zag_restaurant.name, zag_restaurant.rating
    FROM zag_restaurant
    INNER JOIN restaurant
    ON zag_restaurant.name LIKE restaurant.name;'''

    #WHERE ABS(zag_restaurant.lat - restaurant.lat) < 1
    #AND ABS(zag_restaurant.lon - restaurant.lon) < 1

    results = c.execute(search_1)
    result_table = results.fetchall()
    print(result_table)

    results = c.execute(search_2)
    result_table = results.fetchall()
    print(result_table)

    results = c.execute(search_string)
    result_table = results.fetchall()
    print()
    print()
    print(result_table)

    connection.commit()
    c.connection.close()

    return

    result_table.sort(key = lambda x: x[1], reverse = True)

    if "limit" in query:
        limit = query["limit"]

    else:
        limit = 10
    
    result_table = result_table[:10]

    result_frame = pd.DataFrame(result_table, columns=["City", "Rating", "# Restaurants"])
    result_frame = result_frame.round(2)
    result_frame["City"] = result_frame["City"].str.title() # Capitalize city names

    length = len(result_frame.index)
    result_frame.index = [i + 1 for i in range(length)]

    return result_frame.values.tolist()