# Create fake data

import random
import itertools
import copy 

city_list = ["Chicago", "New York City", "San Francisco", "Los Angeles", "Houston", 
    "Boston", "Seattle", "Kalamazoo", "DC", "Miami", "Philidelphia", "Portland",
    "Pompeii", "Atlantis"]  #length 14
cuisine_list = ["American", "Asian Fusion", "BBQ", "Cafe", "Chinese",
    "Fast Food", "Indian", "Italian", "Mediterranean", "Mexican", "Pizza", 
    "Sandwich", "Seafood", "Steak", "Sushi", "Thai", ]  #length 16
source_site = ["Yelp", "TripAdvisor", "Zomato", "OpenTable"] # length 4

cuisine_ratings = {
    "American": (1, 3),
    "Asian Fusion": (1, 4),
    "BBQ": (3, 5),
    "Cafe": (2, 4),
    "Chinese": (1, 4),
    "Fast Food": (2, 3),
    "Indian": (1, 5),
    "Italian": (1, 3),
    "Mediterranean": (3, 5),
    "Mexican": (2, 5),
    "Pizza": (3, 4),
    "Sandwich": (2, 3),
    "Seafood": (1, 5),
    "Steak": (2, 3),
    "Sushi": (2, 4),
    "Thai": (4, 5)
}

###### ADDING THINGS TO FAKE DATA STEPS ########
# Add the list you want to draw from
# Add an appending section to generate_fake_data
# Add the content to the header
# Change the index that references cuisine tags in both files
# Change the table in generate_raw_table
# Change the add_data line in add_data (add a ? mark)

###### Generating a database #######
# run both files
# fake_data = generate_fake_data(some_number)
# create_table("fake.db")
# add_data("fake.db", fake_data)


def generate_fake_data(req_count):
    '''
    Generate a table of fake data for use in calculations/observations. 
    Input is an integer of the desired # of data points, output is a list of lists.
    '''

    # Generate fake data
    uniq_id = 100000
    fake_data = []
    header = ["ID", "City", "Source", "Price", "# Reviews", "Cuisine Tags", "Stars"]
    #fake_data.append(header)
    

    for i in range(req_count):
        fake_entry = []

        uniq_id += 1
        fake_entry.append(uniq_id)

        city_seed = random.randrange(0, 14)
        fake_entry.append(city_list[city_seed])

        source_seed = random.randrange(0, 4)
        fake_entry.append(source_site[source_seed])

        price = round(random.uniform(1,5.005), 2)
        fake_entry.append(price)

        review_count = random.randrange(1, 101)
        fake_entry.append(review_count)

        # Generate 1-3 Cuisine tags
        cuisine_tags = []
        cuisine_seed_a = random.randrange(1, 101)
        if cuisine_seed_a < 60:
            cuisine_seed_b = random.randrange(0, 16)
            cuisine_tags.append(cuisine_list[cuisine_seed_b])
        elif cuisine_seed_a < 85:
            cuisine_seed_b = random.randrange(0, 16)
            cuisine_seed_c = random.randrange(0, 16)
            cuisine_tags.append(cuisine_list[cuisine_seed_b])
            if cuisine_seed_c != cuisine_seed_b:
                cuisine_tags.append(cuisine_list[cuisine_seed_c])
        else:
            cuisine_seed_b = random.randrange(0, 16)
            cuisine_seed_c = random.randrange(0, 16)
            cuisine_seed_d = random.randrange(0, 16)
            cuisine_tags.append(cuisine_list[cuisine_seed_b])
            if cuisine_seed_c != cuisine_seed_b:
                cuisine_tags.append(cuisine_list[cuisine_seed_c])
            if cuisine_seed_d != cuisine_seed_c and cuisine_seed_d != cuisine_seed_b:
                cuisine_tags.append(cuisine_list[cuisine_seed_d])

        fake_entry.append(cuisine_tags)

        # Generates ratings randomly from star distributions of cuisine tag.
        # If multiple tags, gets rating from averaged distribution.
        
        num_cuisines = len(cuisine_tags)
        min_num = 0
        max_num = 0
        
        for tag in cuisine_tags:
            min_num += cuisine_ratings[tag][0]
            max_num += cuisine_ratings[tag][1]
        
        low_star = min_num / num_cuisines
        high_star = max_num / num_cuisines
        stars = round(random.uniform(low_star, high_star), 2)
        fake_entry.append(stars)

        fake_data.append(fake_entry)

    return fake_data
        

# This one doesn't really matter
def calculate_cuisine_score(data, cuisine):
    chinese_a = 0
    chinese_rating_a = []
    chinese_b = 0
    chinese_rating_b = []
    for entry in data:
        if entry[1] == "New York City":
            if "Chinese" in entry[6]:
                chinese_a += 1
                chinese_rating_a.append(entry[2])
        if entry[1] == "Chicago":
            if "Chinese" in entry[6]:
                chinese_b += 1
                chinese_rating_b.append(entry[2])


    avg_chinese_a = sum(chinese_rating_a)/len(chinese_rating_a)
    avg_chinese_b = sum(chinese_rating_b)/len(chinese_rating_b)
    result_table = ["City", "Cuisine", "# of Entries", "Average Rating"]
    result_table.append(["Chicago", "Chinese", chinese_b, avg_chinese_b])
    result_table.append(["New York", "Chinese", chinese_a, avg_chinese_a])

    return result_table
