# This file allows functionality from google charts and writes stepchart class. Code was taken from https://www.pydanny.com/core-concepts-django-modelforms.html and is not original and has not been altered.

from django_google_charts import charts
from .models import StepCount

class StepChart(charts.Chart):
    chart_slug = 'steps_chart'
    columns = (
        ('datetime', "Date"),
        ('number', "Steps"),
    )

    def get_data(self):
        return StepCount.objects.values_list('date', 'count')
