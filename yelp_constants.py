import sqlite3
import csv
import re
import time

# Need to make_two_tables(database) first to create database

def yelp_csv():
    '''
    Creates data table from yelp data in csv
    '''
    yelp_data = []
    data_csv = csv.reader(open('all_restaurants.csv', newline='', encoding = 'ISO-8859-1'), delimiter=',')
    
    for row in data_csv:
        yelp_data.append(row)
    
    # headers = yelp_data[0]
    yelp_data = yelp_data[1:]

    return yelp_data

    # 0 Headers 
    # 1 Unique ID (*)
    # 2 City (*)
    # 3 Name (*)
    # 4 Cuisine (*)
    # 5 Rating (*)
    # 6 Price (*)
    # 7 Review Count (*)
    # 8 Neighborhood
    # 9 Address (*)
    # 10 Zip Code (*)
    # 11 Phone (*)
    # 12 Latitude
    # 13 Longitude


def make_two_tables(database):
    '''
    Given a target database name, creates a database and a table to store
    data.
    '''

    data_table = yelp_csv()

    connection = sqlite3.connect(database)
    c = connection.cursor()

    # Delete existing table
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
        phone VARCHAR(15)
        );"""
    
    create_cuisine_table = """
        CREATE TABLE cuisines (
        id INTEGER,
        cuisine VARCHAR(20)
        );"""

    c.execute(create_restaurant_table)
    c.execute(create_cuisine_table)

    add_restaurant_data = '''INSERT INTO restaurant VALUES (?, ?, ?, ?, ?, ?, ?)'''
    add_cuisine_data = '''INSERT INTO cuisines VALUES (?, ?)'''

    restaurant_sql = []
    cuisine_sql = []

    for entry in data_table:
        # Make restaurant table entry
        restaurant_entry = entry[1 : 4] # Unique ID, City, Name
        restaurant_entry.append(entry[5]) # Rating
        price = entry[6]
        if price == "N/A":
            restaurant_entry.append("")
        else:
            restaurant_entry.append(len(price)) # Price
        restaurant_entry.append(entry[7]) #Review Count
        restaurant_entry.append(entry[11]) # Phone

        restaurant_sql.append(restaurant_entry)
        
        # Make cuisines table entry
        list_chars = re.compile('[[" \]]')
        result = list_chars.sub('', entry[4]).split(',')

        for cuisine_type in result:
            cuisine_type.strip(" \'")
            cuisine_sql.append([entry[1], cuisine_type[1:-1]])

    c.executemany(add_restaurant_data, restaurant_sql)
    c.executemany(add_cuisine_data, cuisine_sql)
    
    connection.commit()
    c.connection.close()


def get_city_ratings(output_file = "city_ratings.csv", database = "yelp_test.db"):
    '''
    Get average city ratings from database for normalization, save to csv
    '''
    start_time = time.clock()
    make_two_tables(database)

    connection = sqlite3.connect(database)
    c = connection.cursor()
    
    search_string = '''SELECT city, AVG(rating)
    FROM restaurant
    GROUP BY city
    '''

    results = c.execute(search_string)
    result_table = results.fetchall()

    connection.commit()
    c.connection.close()

    # Writes into the csv with name specified (default city_ratings.csv)
    with open(output_file, 'wt') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['City', 'Average Rating'])
        for row in result_table:
            csv_out.writerow(row)

    print(time.clock()-start_time, "seconds")