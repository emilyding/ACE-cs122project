'''
This admin file registers models into the admin site.
Admin credentials are:
	username: ACE
	pwd: cs122
'''

from django.contrib import admin
# This is imported for testing purposes
from .models import Question, Choice

#This imports models written for the website
from .models import Comment, Compare, Cuisine

#these are for practice and testing purposes, created by instructions from the Django tutorial
admin.site.register(Question)
admin.site.register(Choice)

# Registered model for this site
admin.site.register(Comment)
admin.site.register(Compare)
admin.site.register(Cuisine)
