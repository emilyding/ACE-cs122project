#testing

from math import radians, cos, sin, asin, sqrt
import sqlite3
import json
import re
import os


# Use this filename for the database
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'test1.db')


def simple_average():
    db = sqlite3.connect(DATABASE_FILENAME)
    c = db.cursor()
    query = "SELEC"+"T AVG(stars) FROM restaurant;"

    r = c.execute(query)

    results = r.fetchall()

    if results == None:
        return ([], [])

    #DATABASE_FILENAME.close()

    return (get_header(c), results)

def get_header(cursor):
    '''
    Given a cursor object, returns the appropriate header (column names)
    '''
    desc = cursor.description
    header = ()

    for i in desc:
        header = header + (clean_header(i[0]),)

    return list(header)


def clean_header(s):
    '''
    Removes table name from header
    '''
    for i in range(len(s)):
        if s[i] == ".":
            s = s[i+1:]
            break

    return s
