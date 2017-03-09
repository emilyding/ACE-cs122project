# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20170309_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='Limit on Number of Results',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='Limit on Price',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='Please Choose a City',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='Specify Best or Worst',
        ),
        migrations.AddField(
            model_name='comment',
            name='best_worst',
            field=models.CharField(choices=[('Best', 'Best'), ('Worst', 'Worst')], default='Best', max_length=10, verbose_name='Specify Best or Worst'),
        ),
        migrations.AddField(
            model_name='comment',
            name='city',
            field=models.CharField(choices=[('Albuquerque', 'Albuquerque'), ('Arlington', 'Arlington'), ('Atlanta', 'Atlanta'), ('Austin', 'Austin'), ('Baltimore', 'Baltimore'), ('Boston', 'Boston'), ('Buffalo', 'Buffalo'), ('Charlotte', 'Charlotte'), ('Chicago', 'Chicago'), ('Cleveland', 'Cleveland'), ('Colorado Springs', 'Colorado Springs'), ('Columbus', 'Columbus'), ('Dallas', 'Dallas'), ('Denver', 'Denver'), ('Detroit', 'Detroit'), ('El Paso', 'El Paso'), ('Fort Worth', 'Fort Worth'), ('Fresno', 'Fresno'), ('Honolulu', 'Honolulu'), ('Houston', 'Houston'), ('Indianapolis', 'Indianapolis'), ('Jacksonville', 'Jacksonville'), ('Kansas City', 'Kansas City'), ('Las Vegas', 'Las Vegas'), ('Long Beach', 'Long Beach'), ('Los Angeles', 'Los Angeles'), ('Louisville', 'Louisville'), ('Memphis', 'Memphis'), ('Mesa', 'Mesa'), ('Miami', 'Miami'), ('Milwaukee', 'Milwaukee'), ('Minneapolis', 'Minneapolis'), ('NashvilleNew Orleans', 'NashvilleNew Orleans'), ('New York', 'New York'), ('Oakland', 'Oakland'), ('Oklahoma CityOmaha', 'Oklahoma CityOmaha'), ('Philadelphia', 'Philadelphia'), ('Phoenix', 'Phoenix'), ('Pittsburgh', 'Pittsburgh'), ('Portland', 'Portland'), ('Raleigh', 'Raleigh'), ('Sacramento', 'Sacramento'), ('San Antonio', 'San Antonio'), ('San Diego', 'San Diego'), ('San Francisco', 'San Francisco'), ('San JoseSeattleSt Louis', 'San JoseSeattleSt Louis'), ('St Paul', 'St Paul'), ('Tampa', 'Tampa'), ('Tucson', 'Tucson'), ('Tulsa', 'Tulsa'), ('Virginia Beach', 'Virginia Beach'), ('Washington DC', 'Washington DC')], default='Chicago', max_length=100, verbose_name='Please Choose a City'),
        ),
        migrations.AddField(
            model_name='comment',
            name='num_limit',
            field=models.CharField(choices=[('5', '5'), ('10', '10'), ('25', '25'), ('50', '50'), ('All', 'All')], default='5', max_length=10, verbose_name='Limit on Number of Results'),
        ),
        migrations.AddField(
            model_name='comment',
            name='price_limit',
            field=models.CharField(choices=[('$', '$'), ('$$', '$$'), ('$$$', '$$$'), ('$$$$', '$$$$')], default='$$$$', max_length=4, verbose_name='Limit on Price'),
        ),
    ]
