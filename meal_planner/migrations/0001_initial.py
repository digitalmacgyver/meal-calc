# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(help_text=b'Food Item UUID', max_length=36, verbose_name=b'Food Item UUID')),
                ('ndb_id', models.CharField(help_text=b'The 5-digit Nutrient Databank identifier of this food item.', unique=True, max_length=5, verbose_name=b'Nutrient Database ID')),
                ('food_group_id', models.CharField(help_text=b'The 4-digit food group code - currently only the first two digits are used.', max_length=4, verbose_name=b'Food Group Code')),
                ('food_group_desc', models.CharField(help_text=b'Food Group Description', max_length=60, verbose_name=b'Food Group Description')),
                ('long_desc', models.CharField(help_text=b'200-character description of food item.', max_length=200, verbose_name=b'Long Description')),
                ('short_desc', models.CharField(help_text=b'60-character description of food item.', max_length=60, verbose_name=b'Short Description')),
                ('common_name', models.CharField(help_text=b'Common name', max_length=100, null=True, verbose_name=b'Common Name', blank=True)),
                ('manufacturer', models.CharField(help_text=b'The manufacturer of this food item.', max_length=65, null=True, verbose_name=b'Manufacturer', blank=True)),
                ('is_fndds', models.BooleanField(default=False, help_text=b'Whether this food item is in the USDA Food and Nutrient Database for Dietary Studies (FNDDS)', verbose_name=b'Is In USDA FNDDS Database')),
                ('refuse_desc', models.CharField(help_text=b'Description of inedible parts of food item, such as seeds or bone.', max_length=125, null=True, verbose_name=b'Description of Inedible Parts', blank=True)),
                ('refuse_pct', models.DecimalField(decimal_places=0, max_digits=2, blank=True, help_text=b'Percentage of inedible parts of food item.', null=True, verbose_name=b'Percentage of Inedible Parts')),
                ('scientific_name', models.CharField(help_text=b'Scientific name - given for least processed form of the food item.', max_length=65, null=True, verbose_name=b'Scientific Name', blank=True)),
                ('nitrogen_factor', models.DecimalField(decimal_places=2, max_digits=6, blank=True, help_text=b'Factor for converting nitrogen to protein', null=True, verbose_name=b'Nitrogen Factor')),
                ('protein_factor', models.DecimalField(decimal_places=2, max_digits=6, blank=True, help_text=b'Factor for calculating calories from protein.', null=True, verbose_name=b'Protein Factor')),
                ('fat_factor', models.DecimalField(decimal_places=2, max_digits=6, blank=True, help_text=b'Factor for calculating calories from fat.', null=True, verbose_name=b'Fat Factor')),
                ('carb_factor', models.DecimalField(decimal_places=2, max_digits=6, blank=True, help_text=b'Factor for calculating calories from carbohydrate.', null=True, verbose_name=b'Carbohydrate Factor')),
                ('langual_id', models.CharField(help_text=b'The LanguaL food description thesaurus ID.', max_length=5, null=True, verbose_name=b'LanguaL Food Thesaurus ID', blank=True)),
                ('langual_desc', models.CharField(help_text=b'The description of this food item from the LanguaL food description thesaurus.', max_length=140, null=True, verbose_name=b'LanguaL Description', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
