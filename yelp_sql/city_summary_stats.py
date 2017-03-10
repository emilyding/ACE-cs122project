# Summary City Data

'''
Takes as an input a dictionary with the name of a city, and returns interesting
summary statistics. Note that using the adjusted database will lead to errors
identifying universally hated/acclaimed restaurants (as ratings of 1 or 5 will
be adjusted slightly upwards or downwards)

Usage: Call get_summary_info with the city of interest.
Example Call: get_summary_info({'city': 'Los Angeles'})
'''

import sqlite3
import csv
from statistics import mean

# Maps cities to median min meters between starbucks
# Dictionary readout produced by build_starbucks_dictionary.py
starbucks_mapper = {'albuquerque': '154.15', 'arlington': '83.33', 'atlanta': '352.59',
'austin': '123.41', 'baltimore': '86.41', 'boston': '98.32', 'buffalo': '162.93', 
'charlotte': '251.00', 'chicago': '138.73', 'cleveland': '149.90', 'colorado springs': '221.52',
'columbus': '385.16', 'dallas': '517.69', 'denver': '282.46', 'detroit': '486.73', 
'el paso': '241.77', 'fort worth': '239.43', 'fresno': '96.81', 'honolulu': '33.39',
'houston': '393.32', 'indianapolis': '406.86', 'jacksonville': '184.75', 'kansas city': '978.47',
'las vegas': '395.43', 'long beach': '112.44', 'los angeles': '187.45', 'louisville': '213.46',
'memphis': '219.27', 'mesa': '411.07', 'miami': '142.43', 'milwaukee': '146.95', 
'minneapolis': '317.86', 'nashville': '173.47', 'new orleans': '103.72', 'new york': '105.39',
'oakland': '97.87', 'oklahoma city': '213.86', 'omaha': '228.06', 'philadelphia': '106.38',
'phoenix': '531.17', 'pittsburgh': '272.22', 'portland': '193.92', 'raleigh': '564.58',
'sacramento': '84.44', 'san antonio': '363.24', 'san diego': '110.48', 'san francisco': '67.07',
'san jose': '89.94', 'seattle': '134.22', 'st louis': '635.64', 'st paul': '125.64',
'tampa': '324.66', 'tucson': '135.19', 'tulsa': '327.75', 'virginia beach': '140.52',
'washington dc': '106.63'}

def build_starbucks_dictionary(filepath = 'starbucks_index.csv'):
    '''
    Given a filepath, constructs a dictionary mapping each city to the
    median minimum distance to another Starbucks. Used in get_summary_info.

    Inputs:
        - filepath: The location of the Starbucks distance csv

    Returns:
        - Dictionary mapping cities to the median min starbucks distance
    '''
    starbucks_mapper = {}

    with open(filepath) as holding:
        reader = csv.reader(holding)
        for row in reader:
            # Skip headers
            if row[2] != "Median Distance":
                # Build dictionary, applying rounding
                starbucks_mapper.update({row[1]: "{0:.2f}".format(float(row[2]))})

    return starbucks_mapper

def get_summary_info(city = {}, database = "yelp_raw.db"):
    '''
    Takes in a city dictionary and database and returns summary statistics.

    Inputs:
        - city: City of interest. Format is {'city': 'Chicago'}
        - database = Location of unadjusted database

    Returns:
        - A list of tuples displaying summary information
    '''

    # Change city input to lowercase, if necessary
    if city != {}:
        city["city"] = city["city"].lower()
        starbucks_index = starbucks_mapper[city["city"]]
    # If city s not supplied, find average distance across all keys
    else:
        float_distances = []
        for distance in starbucks_mapper.values():
            float_distances.append(float(distance))
        starbucks_index = "{0:.2f}".format(mean(float_distances))


    # Find necessary information
    total_restaurants = find_total_restaurants(city, database)
    most_reviewed = find_most_reviewed_restaurant(city, database)
    most_acclaimed = find_consensus_restaurant(city, database, rating = 5)
    most_hated = find_consensus_restaurant(city, database, rating = 1)
    
    # Construct Result List
    result_list = []
    if city != {}:
        result_list.append(("Total Restaurants in City:", total_restaurants))
    else:
        result_list.append(("Total Restaurants in Sample:", total_restaurants))
    result_list.append(("Starbucks Distance Index:", 
        "{} Meters".format(starbucks_index)))
    result_list.append(("Most Reviewed Restaurant:", 
        "{}, {} Reviews".format(most_reviewed[0], most_reviewed[1])))
    result_list.append(("Most Reviewed 5-Star Restaurant:", 
        "{}, {} Reviews".format(most_acclaimed[0], most_acclaimed[1])))
    result_list.append(("Most Reviewed 1-Star Restaurant:", 
        "{}, {} Reviews".format(most_hated[0], most_hated[1])))

    return result_list

def find_total_restaurants(city, database):
    '''
    Finds total number of restauarants in a city.

    Inputs:
        - city: City of interest. Format is {'city': 'Chicago'}
        - database = Location of unadjusted database

    Returns:
        - Integer of number of cities
    '''
 
    connection = sqlite3.connect(database)
    c = connection.cursor()

    search_string = '''SELECT COUNT(*) FROM restaurant '''

    # If city dictionary is empty, instead return overall result
    if city != {}:
        search_string += '''WHERE city = ?
            COLLATE NOCASE'''
        params = [city["city"]]
        result = c.execute(search_string, params)
    else:
         result = c.execute(search_string)
    result = result.fetchone()

    connection.commit()
    c.connection.close()

    return result[0]

def find_most_reviewed_restaurant(city, database):
    '''
    Finds the most reviewed restaurant and its review count

    Inputs:
        - city: City of interest. Format is {'city': 'Chicago'}
        - database = Location of unadjusted database

    Returns:
        - Most reviewed restauarant and review count as a list
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()

    search_string = '''SELECT name, reviews FROM restaurant '''
    
    if city != {}:
        search_string += '''WHERE city = ?
            COLLATE NOCASE'''
        params = [city["city"]]
        result = c.execute(search_string, params)
    else:
         result = c.execute(search_string)

    results = result.fetchall()

    # Sort by review count
    results = sorted(results, key=lambda x: x[1], reverse = True)

    connection.commit()
    c.connection.close()

    return results[0]

def find_consensus_restaurant(city, database, rating):
    '''
    Finds most reviewed restaurant at a given rating level.

    Inputs:
        - city: City of interest. Format is {'city': 'Chicago'}
        - database = Location of unadjusted database

    Returns:
        - Most reviewed restauarant and review count as a list
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()

    params = [rating]

    search_string = '''SELECT name, reviews, rating
    FROM restaurant
    WHERE rating = ?
    '''
    
    # Skip city restriction if no city is provided
    if city != {}:
        search_string += '''AND city = ?
            COLLATE NOCASE'''
        params.append(city["city"])

    result = c.execute(search_string, params)
    results = result.fetchall()

    # Sort by review count
    results = sorted(results, key=lambda x: x[1], reverse = True)

    connection.commit()
    c.connection.close()

    return results[0]


def summarize_all_cities(database):
    '''
    Collect summary table information, but for all cities
    '''

    total_restaurants = find_total_restaurants(city, database)
    starbucks_index = starbucks_mapper[city["city"]]
    most_reviewed = find_most_reviewed_restaurant(city, database)
    most_acclaimed = find_consensus_restaurant(city, database, rating = 5)
    most_hated = find_consensus_restaurant(city, database, rating = 1)
    
    # Construct Result List
    result_list = []
    result_list.append(("Total Restaurants in City:", total_restaurants))
    result_list.append(("Starbucks Distance Index:", 
        "{} Meters".format(starbucks_index)))
    result_list.append(("Most Reviewed Restaurant:", 
        "{}, {} Reviews".format(most_reviewed[0], most_reviewed[1])))
    result_list.append(("Most Reviewed 5-Star Restaurant:", 
        "{}, {} Reviews".format(most_acclaimed[0], most_acclaimed[1])))
    result_list.append(("Most Reviewed 1-Star Restaurant:", 
        "{}, {} Reviews".format(most_hated[0], most_hated[1])))

    return result_list