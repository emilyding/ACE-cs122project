\\\\\\\\\\\\\\\\\\\\\\\\\\\
\#########################\
\### Zagat Comparison ####\
\#########################\
\\\\\\\\\\\\\\\\\\\\\\\\\\\

Files in this folder are used to scrape Zagat data for Chicago (although capability included
theoretically for other cities) and complete record linkage to match up entries with existing
Zagat data, and calculate the difference in averages across the two review sites. 
A full listing of all files, as well as explanations of their purpose, can be found below. 
Please note that each .py file includes summary information and usage instructions at the 
beginning of the file as well.

.py Files:
find_zagat_data.py
zagat_yelp_averages.py

.csv Files:
zagat_Chicago.csv

.db Files:
yelp_raw.db
zagat_raw.db


Python Files:

find_zagat_data.py: Code in this file uses user-supplied Zagat API credentials to
create a csv holding all necessary restaurant information for Chicago.
Note that this code must be run manually with checks since pulling data from Zagat
is prone to random errors due to inconsistencies with the API.

zagat_yelp_averages.py: Code in this file completes record linkage of Zagat entries 
with the Yelp data and calculates the overall average differences between the two sites for
Chicago. 


If a user wanted to construct our databases and get average differences from scratch, the following steps would be necessary:
- Run go() within file find_zagat_data.py and follow instructions in comments to
  get complete data for a city
- Run go() within file zagat_yelp_averages.py