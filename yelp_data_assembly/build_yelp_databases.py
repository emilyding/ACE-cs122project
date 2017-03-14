# SQL Database Constructor

'''
This program takes a csv containing Yelp data from all restaurants in all cities,
and constructs a SQL database storing the information. A csv file is also written
containing average ratings of restaurants in each city, so that rating information
can be standardized. These standardized ratings are stored in a second SQL database.

Note that the second database will result in a small number of restaurants with
ratings below 1.0 or above 5.0.

Usage: Call "go" with default parameters or preferred alternatives
'''

import sqlite3
import csv
import re
import time
from statistics import mean


def go(output_file = "city_ratings.csv", database1 = "yelp_raw.db", 
    database2 = "yelp_adjusted.db", source_file = "all_restaurants.csv"):
    '''
    Creates two SQL databases, with raw and adjusted review data, as well as a
    csv containing the average rating in each city.

    Inputs: 
        - output_file: The name of the csv to save average reviews per city to
        - database1: The name of the SQL database for unadjusted data
        - database2: The name of the SQL database for adjusted data (normalized across cities)
        - source_file: The name of the csv where yelp data is located
    '''

    # Time is tracked for efficiency testing
    start_time = time.clock()

    # Collect data, build initial database
    yelp_data = yelp_csv(source_file)
    build_database(database1, yelp_data)

    # Constructs csv of city ratings
    result_table = get_city_ratings(output_file, database1)

    # Finds the adjustment factor for each city to standardize across cities
    # Note: multiplying by factor as opposed to linear adjustment allows accounting
    # for possible differences in use of the range of reviews
    avg_review = mean(city_avg for city_name, city_avg in result_table)
    adjustment_rates = {}
    for city in result_table:
        adjustment_rates[city[0]] = avg_review / city[1]

    # Adjusts the rating of each restaurant in the data
    # (Yelp reports rating as a string, so it must first be converted to a float)
    for item in yelp_data:
        item[5] = float(item[5]) * adjustment_rates[item[2]]

    # Builds the second database, with adjusted restaurant review numbers
    build_database(database2, yelp_data)

    # This code exists for testing: See that all averages are essentially identical
    # get_city_ratings("city_ratings_adjusted.csv", database2)

    print(time.clock() - start_time, "seconds")

def yelp_csv(source_file):
    '''
    Creates data table from yelp data in csv. 

    Inputs:
        - source_file: The csv containing yelp data

    Returns:
        - yelp_data: A list of lists containing the data
    '''

    yelp_data = []
    data_csv = csv.reader(open(source_file, newline='', encoding = 'ISO-8859-1'), delimiter=',')
    for row in data_csv:
        yelp_data.append(row)
    
    # Skips the first row, which stores heading information
    yelp_data = yelp_data[1:]

    return yelp_data

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


def find_cuisines(filepath="cuisines_tags.csv"):
    '''
    Reads a csv copied from Yelp's category_list for v3, found here:
    https://www.yelp.com/developers/documentation/v3/category_list
    and converts to a usable list of string tags. Note that restaurants may
    include cuisine tags that don't appear on this list, in the case of "hybrid"
    restaurants (for example, several Asian restaurants are also grocery stores).
    These tags aren't excluded.

    Inputs:
        - filepath: Filepath for the location of the csv

    Returns:
        - cuisine_tags: A list of strings
    '''

    # Open csv
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        cuisine_list = list(reader)

    # Translate to usable form
    cuisine_tags = []
    for item in cuisine_list:
        search = re.search(r'^.*(?=\s\()', item[0]).group()

        # Delete spaces, convert to lowercase
        search = search.lower()
        search = search.replace(' ', '')
        cuisine_tags.append(search)


    return cuisine_tags


def build_database(database, yelp_data):
    '''
    Given a target database name and a data source, creates a SQL database using
    two tables for restaurant and cuisine information, and loads relevant data into
    it.

    Inputs:
        - database: The name of the SQL database to be created
        - source_file: The name of the csv where yelp data is located
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()

    # Delete existing tables, if applicable
    c.execute("""DROP TABLE IF EXISTS restaurant;""")
    c.execute("""DROP TABLE IF EXISTS cuisines;""")

    create_restaurant_table = """
        CREATE TABLE restaurant ( 
        id INTEGER, 
        city VARCHAR(20),
        name VARCHAR(30),
        rating INTEGER,
        price VARCHAR(5), 
        reviews INTEGER,
        phone VARCHAR(15),
        neighborhood VARCHAR(20),
        address VARCHAR(40),
        zipcode INTEGER,
        lat FLOAT(25),
        lon FLOAT(25)
        );"""
    
    create_cuisine_table = """
        CREATE TABLE cuisines (
        id INTEGER,
        cuisine VARCHAR(20)
        );"""

    c.execute(create_restaurant_table)
    c.execute(create_cuisine_table)

    cuisine_tags = find_cuisines()

    # Construct strings for inserting data
    add_restaurant_data = '''INSERT INTO restaurant VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    add_cuisine_data = '''INSERT INTO cuisines VALUES (?, ?)'''

    restaurant_sql = []
    cuisine_sql = []

    # Collect relevant information, and clean up cuisine information
    for entry in yelp_data:
        restaurant_entry = entry[1 : 4] # Unique ID, City, Name
        restaurant_entry.append(entry[5]) # Rating
        price = entry[6]
        if price == "N/A":
            restaurant_entry.append("")
        else:
            restaurant_entry.append(len(price))
        restaurant_entry.append(entry[7]) # Review Count
        restaurant_entry.append(entry[11]) # Phone
        restaurant_entry.append(entry[8]) # Neighborhood
        restaurant_entry.append(entry[9]) # Address
        restaurant_entry.append(entry[10]) # Zipcode
        restaurant_entry.append(entry[13]) # Latitude
        restaurant_entry.append(entry[12]) # Longitude

        restaurant_sql.append(restaurant_entry)
        
        # Make cuisines table entry
        # This is necessary because each restaurant has a varying number of
        # cuisine tags
        list_chars = re.compile('[[" \]]')
        result = list_chars.sub('', entry[4]).split(',')

        for cuisine_type in result:
            cuisine_type.strip(" \'")
            cuisine_type = cuisine_type[1:-1]
            # Excludes tags that are not food tags
            if cuisine_type.lower() in cuisine_tags:
                cuisine_sql.append([entry[1], cuisine_type])

    c.executemany(add_restaurant_data, restaurant_sql)
    c.executemany(add_cuisine_data, cuisine_sql)
    
    connection.commit()
    c.connection.close()