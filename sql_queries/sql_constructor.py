# 02/05/2017
# Construct SQL Database from fake data
# Austin Herrick

import sqlite3
import itertools
import copy 

def create_table(database):
    '''
    Given a target database name, creates a database and a table to store
    data.
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()

    # Delete existing table
    c.execute("""DROP TABLE IF EXISTS restaurant;""")

    create_restaurant_table = """
        CREATE TABLE restaurant ( 
        id INTEGER PRIMARY KEY, 
        city VARCHAR(20),
        site VARCHAR(20), 
        stars INTEGER, 
        price INTEGER, 
        reviews INTEGER,
        cuisine_id INTEGER);"""

    c.execute(create_restaurant_table)

    c.connection.close()

def add_data(database, data_table):
    '''
    Given a data_table and a target database, translates data and inputs
    into SQL table.
    '''

    cuisines = find_all_cuisines(data_table)
    id_table = map_cuisines(cuisines[0], cuisines[1])
    sql_data = translate_tags(data_table, id_table)

    connection = sqlite3.connect(database)
    c = connection.cursor()

    # http://stackoverflow.com/questions/5905721/python-to-sql-list-of-lists
    add_data = '''INSERT INTO restaurant VALUES (?, ?, ?, ?, ?, ?, ?)'''

    c.executemany(add_data, sql_data)
    connection.commit()
    c.connection.close()



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
        entry[6] = lookup_cuisine_id(id_table, entry[6])

    return sql_data

def find_all_cuisines(data):
    '''
    Given a data table, finds all valid cuisine tags and the largest number
    appearing for a single restaurant.
    '''
    cuisine_list = []
    max_tag_length = 0

    for entry in data:
        for tag in entry[6]:
            if tag not in cuisine_list:
                cuisine_list.append(tag)
        if len(entry[6]) > max_tag_length:
            max_tag_length = len(entry[6])

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