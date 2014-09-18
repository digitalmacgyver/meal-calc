# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('meal_planner', '0004_auto_20140917_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditemnutrients',
            name='unit',
            field=models.CharField(help_text=b'Nutrient unit (e.g. kcal, IU, g).', max_length=7, verbose_name=b'Unit', choices=[(b'g', b'Grams'), (b'mg', b'Milligrams'), (b'ug', b'Micrograms'), (b'IU', b'International unit'), (b'kcal', b'Kilocalorie')]),
        ),
        migrations.AlterField(
            model_name='fooditemnutrients',
            name='updated_date',
            field=models.DateField(default=datetime.datetime(2014, 9, 17, 3, 24, 28, 550650), help_text=b'When this value was added or last modified.', null=True, verbose_name=b'Updated Date', blank=True),
        ),
    ]
