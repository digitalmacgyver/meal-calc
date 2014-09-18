# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('meal_planner', '0003_auto_20140917_0142'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItemLanguaLDesc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('langual_id', models.CharField(help_text=b'The LanguaL food description thesaurus ID.', max_length=5, verbose_name=b'LanguaL Food Thesaurus ID')),
                ('langual_desc', models.CharField(help_text=b'The description of this food item from the LanguaL food description thesaurus.', max_length=140, verbose_name=b'LanguaL Description')),
                ('food_item_id', models.ForeignKey(verbose_name=b'FoodItem ID', to='meal_planner.FoodItems', help_text=b'The database ID of the food item this LanguaL description pertains to.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='fooditems',
            name='langual_desc',
        ),
        migrations.RemoveField(
            model_name='fooditems',
            name='langual_id',
        ),
        migrations.AlterField(
            model_name='fooditemnutrients',
            name='updated_date',
            field=models.DateField(default=datetime.datetime(2014, 9, 17, 2, 39, 52, 563440), help_text=b'When this value was added or last modified.', null=True, verbose_name=b'Updated Date', blank=True),
        ),
    ]
