
import numpy as np
import random
import math
from sklearn import neighbors
from statistics import mean

def go(i):
    '''
    Test function
    '''

    fake_data = generate_points(i)
    fake_globe_data = []

    for item in fake_data:
        globed = convert_to_3d(item)
        fake_globe_data.append(globed)

    distance = find_average_min_distance(fake_globe_data)

    return distance


def generate_points(i):
    # Count iterations
    points = []

    for entry in range(i):
        a = random.uniform(70, 75)
        a = int(a*10000 + 0.5)/10000
        b = random.uniform(70, 75)
        b = int(b*10000 + 0.5)/10000
        points.append((a,b))
    return points

def convert_to_3d(coordinates):
    '''
    Given a lat-long pair, converts to points on a 3D grid

    Inputs:
        coordinates: A tuple of latitude and longitude

    Returns:
       A tuple of 3-D coordinates

    '''

    # Radius of Earth (meters)
    R = 6371000

    x = R * math.cos(math.radians(coordinates[0])) * math.cos(math.radians(coordinates[1]))
    y = R * math.cos(math.radians(coordinates[0])) * math.sin(math.radians(coordinates[1]))
    z = R * math.sin(math.radians(coordinates[0]))

    return (x, y, z)

def find_average_min_distance(points):
    '''
    if it works tho
    '''

    tree = neighbors.BallTree(points)
    min_distances = []

    for i in range(len(points)):
        results = tree.query([points[i]], k=2) 
        path = results[0].item(1)
        min_distances.append(path)

    average_min_distance = mean(min_distances)

    return average_min_distance
