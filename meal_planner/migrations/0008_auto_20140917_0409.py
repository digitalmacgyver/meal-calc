# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal_planner', '0007_auto_20140917_0352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditems',
            name='refuse_desc',
            field=models.CharField(default=None, max_length=135, blank=True, help_text=b'Description of inedible parts of food item, such as seeds or bone.', null=True, verbose_name=b'Description of Inedible Parts'),
        ),
    ]
