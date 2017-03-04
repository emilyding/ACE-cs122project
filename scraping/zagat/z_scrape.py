import requests
import re
#import bs4
import json
#import sys
import csv

test_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=41.881832,-87.623177&radius=5000&type=restaurant&key="
#url = "https://www.zagat.com/r/goosefoot-chicago"

def run_code():
    # Camille's API
    API = "AIzaSyCP58u53oJ_brOYoNkF0ktaCE2EyZaJIyA"
    
    # Emily's API
    #API = "AIzaSyDW15a3LCSe7J1YDRvUMWR1IsVlMxqQtRU"
    
    # Austin's API
    # API = "AIzaSyB28WD_QVBYhUlO3fr22uMNr2zemUA7ZyQ"
    run_number = 1 #haven't done this one yet
    full_results = []

    # locations dict with key city: [lat, long, radius (est.)]
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
        
        lat = info[0] - radius_deg # COMMENT OUT IF MID CITY
        #lat = 42.040136347826036# UNCOMMENT IF MID CITY
        lon = info[1] - radius_deg # COMMENT OUT IF MID CITY
        #lon = -87.69487265217385# UNCOMMENT IF MID CITY
        start_lon = info[1] - radius_deg
        stop_lat = info[0] + radius_deg
        stop_lon = info[1] + radius_deg

        data, lat, lon = cook_soup(
            API, lat, lon, stop_lat, stop_lon, start_lon)
        full_results = full_results + data

    print(city_name)
    print("lat:", lat)
    print("lon:", lon)

    csv_name = "zagat_" + city_name + "_" + str(run_number) + ".csv"
    with open(csv_name,"w") as f:
        wr = csv.writer(f)
        wr.writerows([["name", "place_id", "street address", "city", "zipcode" "price_level", "rating"]] + full_results)

    return (city_name, lat, lon)

def cook_soup(API, lat, lon, stop_lat, stop_lon, start_lon):
    url_1 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    url_2 = "&radius=1000&type=restaurant&key="
    
    results = []
    request_num = 0
        
    while request_num < 500: #- 3:
        # Loops over city area, pulls restaurant results
        if lat >= stop_lat:
            print("finished searching city")
            break

        if lat <= stop_lat:            
            if lon < stop_lon:
                loc_url = "location=" + str(lat) + "," + str(lon)
                url = url_1 + loc_url + url_2 + API
                request_dict = get_results(url)
                print(request_dict["status"])
                list_results = request_dict["results"]
                for result in list_results:
                    name = result.get("name", None)
                    place_id = result.get("place_id", None)
                    address_data = get_results(
                        "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + place_id + "&key=" + API)
                    if "result" in address_data:
                        if "address_components" in address_data["result"]:
                            address_components = address_data["result"]["address_components"]
                            for component in address_components:
                                if "street_number" in component["types"]:
                                    street_number = component.get("long_name", None)
                                elif "route" in component["types"]:
                                    street = component.get("long_name", None)
                                    street = street_number + " " + street
                                elif "locality" in component["types"]:
                                    city = component.get("long_name", None)
                                elif "postal_code" in component["types"]:
                                    zipcode = component.get("long_name", None)
                        else:
                            street = None
                            city = None
                            zipcode = None 
                    else:
                        street = None
                        city = None
                        zipcode = None
                    price_level = result.get("price_level", None)
                    rating = result.get("rating", None)
                    results.append([name, place_id, street, city, zipcode, price_level, rating])
            
                # If > 20 locations, pulls up to 40 more
                if "next_page_token" in request_dict:
                    request_dict = get_results(
                        "https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken=" 
                        + request_dict["next_page_token"] + "&key=" + API)
                    list_results = request_dict["results"]
                    for result in list_results:
                        name = result.get("name", None)
                        place_id = result.get("place_id", None)
                        address_data = get_results(
                            "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + place_id + "&key=" + API)
                        if "result" in address_data:
                            if "address_components" in address_data["result"]:
                                address_components = address_data["result"]["address_components"]
                                for component in address_components:
                                    if "street_number" in component["types"]:
                                        street_number = component.get("long_name", None)
                                    elif "route" in component["types"]:
                                        street = component.get("long_name", None)
                                        street = street_number + " " + street
                                    elif "locality" in component["types"]:
                                        city = component.get("long_name", None)
                                    elif "postal_code" in component["types"]:
                                        zipcode = component.get("long_name", None)
                            else:
                                street = None
                                city = None
                                zipcode = None 
                        else:
                            street = None
                            city = None
                            zipcode = None
                        price_level = result.get("price_level", None)
                        rating = result.get("rating", None)
                        results.append([name, place_id, street, city, zipcode, price_level, rating])
                    request_num += 1
                    
                    if "next_page_token" in request_dict:
                        request_dict = get_results(
                            "https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken=" 
                            + request_dict["next_page_token"] + "&key=" + API)
                        list_results = request_dict["results"]
                        for result in list_results:
                            name = result.get("name", None)
                            place_id = result.get("place_id", None)
                            address_data = get_results(
                                "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + place_id + "&key=" + API)
                            if "result" in address_data:
                                if "address_components" in address_data["result"]:
                                    address_components = address_data["result"]["address_components"]
                                    for component in address_components:
                                        if "street_number" in component["types"]:
                                            street_number = component.get("long_name", None)
                                        elif "route" in component["types"]:
                                            street = component.get("long_name", None)
                                            street = street_number + " " + street
                                        elif "locality" in component["types"]:
                                            city = component.get("long_name", None)
                                        elif "postal_code" in component["types"]:
                                            zipcode = component.get("long_name", None)
                                else:
                                    street = None
                                    city = None
                                    zipcode = None 
                            else:
                                street = None
                                city = None
                                zipcode = None
                            price_level = result.get("price_level", None)
                            rating = result.get("rating", None)
                            results.append([name, place_id, street, city, zipcode, price_level, rating])
                        request_num += 1
                lon += .01
                request_num += 1
                print(lat, lon)

            else:
                lon = start_lon
                lat += .01

    # Gets rid of duplicates
    results = list(uniq(sorted(results, reverse=True)))

    return results, lat, lon

def uniq(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item

def get_results(url):
    '''
    Input:
        - url
    Output:
        - list of result restaurants
    '''
    # Stores page results in variable data. Dictionary with key "results"
    # in the form of list of dictionaries of each result. Relevant keys:
    # name, rating, place_id, next_page_token

    request = requests.get(url)
    data = request.json()
    with open('data.json', 'w') as f:
        json.dump(data, f)
    return data



#    encoding = request.encoding
#    html = request.text.encode(encoding)
#    soup = bs4.BeautifulSoup(html, "html5lib")

#    return soup
'''

def get_info(soup):
    name_tag = soup.find_all('h1', id = "main-content-title")
    name = name_tag[0].text

##
    info_tag = soup.find_all('span', class_ = "info--header", limit = 3)
    cuisine = info_tag[0].text
    rating = info_tag[2].text

    price_tag = soup.find_all('div', class_ = "detail first price_rating separator")
    price = price_tag[0].text
    price = price.replace("\n", "")

    
    cuisine_all = soup.find_all('div', class_ = "detail separator")
    cuisine_tags = cuisine_all[0].find_all('a')
    cuisine = []
    for cuisine_tag in cuisine_tags:
        cuisine.append(cuisine_tag.text)

    address_tag = soup.find_all('span', property = "streetAddress")
    address = address_tag[0].text

    city_tag = soup.find_all('span', property = "addressLocality")
    city = city_tag[0].text

    state_tag = soup.find_all('span', property = "addressRegion")
    state = state_tag[0].text

    country_tag = soup.find_all('span', property = "addressCountry")
    country = country_tag[0]["content"]

    zipcode_tag = soup.find_all('span', property = "postalCode")
    zipcode = zipcode_tag[0].text

    phone_tag = soup.find_all('div', class_ = "fl phoneNumber")
    phone = phone_tag[0].text
    phone = re.findall("[0-9-]{12}", phone)
    phone = phone[0].replace("-", "")
    # returns in form 3126671701

    restaurant_info = {
    "name": name,
    "rating": rating,
    "price": price
    "cuisine": cuisine
    "address": address, 
    "city": city,
    "state": state, 
    "zipcode": zipcode,
    "country": country,
    "phone": phone

    }

    return restaurant_info

#name = re.findall()

#    lower_text = text.lower()
#    word_list = []

#    words = re.findall("[A-Za-z]\w*", lower_text)
'''