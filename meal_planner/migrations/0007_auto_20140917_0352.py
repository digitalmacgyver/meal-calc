# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal_planner', '0006_auto_20140917_0325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footnotes',
            name='food_item_id',
            field=models.ForeignKey(default=None, to='meal_planner.FoodItems', blank=True, help_text=b'The database ID of the food item this footnote pertains to.', null=True, verbose_name=b'FoodItem ID'),
        ),
    ]
