\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

\##############################\

\###         Mysite        ####\

\##############################\

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

Welcome to /mysite/mysite! 

Here you will find the following directories:
	myapp : a directory for myapp which supports interactive functionality through forms
	mysite : a directory created when django project was initiated. Contains python packages for running the site
	_pycache : a directory of cached files (that we are afraid to clear, just in case)
	Not Used (Testing Only): a directory of old file that did not end up getting used (are kept for backup purposes only). These files are for testing links and functions.


Databases:
	db.sqlite3 : sql database for the django framework. Contains all migrations.
	yelp_raw.db : sql database containing raw data pulled from yelp api
	yelp_adjusted.db : sql database containing adjusted values for yelp data. Data is normalized to city averages. 

And files:
	city_summary_stats.py : contains python functions to collect, aggregate, and return summary information (fun facts)
	compare_cities.py : contains python functions to compare two cities to return data on which city has better food by cuisine
	cuisines_tags.csv : compare_cities.py refers to this file. CSV contains all data on which cuisine tags exist in the database. 
	yelp_all_cities.py : contains a function to return ranked list of all cuisines
	yelp_sql_nograph.py : contains python functions to aggregate data for the city snapshot, such as top 5 best/worst cuisines, price: rating comparisons, common cuisines, etc.
	
	manage.py : django shell for running the server

