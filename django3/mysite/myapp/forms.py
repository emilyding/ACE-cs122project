'''
This file writes classes to create forms. Forms use django's ModelForm capacity. This is original code; however, credit must be attributed to the following sites which were used as resources:
	-http://www.effectivedjango.com/tutorial/forms.html
	-http://blog.appliedinformaticsinc.com/using-django-modelform-a-quick-guide/
	-https://www.pydanny.com/core-concepts-django-modelforms.html
'''

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from myapp.models import Comment, Compare, Cuisine

 
class MyCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['city', 'price_limit', 'best_worst']

class MyCompareForm(ModelForm):
    class Meta:
        model = Compare
        fields = ['city1', 'city2', 'cuisine']

class MyCuisineForm(ModelForm):
    class Meta:
        model = Cuisine
        fields = ['cuisine']



