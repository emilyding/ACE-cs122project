# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-10 04:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20170309_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='city',
            field=models.CharField(choices=[('Albuquerque', 'Albuquerque'), ('Arlington', 'Arlington'), ('Atlanta', 'Atlanta'), ('Austin', 'Austin'), ('Baltimore', 'Baltimore'), ('Boston', 'Boston'), ('Buffalo', 'Buffalo'), ('Charlotte', 'Charlotte'), ('Chicago', 'Chicago'), ('Cleveland', 'Cleveland'), ('Colorado Springs', 'Colorado Springs'), ('Columbus', 'Columbus'), ('Dallas', 'Dallas'), ('Denver', 'Denver'), ('Detroit', 'Detroit'), ('El Paso', 'El Paso'), ('Fort Worth', 'Fort Worth'), ('Fresno', 'Fresno'), ('Honolulu', 'Honolulu'), ('Houston', 'Houston'), ('Indianapolis', 'Indianapolis'), ('Jacksonville', 'Jacksonville'), ('Kansas City', 'Kansas City'), ('Las Vegas', 'Las Vegas'), ('Long Beach', 'Long Beach'), ('Los Angeles', 'Los Angeles'), ('Louisville', 'Louisville'), ('Memphis', 'Memphis'), ('Mesa', 'Mesa'), ('Miami', 'Miami'), ('Milwaukee', 'Milwaukee'), ('Minneapolis', 'Minneapolis'), ('Nashville', 'Nashville'), ('New Orleans', 'New Orleans'), ('New York', 'New York'), ('Oakland', 'Oakland'), ('Oklahoma City', 'Oklahoma City'), ('Omaha', 'Omaha'), ('Philadelphia', 'Philadelphia'), ('Phoenix', 'Phoenix'), ('Pittsburgh', 'Pittsburgh'), ('Portland', 'Portland'), ('Raleigh', 'Raleigh'), ('Sacramento', 'Sacramento'), ('San Antonio', 'San Antonio'), ('San Diego', 'San Diego'), ('San Francisco', 'San Francisco'), ('San Jose', 'San Jose'), ('Seattle', 'Seattle'), ('St Louis', 'St Louis'), ('St Paul', 'St Paul'), ('Tampa', 'Tampa'), ('Tucson', 'Tucson'), ('Tulsa', 'Tulsa'), ('Virginia Beach', 'Virginia Beach'), ('Washington DC', 'Washington DC')], default='Chicago', max_length=100, verbose_name='Please Choose a City'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='num_limit',
            field=models.CharField(choices=[('5', '5'), ('10', '10'), ('25', '25'), ('50', '50'), ('All', 'All')], default='5', max_length=10, verbose_name='Max Number of Results'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='price_limit',
            field=models.CharField(choices=[('$', '$'), ('$$', '$$'), ('$$$', '$$$'), ('$$$$', '$$$$')], default='$$$$', max_length=4, verbose_name='Max Price'),
        ),
    ]