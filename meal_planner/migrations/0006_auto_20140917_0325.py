# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal_planner', '0005_auto_20140917_0324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditemnutrients',
            name='updated_date',
            field=models.DateField(help_text=b'When this value was added or last modified.', null=True, verbose_name=b'Updated Date', blank=True),
        ),
    ]
