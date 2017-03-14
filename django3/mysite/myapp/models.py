'''
This file writes models using django capacity. 
The file contains Question and Choice which are used for learning and testing and is not used for the website. It also contains Compare, Cuisine, and Comment.
'''

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
#just in case, to pass data to rendering
from django.utils.safestring import mark_safe

#these two classes are from the Django Tutorial. They are included for
#testing purposes and are never displayed in the website.


class Question(models.Model):
    '''
    The Question model contains three fields:
        question_text: to input text for question_text
        pub_date: uses date time to designate data/time. IF USED, PLEASE IMPORT timezone
    '''
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        #self is named with a string (the question text)
        return self.question_text
    def was_published_recently(self):
        # a function to determine if question was published recently.
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    '''
    The Choice model contains answer choices. It is linked to Questions.

    Fields contained:
        question: the question it is linked to
        choice_text: a string input for choice text
        votes: how many votes there has been. 
    '''
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        #choices are named with a string after choice_text
        return self.choice_text

#all the choice options for cities in our data. Referenced in dropdowns.
CITY_CHOICES = (
     ('Albuquerque', 'Albuquerque'),
     ('Arlington', 'Arlington'),
     ('Atlanta', 'Atlanta'),
     ('Austin', 'Austin'),
     ('Baltimore', 'Baltimore'),
     ('Boston', 'Boston'),
     ('Buffalo', 'Buffalo'),
     ('Charlotte', 'Charlotte'),
     ('Chicago', 'Chicago'),
     ('Cleveland', 'Cleveland'),
     ('Colorado Springs', 'Colorado Springs'),
     ('Columbus', 'Columbus'),
     ('Dallas', 'Dallas'),
     ('Denver', 'Denver'),
     ('Detroit', 'Detroit'),
     ('El Paso', 'El Paso'),
     ('Fort Worth', 'Fort Worth'),
     ('Fresno', 'Fresno'),
     ('Honolulu', 'Honolulu'),
     ('Houston', 'Houston'),
     ('Indianapolis', 'Indianapolis'),
     ('Jacksonville', 'Jacksonville'),
     ('Kansas City', 'Kansas City'),
     ('Las Vegas', 'Las Vegas'),
     ('Long Beach', 'Long Beach'),
     ('Los Angeles', 'Los Angeles'),
     ('Louisville', 'Louisville'),
     ('Memphis', 'Memphis'),
     ('Mesa', 'Mesa'),
     ('Miami', 'Miami'),
     ('Milwaukee', 'Milwaukee'),
     ('Minneapolis', 'Minneapolis'),
     ('Nashville', 'Nashville'),
     ('New Orleans', 'New Orleans'),
     ('New York', 'New York'),
     ('Oakland', 'Oakland'),
     ('Oklahoma City', 'Oklahoma City'),
     ('Omaha', 'Omaha'),
     ('Philadelphia', 'Philadelphia'),
     ('Phoenix', 'Phoenix'),
     ('Pittsburgh', 'Pittsburgh'),
     ('Portland', 'Portland'),
     ('Raleigh', 'Raleigh'),
     ('Sacramento', 'Sacramento'),
     ('San Antonio', 'San Antonio'),
     ('San Diego', 'San Diego'),
     ('San Francisco', 'San Francisco'),
     ('San Jose', 'San Jose'),
     ('Seattle', 'Seattle'),
     ('St Louis', 'St Louis'),
     ('St Paul', 'St Paul'),
     ('Tampa', 'Tampa'),
     ('Tucson', 'Tucson'),
     ('Tulsa', 'Tulsa'),
     ('Virginia Beach', 'Virginia Beach'),
     ('Washington DC', 'Washington DC')
)

#All Price Choices that is inclued in data. Referenced in dropdown.
PRICE_CHOICES = (
    ('$','$'),
    ('$$', '$$'),
    ('$$$','$$$'),
    ('$$$$','$$$$')
)

# Choices for upper limit. Taken out as a feature.

NUM_CHOICES = (
    ('5','5'),
    ('10', '10'),
    ('25','25'),
    ('50','50'),
    ('All','All')
)

#Choices for best/worst dropdown.
BW_CHOICES = (
    ('Best','Best'),
    ('Worst', 'Worst')
)

#All cuisine tags in our data. Referenced in dropdown.
CUISINE_CHOICES = (
     ('None', "--"),
     ('Afghan', 'Afghan'),
     ('African', 'African'),
     ('Senegalese', 'Senegalese'),
     ('SouthAfrican', 'South African'),
     ('American(New)', 'American (New)'),
     ('American(Traditional)', 'American (Traditional)'),
     ('Arabian', 'Arabian'),
     ('Argentine', 'Argentine'),
     ('Armenian', 'Armenian'),
     ('AsianFusion', 'Asian Fusion'),
     ('Australian', 'Australian'),
     ('Austrian', 'Austrian'),
     ('Bangladeshi', 'Bangladeshi'),
     ('Barbeque', 'Barbeque'),
     ('Basque', 'Basque'),
     ('Belgian', 'Belgian'),
     ('Brasseries', 'Brasseries'),
     ('Brazilian', 'Brazilian'),
     ('Breakfast&Brunch', 'Breakfast & Brunch'),
     ('British', 'British'),
     ('Buffets', 'Buffets'),
     ('Burgers', 'Burgers'),
     ('Burmese', 'Burmese'),
     ('Cafes', 'Cafes'),
     ('ThemedCafes', 'Themed Cafes'),
     ('Cafeteria', 'Cafeteria'),
     ('Cajun/Creole', 'Cajun/Creole'),
     ('Cambodian', 'Cambodian'),
     ('Caribbean', 'Caribbean'),
     ('Dominican', 'Dominican'),
     ('Haitian', 'Haitian'),
     ('PuertoRican', 'Puerto Rican'),
     ('Trinidadian', 'Trinidadian'),
     ('Catalan', 'Catalan'),
     ('Cheesesteaks', 'Cheesesteaks'),
     ('ChickenShop', 'Chicken Shop'),
     ('ChickenWings', 'Chicken Wings'),
     ('Chinese', 'Chinese'),
     ('Cantonese', 'Cantonese'),
     ('DimSum', 'Dim Sum'),
     ('Hainan', 'Hainan'),
     ('Shanghainese', 'Shanghainese'),
     ('Szechuan', 'Szechuan'),
     ('ComfortFood', 'Comfort Food'),
     ('Creperies', 'Creperies'),
     ('Cuban', 'Cuban'),
     ('Czech', 'Czech'),
     ('Delis', 'Delis'),
     ('Diners', 'Diners'),
     ('DinnerTheater', 'Dinner Theater'),
     ('Ethiopian', 'Ethiopian'),
     ('FastFood', 'Fast Food'),
     ('Filipino', 'Filipino'),
     ('Fish&Chips', 'Fish & Chips'),
     ('Fondue', 'Fondue'),
     ('FoodCourt', 'Food Court'),
     ('FoodStands', 'Food Stands'),
     ('French', 'French'),
     ('Mauritius', 'Mauritius'),
     ('Reunion', 'Reunion'),
     ('Gastropubs', 'Gastropubs'),
     ('German', 'German'),
     ('Gluten-Free', 'Gluten-Free'),
     ('Greek', 'Greek'),
     ('Guamanian', 'Guamanian'),
     ('Halal', 'Halal'),
     ('Hawaiian', 'Hawaiian'),
     ('Himalayan/Nepalese', 'Himalayan/Nepalese'),
     ('Honduran', 'Honduran'),
     ('HongKong Style Cafe', 'Hong Kong Style Cafe'),
     ('HotDogs', 'Hot Dogs'),
     ('HotPot', 'Hot Pot'),
     ('Hungarian', 'Hungarian'),
     ('Iberian', 'Iberian'),
     ('Indian', 'Indian'),
     ('Indonesian', 'Indonesian'),
     ('Irish', 'Irish'),
     ('Italian', 'Italian'),
     ('Calabrian', 'Calabrian'),
     ('Sardinian', 'Sardinian'),
     ('Tuscan', 'Tuscan'),
     ('Japanese', 'Japanese'),
     ('Conveyor Belt Sushi', 'Conveyor Belt Sushi'),
     ('Izakaya', 'Izakaya'),
     ('Japanese Curry', 'Japanese Curry'),
     ('Ramen', 'Ramen'),
     ('Teppanyaki', 'Teppanyaki'),
     ('Kebab', 'Kebab'),
     ('Korean', 'Korean'),
     ('Kosher', 'Kosher'),
     ('Laotian', 'Laotian'),
     ('LatinAmerican', 'Latin American'),
     ('Colombian', 'Colombian'),
     ('Salvadoran', 'Salvadoran'),
     ('Venezuelan', 'Venezuelan'),
     ('Live/Raw Food', 'Live/Raw Food'),
     ('Malaysian', 'Malaysian'),
     ('Mediterranean', 'Mediterranean'),
     ('Falafel', 'Falafel'),
     ('Mexican', 'Mexican'),
     ('Tacos', 'Tacos'),
     ('Middle Eastern', 'Middle Eastern'),
     ('Egyptian', 'Egyptian'),
     ('Lebanese', 'Lebanese'),
     ('ModernEuropean', 'Modern European'),
     ('Mongolian', 'Mongolian'),
     ('Moroccan', 'Moroccan'),
     ('NewMexicanCuisine', 'New Mexican Cuisine'),
     ('Nicaraguan', 'Nicaraguan'),
     ('Noodles', 'Noodles'),
     ('Pakistani', 'Pakistani'),
     ('PanAsian', 'Pan Asian'),
     ('Persian/Iranian', 'Persian/Iranian'),
     ('Peruvian', 'Peruvian'),
     ('Pizza', 'Pizza'),
     ('Polish', 'Polish'),
     ('Pop-UpRestaurants', 'Pop-Up Restaurants'),
     ('Portuguese', 'Portuguese'),
     ('Poutineries', 'Poutineries'),
     ('Russian', 'Russian'),
     ('Salad', 'Salad'),
     ('Sandwiches', 'Sandwiches'),
     ('Scandinavian', 'Scandinavian'),
     ('Scottish', 'Scottish'),
     ('Seafood', 'Seafood'),
     ('Singaporean', 'Singaporean'),
     ('Slovakian', 'Slovakian'),
     ('SoulFood', 'Soul Food'),
     ('Soup', 'Soup'),
     ('Southern', 'Southern'),
     ('Spanish', 'Spanish'),
     ('SriLankan', 'Sri Lankan'),
     ('Steakhouses', 'Steakhouses'),
     ('SupperClubs', 'Supper Clubs'),
     ('SushiBars', 'Sushi Bars'),
     ('Syrian', 'Syrian'),
     ('Taiwanese', 'Taiwanese'),
     ('TapasBars', 'Tapas Bars'),
     ('Tapas/Small Plates', 'Tapas/Small Plates'),
     ('Tex-Mex', 'Tex-Mex'),
     ('Thai', 'Thai'),
     ('Turkish', 'Turkish'),
     ('Ukrainian', 'Ukrainian'),
     ('Uzbek', 'Uzbek'),
     ('Vegan', 'Vegan'),
     ('Vegetarian', 'Vegetarian'),
     ('Vietnamese', 'Vietnamese'),
     ('Waffles', 'Waffles'),
     ('Wraps', 'Wraps')
)

class Comment(models.Model):
    '''
    The Comment model allows user to input when generating a city snapshot
    Contains the following fields:
        auto_increment_id: primary key id for each input
        city: designated city for snapshot lookup
        price_limit: upper limit on prices of restaurants that is searched and aggregated
            for top cuisines.
        num_limit: (discontinued feature because makes website slow) 
            allows user to input upper limit on number of restaruants returned for "top cuisines"
        best_worst: a field to designate whether user is interested in best or worst cuisine
    '''
    auto_increment_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=100, choices = CITY_CHOICES, default='Chicago', verbose_name = "Please Choose a City")
    price_limit = models.CharField(max_length=4, choices = PRICE_CHOICES, default='$$$$', verbose_name = "Max Price")
    # Note: field num_limit is included for grading but is not used in site.
    num_limit = models.CharField(max_length=10, choices = NUM_CHOICES, default='5', verbose_name = "Max Number of Results")
    best_worst = models.CharField(max_length=10, choices = BW_CHOICES, default='Best', verbose_name= "Specify Best or Worst")
    def __int__(self):   
        #class is named and refered to by id
        return self.auto_increment_id
    def make_dict(self):
        #a function to format input to use in views. makes a dictionary.
        args = {"city": self.city, "price": self.price_limit, "limit": self.num_limit, "worst": self.best_worst}
        return args

class Compare(models.Model):
    '''
    The Compare model allows user to input two cities and a cuisine when comparing two cities.
    Contains the following dropdown fields:
        idd: primary key id for each input
        city1: city 1 to compare
        city2: city 2 to compare
        cuisine: if user is interested in cuisine, can designate and compare across two cities.
    '''
    idd = models.AutoField(primary_key= True)
    city1 = models.CharField(max_length=100, choices= CITY_CHOICES, default = 'Chicago', verbose_name = "Choose City 1")
    city2 = models.CharField(max_length = 100, choices = CITY_CHOICES, default= 'New York', verbose_name = "Choose City 2")
    cuisine = models.CharField(max_length = 100, choices = CUISINE_CHOICES, default = 'Waffle', verbose_name = "If you would like to specify a cuisine for comparison, choose here:")
    def __int__(self):
        #Compare class is identified and named as an integer 
        return self.idd
    def make_dict(self):
        #a function to format input to use in views. makes a dictionary.
        args = ({'city': self.city1}, {'city': self.city2}, self.cuisine)
        return args

class Cuisine(models.Model):
    '''
    The Compare model allows user to input cuisine to find top cities.
    Contains the following (dropdown) fields:
        idd: primary key id for each input (not dropdown)
        cuisine: if user is interested in cuisine, can designate and lookup best cities (dropdown)
    '''
    idd = models.AutoField(primary_key= True)
    cuisine = models.CharField(max_length = 100, choices = CUISINE_CHOICES, default = 'Waffle', verbose_name = "To find top city for a cuisine, choose cuisine here:")
    def __int__(self):
        return self.idd
    def make_dict(self):
        return self.cuisine
