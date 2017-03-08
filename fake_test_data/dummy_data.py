# Create fake data

import random

city_list = ["Chicago", "New York City", "San Francisco", "Los Angeles", "Houston", 
    "Boston", "Seattle", "Kalamazoo"]  #length 8
cuisine_list = ["Mexican", "Chinese", "Fast Food", "American", "Sandwich", 
    "Seafood", "Italian", "Pizza", "BBQ", "Cafe", "Steak", "Sushi"]  #length 12

# Info to track per entry
# Unique_Id, City, Cuisine, Star Rating, Price raiting, Number of reviews

def generate_fake_data(req_count):
	'''
	Generate a table of fake data for use in calculations/observations. 
	Input is an integer of the desired # of data points, output is a list of lists.
	'''

	# Generate fake data
	uniq_id = 100000
	fake_data = []
	header = ["ID", "City", "Stars", "Price", "# Reviews", "Cuisine Tags"]
	fake_data.append(header)
	

	for i in range(req_count - 1):
		fake_entry = []

		uniq_id += 1
		fake_entry.append(uniq_id)

		city_seed = random.randrange(0, 8)
		fake_entry.append(city_list[city_seed])

		stars = round(random.uniform(1,5.005), 2)
		fake_entry.append(stars)

		price = round(random.uniform(1,5.005), 2)
		fake_entry.append(price)

		review_count = random.randrange(1, 101)
		fake_entry.append(review_count)

		# Generate 1-3 Cuisine tags
		cuisine_tags = []
		cuisine_seed_a = random.randrange(1, 101)
		if cuisine_seed_a < 60:
			cuisine_seed_b = random.randrange(0, 12)
			cuisine_tags.append(cuisine_list[cuisine_seed_b])
		elif cuisine_seed_a < 85:
			cuisine_seed_b = random.randrange(0, 12)
			cuisine_seed_c = random.randrange(0, 12)
			cuisine_tags.append(cuisine_list[cuisine_seed_b])
			if cuisine_seed_c != cuisine_seed_b:
			    cuisine_tags.append(cuisine_list[cuisine_seed_c])
		else:
			cuisine_seed_b = random.randrange(0, 12)
			cuisine_seed_c = random.randrange(0, 12)
			cuisine_seed_d = random.randrange(0, 12)
			cuisine_tags.append(cuisine_list[cuisine_seed_b])
			if cuisine_seed_c != cuisine_seed_b:
			    cuisine_tags.append(cuisine_list[cuisine_seed_c])
			if cuisine_seed_d != cuisine_seed_c and cuisine_seed_d != cuisine_seed_b:
				cuisine_tags.append(cuisine_list[cuisine_seed_d])

		fake_entry.append(cuisine_tags)

		fake_data.append(fake_entry)

	return fake_data
		


