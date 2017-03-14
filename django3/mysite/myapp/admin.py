from django.contrib import admin
from .models import Question, Choice, Comment, Compare

#these are for practice and testing purposes, created by following the Django tutorial
admin.site.register(Question)
admin.site.register(Choice)

# Registered model for this site
admin.site.register(Comment)
admin.site.register(Compare)

