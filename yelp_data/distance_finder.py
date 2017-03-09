# Distance Finder

'''
This program produces the "Starbucks Index" for a list of cities, given a csv
containing the coordinates for each restaurant. The index reflects the median
minimum distance necessary to travel from a random Starbucks to the nearest other 
Starbucks. 

Usage: The program can be ran by calling construct_city_index with the default 
parameters, or others preferred by the user.

Caffiene addicts can now learn where they ought to live.
'''


# Import necessary modules. sklearn requires installation, and installation
# requires both numpy and scipy to be installed. To run through a Windows machine,
# updated scipy installation required using Anaconda (or similar) to create an environment
# (Other downloaders/pip installs are not compatible)
import numpy as np
import pandas as pd
import random
import math
import time
import csv
from sklearn import neighbors
from statistics import median

def construct_city_index(filename = "starbucks_locations.csv", filepath = "starbucks_index.csv"):
    '''
    Given a csv of cities and associated lat/long pairs, find the median
    minimum distance between all points by city, and outputs to a csv.

    Inputs:
        - filename: The csv to pull data from 
        - filepath: The filename to save the index to

    Returns:
        - A list of tuples of city and median distance
    '''

    # Track run time
    start_time = time.clock()

    df = pd.read_csv(filename, usecols=["City", "Latitude", "Longitude"])
    city_list = df.City.unique()

    distance_index = []

    for city in city_list:
        sub_df = df[df["City"] == city]
        coordinate_tuples = list(zip(sub_df.Latitude, sub_df.Longitude))
        median_distance = get_median_distance(coordinate_tuples)
        distance_index.append((city, median_distance))

    # Convert to pandas dataframe
    headers = (["City", "Median Distance"])
    index_df = pd.DataFrame(distance_index, columns = headers)

    # Save to csv
    index_df.to_csv(filepath)

    print(time.clock() - start_time, "seconds")

    return index_df

def get_median_distance(points):
    '''
    Given a list of lat/long pairs, find the median of the minimum distances 
    between any two points. Distance is in kilometers.

    Inputs:
        - points: A list of tuples of lat/long pairs

    Returns:
        - An integer of the median kilometer distance
    '''

    # Convert to 3D coordinates
    projected_points = []
    for point in points:
        projected_points.append(convert_to_3d(point))

    # Find median min distance
    distance = find_median_min_distance(projected_points)

    return distance

def convert_to_3d(coordinates):
    '''
    Given a lat-long pair, converts to points on a 3D grid

    Inputs:
        coordinates: A tuple of latitude and longitude

    Returns:
       A tuple of 3-D coordinates

    '''

    # Radius of Earth (kilometers)
    # Note that changing this radius changes the units of the final distance
    R = 6371

    # Convert points to 3D grid. Insight into equations provided by:
    # http://stackoverflow.com/questions/1185408/converting-from-longitude-latitude-to-cartesian-coordinates
    x = R * math.cos(math.radians(coordinates[0])) * math.cos(math.radians(coordinates[1]))
    y = R * math.cos(math.radians(coordinates[0])) * math.sin(math.radians(coordinates[1]))
    z = R * math.sin(math.radians(coordinates[0]))

    return (x, y, z)

def find_median_min_distance(points):
    '''
    Given a list of 3D coordinates, constructs a BallTree and finds the distance
    to the nearest neighbor (besides the point itself) for each point. Algorithm 
    dramatically improves efficiency compared to checking every edge (estimated increase
    from n(n-1)/2 to n*log(n) according to most sources.)

    Documentation on the BallTree module can be found here:
    http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.BallTree.html#sklearn.neighbors.BallTree

    Inputs:
        - Points: A list of lat/long pairs (as tuples)

    Returns:
        - Integer median of the minimum distances
    '''

    tree = neighbors.BallTree(points)
    min_distances = []

    for i in range(len(points)):
        # Checks for missing coordinates (true of 6 out 23,319 Starbucks)
        if not math.isnan(points[i][0]):
            results = tree.query([points[i]], k=2) 
            path = results[0].item(1)
            min_distances.append(path)

    return median(min_distances)


##### Testing Functions ######
def go_fake(i):
    '''
    Function used for testing purposes. Generates fake lat/long pairs, converts
    them to a 3D grid, then finds the median_min_distance

    Inputs:
        - i: Number of datapoints to generate

    Returns:
        - Median minimum distance
    '''

    # Create fake lat/long pairs
    fake_data = generate_points(i)

    # Testing data with known distances. Locations are Snail Thai, Medici, and A10
    #fake_data = [(41.79119492, -87.59375), (41.79510918, -87.5847875), (41.7996924543722,-87.5893376827952)]

    # Convert data to 3D grid
    fake_globe_data = []
    for item in fake_data:
        globed = convert_to_3d(item)
        fake_globe_data.append(globed)

    # Track run time
    start_time = time.clock()

    # Find median min distance
    distance = find_median_min_distance(fake_globe_data)

    print(time.clock() - start_time, "seconds")

    return distance


def generate_points(i, lat_range = (40, 42), long_range = (-86, -88), rounding = 4):
    '''
    Constructs fake latitude/longitude information for testing purposes.
    Defaults are near Chicago

    Inputs:
        - i: The number of points to be generated
        - lat_range: The range of latitudes to be generated
        - long_range: The range of longitudes to be generated
        - rounding: Number of decimal places to store lat/long results

    Returns:
        - points: A list of tuples of lat/long pairs
    '''

    # Construct blank list to hold fake data
    points = []

    for entry in range(i):
        a = random.uniform(lat_range[0], lat_range[1])
        b = random.uniform(long_range[0], long_range[1])

        # Round resulting datapoints
        a = int(a*10*rounding + 0.5)/(10*rounding)
        b = int(b*10*rounding + 0.5)/(10*rounding)

        points.append((a,b))

    return points
