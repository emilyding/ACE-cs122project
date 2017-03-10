from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from myapp.models import Comment
 
class MyCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['city', 'price_limit', 'num_limit', 'best_worst']
