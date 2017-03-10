from django.db import models
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    selection = ""
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text



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
     ('NashvilleNew Orleans', 'NashvilleNew Orleans'),
     ('New York', 'New York'),
     ('Oakland', 'Oakland'),
     ('Oklahoma CityOmaha', 'Oklahoma CityOmaha'),
     ('Philadelphia', 'Philadelphia'),
     ('Phoenix', 'Phoenix'),
     ('Pittsburgh', 'Pittsburgh'),
     ('Portland', 'Portland'),
     ('Raleigh', 'Raleigh'),
     ('Sacramento', 'Sacramento'),
     ('San Antonio', 'San Antonio'),
     ('San Diego', 'San Diego'),
     ('San Francisco', 'San Francisco'),
     ('San JoseSeattleSt Louis', 'San JoseSeattleSt Louis'),
     ('St Paul', 'St Paul'),
     ('Tampa', 'Tampa'),
     ('Tucson', 'Tucson'),
     ('Tulsa', 'Tulsa'),
     ('Virginia Beach', 'Virginia Beach'),
     ('Washington DC', 'Washington DC')
)

PRICE_CHOICES = (
    ('$','$'),
    ('$$', '$$'),
    ('$$$','$$$'),
    ('$$$$','$$$$')
)


NUM_CHOICES = (
    ('5','5'),
    ('10', '10'),
    ('25','25'),
    ('50','50'),
    ('All','All')
)

BW_CHOICES = (
    ('Best','Best'),
    ('Worst', 'Worst')
)

class Comment(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=100, choices = CITY_CHOICES, default='Chicago', verbose_name = "Please Choose a City")
    price_limit = models.CharField(max_length=4, choices = PRICE_CHOICES, default='$$$$', verbose_name = "Limit on Price")
    num_limit = models.CharField(max_length=10, choices = NUM_CHOICES, default='5', verbose_name = "Limit on Number of Results")
    best_worst = models.CharField(max_length=10, choices = BW_CHOICES, default='Best', verbose_name= "Specify Best or Worst")
    def __int__(self):   # __unicode__ on Python 2
        return self.auto_increment_id
    def make_dict(self):
        args = {"city": self.city, "price": self.price_limit, "limit": self.num_limit, "worst": self.best_worst}
        return args