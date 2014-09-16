# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal_planner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditems',
            name='carb_factor',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=6, blank=True, help_text=b'Factor for calculating calories from carbohydrate.', null=True, verbose_name=b'Carbohydrate Factor'),
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='common_name',
            field=models.CharField(default=None, max_length=100, blank=True, help_text=b'Common name', null=True, verbose_name=b'Common Name'),
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='fat_factor',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=6, blank=True, help_text=b'Factor for calculating calories from fat.', null=True, verbose_name=b'Fat Factor'),
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='langual_desc',
            field=models.CharField(default=None, max_length=140, blank=True, help_text=b'The description of this food item from the LanguaL food description thesaurus.', null=True, verbose_name=b'LanguaL Description'),
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='langual_id',
            field=models.CharField(default=None, max_length=5, blank=True, help_text=b'The LanguaL food description thesaurus ID.', null=True, verbose_name=b'LanguaL Food Thesaurus ID'),
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='manufacturer',
            field=models.CharField(default=None, max_length=65, blank=True, help_text=b'The manufacturer of this food item.', null=True, verbose_name=b'Manufacturer'),
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='nitrogen_factor',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=6, blank=True, help_text=b'Factor for converting nitrogen to protein', null=True, verbose_name=b'Nitrogen Factor'),
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='protein_factor',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=6, blank=True, help_text=b'Factor for calculating calories from protein.', null=True, verbose_name=b'Protein Factor'),
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='refuse_desc',
            field=models.CharField(default=None, max_length=125, blank=True, help_text=b'Description of inedible parts of food item, such as seeds or bone.', null=True, verbose_name=b'Description of Inedible Parts'),
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='refuse_pct',
            field=models.DecimalField(decimal_places=0, default=None, max_digits=2, blank=True, help_text=b'Percentage of inedible parts of food item.', null=True, verbose_name=b'Percentage of Inedible Parts'),
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='scientific_name',
            field=models.CharField(default=None, max_length=65, blank=True, help_text=b'Scientific name - given for least processed form of the food item.', null=True, verbose_name=b'Scientific Name'),
        ),
    ]
