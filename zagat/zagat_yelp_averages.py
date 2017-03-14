# SQL Database Constructor

'''
This program takes a csv containing Zagat data from all restaurants in Chicago and
surrounding areas, and matches with Yelp data to find difference in average ratings across
the two review sites.

Usage: Call "go" with default parameters or preferred alternatives
'''

import sqlite3
import csv
import re
import time
import pandas as pd
import jellyfish
import string

zagat_translate_address = {"West": "W", "North": "N", "South": "S", "East": "E", "Road": "Rd", "Street": "St",
    "Boulevard": "Blvd", "Place": "Pl", "Avenue": "Ave", "Lane": "Ln", "Center": "Ctr"}

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
    unique_matches = merge_data()
    yelp_matches_list = unique_matches["Yelp Rating"].tolist()
    zagat_matches_list = unique_matches["Zagat Rating"].tolist()
    
    # Get average Chicago rating from Zagat
    match_sum = 0
    for match_rating in zagat_matches_list:
        if match_rating:
            match_sum += match_rating
    avg = match_sum/len(zagat_matches_list)
    print("Zagat: ", avg)

    # Get average Chicago rating from Yelp
    match_sum = 0
    for match_rating in yelp_matches_list:
        if match_rating:
            match_sum += match_rating
    avg = match_sum/len(yelp_matches_list)
    print("Yelp: ", avg)

    print(time.clock() - start_time, "seconds")


def zagat_csv(source_file):
    '''
    Creates data table from zagat data in csv. 

    Inputs:
        - source_file: The csv containing zagat data

    Returns:
        - zagat_data: A list of lists containing the data
    '''

    duplicate = 0
    searched = set()
    zagat_data = []
    data_csv = csv.reader(open(source_file, newline='', encoding = 'ISO-8859-1'), delimiter=',')
    
    for row in data_csv:
        # Checks for duplicates
        if tuple(row[:7]) not in searched: # Excludes lat and lon for accuracy errors
            zagat_data.append(row)
            searched.add(tuple(row[:7]))
        else:
            duplicate += 1

    print("duplicates removed: ", duplicate)
    
    return zagat_data


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
        rating FLOAT,
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
    ID = 1
    for entry in zagat_data:
        restaurant_entry = [ID] # Unique ID
        restaurant_entry.append(entry[0]) # Name
        restaurant_entry.append(entry[6]) # Rating
        restaurant_entry.append(entry[2]) # Address
        restaurant_entry.append(entry[3]) # City
        restaurant_entry.append(entry[4]) # Zip Code
        restaurant_entry.append(entry[7]) # Latitude
        restaurant_entry.append(entry[8]) # Longitude

        restaurant_sql.append(restaurant_entry)
        ID += 1

    c.executemany(add_restaurant_data, restaurant_sql)
    
    connection.commit()
    c.connection.close()


def merge_data(database1 = "zagat_raw.db", database2 = "yelp_raw.db", output_database = "linked_data.db"):
    '''
    Get matches between Zagat and Yelp databases, returns pandas dataframe of matched data
    '''

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
        rating FLOAT,
        price VARCHAR(5), 
        reviews INTEGER,
        phone VARCHAR(15),
        neighborhood VARCHAR(20),
        address VARCHAR(50),
        zipcode INTEGER,
        lat FLOAT(25),
        lon FLOAT(25)
        );""")
    c.execute("INSERT INTO main.restaurant SELECT * FROM yelp.restaurant")   

    # Gets IDs, name, ratings, and addresses from Zagat and Yelp data tables
    # if they match mame, zipcode, and lat/lon to 1 decimal place
    search_string = '''SELECT zag_restaurant.id, restaurant.id, zag_restaurant.name, zag_restaurant.rating, restaurant.rating, 
    zag_restaurant.address, restaurant.address
    FROM zag_restaurant
    JOIN restaurant
    ON zag_restaurant.name = restaurant.name
    COLLATE NOCASE
    AND zag_restaurant.zipcode = restaurant.zipcode
    AND ROUND(zag_restaurant.lat, 1) = ROUND(restaurant.lat, 1)
    AND ROUND(zag_restaurant.lon, 1) = ROUND(zag_restaurant.lon, 1);'''

    results = c.execute(search_string)
    result_table = results.fetchall()
    result_frame = pd.DataFrame(result_table, columns=["Zagat_ID", "Yelp_ID", "Zagat Name", 
        "Zagat Rating", "Yelp Rating", "Zagat Address", "Yelp Address"])

    connection.commit()
    c.connection.close()
    
    zagat_address_series = result_frame["Zagat Address"]
    new_address_series = []

    # Change Zagat addresses to Yelp formatting
    for address in zagat_address_series:
        for place_word in zagat_translate_address.keys():
            address = address.replace(place_word, zagat_translate_address[place_word])
        new_address_series.append(address)
    new_address_series = pd.Series(new_address_series, name = "Zagat Address")
    result_frame["Zagat Address"] = new_address_series

    zagat_unique = unique_matches("Zagat_ID", result_frame)
    yelp_unique = unique_matches("Yelp_ID", zagat_unique)
    
    return yelp_unique

def unique_matches(ID, df):
    '''
    Removes duplicate matches, finds best match

    Inputs:
        - ID: column name for source ID that is being checked for duplicates
        - df: dataframe for which duplicates are being removed and best matches found

    Outputs:
        - unique_matches: dataframe of matched data
    '''
    # Dataframe with entries that had duplicate IDs
    unique_matches = df.drop_duplicates(subset = ID)

    if ID == "Zagat_ID":
        dup = unique_matches[unique_matches[unique_matches.columns[0]].duplicated()]
    else:
        dup = unique_matches[unique_matches[unique_matches.columns[1]].duplicated()]
    dup_ids = dup[ID].unique().tolist()

    # Chooses best match for each set of multiple matches
    for dup_id in dup_ids:
        dup_frame = dup.loc[dup[ID] == dup_id]
        score = 0
        match = False
        
        # Get best match using jaro_winkler distance
        for index, row in dup_frame.iterrows():
            row_score = jellyfish.jaro_winkler(row["Zagat Address"], row["Yelp Address"])
            if row_score > score and row_score > .5: # Chosen to max correct matches, min false matches
                score = row_score
                best_row = row
                match = True

        if match:
            unique_matches = unique_matches.append(best_row)

    return unique_matches