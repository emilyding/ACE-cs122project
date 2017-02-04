API_key = "AIzaSyCP58u53oJ_brOYoNkF0ktaCE2EyZaJIyA"

import requests
import re
import util
import bs4
import queue
import json
import sys
import csv
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=500&type=restaurant&keyword=cruise&key=AIzaSyCP58u53oJ_brOYoNkF0ktaCE2EyZaJIyA&callback=?"
#url = "https://www.zagat.com/r/goosefoot-chicago"
def cook_soup(url):
    request = requests.get(url)
    data = request.json()
    with open('data.json', 'w') as f:
        json.dump(data, f)
    #data now stored in variable data

#    encoding = request.encoding
#    html = request.text.encode(encoding)
#    soup = bs4.BeautifulSoup(html, "html5lib")

#    return soup


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