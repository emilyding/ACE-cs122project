\\\\\\\\\\\\\\\\\\\\\\\\\\\
\#########################\
\### Yelp SQL Queries ####\
\#########################\
\\\\\\\\\\\\\\\\\\\\\\\\\\\

Files in this folder are used to construct the tables, lists, and SQL queries
underpinning the information displayed on our website. Some of the code included
is unique to this folder - primarily code that creates graphs (which are made differently
through Django)

Non-py files:
all_restaurants.csv
cuisines_tags.csv
starbucks_index.csv

.db Files:
yelp_raw.db
yelp_adjusted.db

The above files, produced via files in yelp_data_assembly (with the exception
of cuisines_tags.csv, which is created via information from Yelp's website), 
are necessary asinputs of various functions and files within yelp_sql. 

.py files:
city_summary_stats.py
compare_cities.py
yelp_sql.py

city_summary_stats.py: Code in this file creates the header table displayed by 
the website's aggregator whenever data for a city is requested. It returns
the number of restaurants in a city, the starbucks index, the most reviewed 1
star and 5 star restaurant, and the most reviewed restaurant overall. It also
produces the summary stats for all cities seen when viewing results from all cities.

compare_cities.py: Code in this file creates matplotlib stacked bar graphs comparing
cuisines across different cities, as well as generating the table relating average
cuisine scores used for the same comparison on the website.  

yelp_sql.py: Code in this file conducts all dynamic analysis of data for our website, including top cities for a cuisine, top cuisines for a city, number of restaurants and average number of reviews per restaurant for a given rating, rating and number of restaurants and avergae number of reviews per restaurant for a given price bracket, all cuisines in a city, and cuisines with the most number of restaurants and ratings.
