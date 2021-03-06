import requests
import re
import json
import csv

test_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=41.881832,-87.623177&radius=5000&type=restaurant&key="

# Uncomment whichever API key is still functional as you run the code.
# Camille's API key
API = "AIzaSyCP58u53oJ_brOYoNkF0ktaCE2EyZaJIyA"

# Emily's API key
# API = "AIzaSyDW15a3LCSe7J1YDRvUMWR1IsVlMxqQtRU"

# Austin's API key
# API = "AIzaSyB28WD_QVBYhUlO3fr22uMNr2zemUA7ZyQ"

# Fourth API key
# API = "AIzaSyDLWHjPZycWPeYui9yg2AM0own1IaVHIFc"

# Fifth API key
# API = "AIzaSyCkSm8tFiiEFSoXc9ixXNLlMD0N3O52sno"

def go():
    '''
    Loops over largest possible area in which restaurant data from that city could be found, 
    and pulls restaurant data from Google Maps API, which contains Zagat review data,
    using Nearby Searches and Place Searches.

    Theoretically, code should loop over cities and pull data. However, due to constantly having
    to change API keys mid-city, and inconsistencies in when the API keys stop working, functionally
    this only works with manual runs. The code structure has been left in for the go function to 
    demonstrate conceptual understanding of how it would work.

    '''
    full_results = []

    # Dictionary mapping city to lat lon location, and radius in miles
    locations = {"Chicago": [41.881832, -87.623177, 15.297]}#,
    #            "LA": [34.052235, -118.243683, 22.428]}
    #            "New York": [40.730610, -73.935242, 17.453]}
    #            "San Francisco": [37.733795, -122.446747, 6.846]}
    #            "Houston": [29.7604, -95.3698, 25.040]}
    
    for city in locations:
        city_name = city
        info = locations[city]

        # Converts radius from miles into lat/lon degrees
        radius_deg = info[2] / 69
        
        #lat = info[0] - radius_deg # COMMENT OUT IF MID CITY
        lat = 42.090136347826036 # UNCOMMENT IF MID CITY, manually input last stopping point printed in terminal
        #lon = info[1] - radius_deg # COMMENT OUT IF MID CITY
        lon = -87.39487265217385 # UNCOMMENT IF MID CITY, manually input last stopping point printed in terminal
        start_lon = info[1] - radius_deg
        stop_lat = info[0] + radius_deg
        stop_lon = info[1] + radius_deg

        csv_name = "zagat_" + city_name

        data, lat, lon = city_search(
            API, lat, lon, stop_lat, stop_lon, start_lon, csv_name)
        full_results = full_results + data

    # Print statements to make manually running the code possible
    print(city_name)
    print("lat:", lat)
    print("lon:", lon)

    return (city_name, lat, lon)

def city_search(API, lat, lon, stop_lat, stop_lon, start_lon, csv_name):
    '''
    Pull restaurant data from a Nearby Search in Google Maps for a lat/lon location, 
    writes to csv.

    Columns in data csv:
    ["name", "place_id", "street address", "city", "zipcode", "price_level", 
    "rating", "latitude", "longitude"])
    '''
    url_1 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    url_2 = "&radius=1000&type=restaurant&key="
    
    results = []
    request_num = 0
        
    while request_num < 100: # Manual limit, around the limit when keys stop working
        # Loops over city area, pulls restaurant results
        if lat >= stop_lat:
            print("finished searching city")
            break

        if lat <= stop_lat:            
            if lon < stop_lon:
                # Builds URL
                loc_url = "location=" + str(lat) + "," + str(lon)
                url = url_1 + loc_url + url_2 + API
                request_dict = get_results(url)
                print(request_dict["status"]) # Used to see when over query limit
                
                request_rows = get_info(request_dict, lat, lon)
                results.append(request_rows)

                # Write to csv
                with open (csv_name + ".csv",'a') as filedata:                            
                    writer = csv.writer(filedata, delimiter=',')
                    writer.writerows(request_rows)

            
                # If > 20 total locations, pulls data of next 20 results
                if "next_page_token" in request_dict:
                    request_dict = get_results(
                        "https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken=" 
                        + request_dict["next_page_token"] + "&key=" + API)
                    request_rows = get_info(request_dict, lat, lon)
                    results.append(request_rows)
                    with open (csv_name + ".csv",'a') as filedata:                            
                        writer = csv.writer(filedata, delimiter=',')
                        writer.writerows(request_rows)
                    request_num += 1
                    
                    # If > 40 total locations, pulls data of next 20 results
                    if "next_page_token" in request_dict:
                        request_dict = get_results(
                            "https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken=" 
                            + request_dict["next_page_token"] + "&key=" + API)
                        request_rows = get_info(request_dict, lat, lon)
                        results.append(request_rows)
                        with open (csv_name + ".csv",'a') as filedata:                            
                            writer = csv.writer(filedata, delimiter=',')
                            writer.writerows(request_rows)
                        request_num += 1
                
                lon += .01
                request_num += 1
                print(lat, lon)

            else:
                lon = start_lon
                lat += .01

    # Gets rid of duplicates
    results = list(uniq(results))

    return results, lat, lon

def get_info(request_dict, lat, lon):
    '''
    For each location found through Nearby Search, conduct a Place Search to pull
    address data from the latitude longitude coordinate.
    '''

    request_rows = []
    list_results = request_dict["results"]
    for result in list_results:
        name = result.get("name", None)
        place_id = result.get("place_id", None)
        
        # Pull address data through place search
        address_data = get_results(
            "https://maps.googleapis.com/maps/api/place/details/json?placeid=" 
            + place_id + "&key=" + API)
        if "result" in address_data:
            if "address_components" in address_data["result"]:
                address_components = address_data["result"]["address_components"]
                for component in address_components:
                    if "street_number" in component["types"]:
                        street_number = component.get("long_name", None)
                    elif "route" in component["types"]:
                        street = component.get("long_name", None)
                        try:
                            street_number
                        except NameError:
                            street_number = None
                        if street_number:
                            street = street_number + " " + street
                    elif "locality" in component["types"]:
                        city = component.get("long_name", None)
                    elif "postal_code" in component["types"]:
                        zipcode = component.get("long_name", None)

        # starter code for checking variable assignment found at
        # http://stackoverflow.com/questions/25666853/how-to-make-a-variable-
        # inside-a-try-except-block-public
        try:
            street
        except NameError:
            street = None
        try:
            city
        except NameError:
            city = None
        try:
            zipcode
        except NameError:
            zipcode = None
        
        price_level = result.get("price_level", None)
        rating = result.get("rating", None)
        request_rows.append([name, place_id, street, city, zipcode, price_level, rating, lat, lon])

    return request_rows


def uniq(lst):
    '''
    Iterates over list, removes duplicate entries
    '''
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item

def get_results(url):
    '''
    Stores page results in variable data. Dictionary with key "results"
    in the form of list of dictionaries of each result. Relevant keys:
    name, rating, place_id, next_page_token
    
    Input:
        - url

    Output:
        - list of result restaurants
    '''

    request = requests.get(url)
    data = request.json()
    with open('data.json', 'w') as f:
        json.dump(data, f)
    return data