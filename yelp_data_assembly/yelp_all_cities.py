import sqlite3
import csv
import string
import math
import matplotlib.pyplot as plt
import statistics as stat
import numpy as np
import pandas as pd
from pandas.tools.plotting import table

def best_cuisines(database = "yelp_adjusted.db"):
    '''
    Gets best cuisines across cities
    '''

    connection = sqlite3.connect(database)
    c = connection.cursor()
    
    search_string = '''SELECT cuisine, AVG(rating), SUM(reviews) as num_reviews
    FROM restaurant
    JOIN cuisines
    ON restaurant.id = cuisines.id
    WHERE reviews > 10
    GROUP BY cuisine
    '''

    results = c.execute(search_string)
    result_table = results.fetchall()
    result_table.sort(key = lambda x: x[1], reverse = True)
    result_table = result_table[:10]

    connection.commit()
    c.connection.close()
    
    result_frame = pd.DataFrame(result_table, 
        columns=["Cuisine", "Rating", "# Reviews"])
    result_frame = result_frame.round(2)
    result_list = result_frame.values.tolist()

    return result_list