from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from myapp.models import Comment
from myapp.models import Compare
 
class MyCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['city', 'price_limit', 'num_limit', 'best_worst']

class MyCompareForm(ModelForm):
    class Meta:
        model = Compare
        fields = ['city1', 'city2', 'cuisine']


#http://www.effectivedjango.com/tutorial/forms.html
#http://blog.appliedinformaticsinc.com/using-django-modelform-a-quick-guide/
#https://www.pydanny.com/core-concepts-django-modelforms.html
