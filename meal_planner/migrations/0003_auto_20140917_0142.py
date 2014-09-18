# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('meal_planner', '0002_auto_20140916_0205'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItemNutrients',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nutrient_id', models.CharField(help_text=b'Unique 3-digit identifier for a nutrient.', max_length=3, verbose_name=b'Nutrient ID')),
                ('unit', models.CharField(help_text=b'Nutrient unit (e.g. kcal, IU, g).', max_length=7, verbose_name=b'Unit')),
                ('infoods_tag', models.CharField(default=None, max_length=20, blank=True, help_text=b'International Network of Food Data Systems (INFOODS) Tagname.', null=True, verbose_name=b'INFOODS Tagname')),
                ('nutrient', models.CharField(help_text=b'Name of the nutrient/food component.', max_length=60, verbose_name=b'Nutrient')),
                ('sort_order', models.IntegerField(help_text=b'The order to display this nutrient in to be consistent with various USDA reports.', verbose_name=b'Sort Order')),
                ('amount', models.DecimalField(help_text=b'Amount of nutrient in 1 edible gram of a food item.', verbose_name=b'Amount of Nutrient in 1 g of Food Item', max_digits=18, decimal_places=11)),
                ('data_points', models.PositiveIntegerField(help_text=b'Number of analyses used to calculate nutrient value.  If zero, then the value was calculated or imputed.', verbose_name=b'Number of Data Points')),
                ('std_err', models.DecimalField(decimal_places=3, default=None, max_digits=8, blank=True, help_text=b'Standard error, null if the error can not be calculated or if fewer than three data points.', null=True, verbose_name=b'Standard Error')),
                ('is_fortified', models.BooleanField(default=False, help_text=b'Indicates that this nutrient was added for fortification or enrichment.', verbose_name=b'Is Fortified')),
                ('studies', models.PositiveIntegerField(default=None, help_text=b'Number of studies.', null=True, verbose_name=b'Number of Studies', blank=True)),
                ('min_value', models.DecimalField(decimal_places=3, default=None, max_digits=10, blank=True, help_text=b'Minimum value.', null=True, verbose_name=b'Minimum Value')),
                ('max_value', models.DecimalField(decimal_places=3, default=None, max_digits=10, blank=True, help_text=b'Maximum value.', null=True, verbose_name=b'Maximum Value')),
                ('freedom_degrees', models.PositiveIntegerField(default=None, help_text=b'Degrees of freedom.', null=True, verbose_name=b'Degrees of Freedom', blank=True)),
                ('lower_error_bound', models.DecimalField(decimal_places=3, default=None, max_digits=10, blank=True, help_text=b'Lower 95% error bound.', null=True, verbose_name=b'Lower Error Bound')),
                ('upper_error_bound', models.DecimalField(decimal_places=3, default=None, max_digits=10, blank=True, help_text=b'Upper 95% error bound.', null=True, verbose_name=b'Upper Error Bound')),
                ('stat_comments', models.CharField(default=None, max_length=10, blank=True, help_text=b'Statistical comments.', null=True, verbose_name=b'Statistical Comments')),
                ('updated_date', models.DateField(default=datetime.datetime(2014, 9, 17, 1, 42, 48, 676205), help_text=b'When this value was added or last modified.', null=True, verbose_name=b'Updated Date', blank=True)),
                ('food_item_id', models.ForeignKey(verbose_name=b'FoodItem ID', to='meal_planner.FoodItems', help_text=b'The database ID of the food item this nutrient is associated with.')),
            ],
            options={
                'ordering': ['sort_order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FoodItemServingSizes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.DecimalField(help_text=b'The number of units (e.g. 1 in 1 cup).', verbose_name=b'Quantity', max_digits=5, decimal_places=3)),
                ('unit', models.CharField(help_text=b'The unit to which quantity pertains (e.g. cup in 1 cup).', max_length=84, verbose_name=b'Unit')),
                ('grams', models.DecimalField(help_text=b'Weight in grams.', verbose_name=b'Grams', max_digits=7, decimal_places=1)),
                ('data_points', models.PositiveIntegerField(default=None, help_text=b'Number of data points.', null=True, verbose_name=b'Number of Data Points', blank=True)),
                ('std_dev', models.DecimalField(decimal_places=3, default=None, max_digits=7, blank=True, help_text=b'Standard deviation in the data points.', null=True, verbose_name=b'Standard Deviation')),
                ('food_item_id', models.ForeignKey(verbose_name=b'FoodItem ID', to='meal_planner.FoodItems', help_text=b'The database ID of the food item this serving size pertains to.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Footnotes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('footnote_number', models.PositiveIntegerField(help_text=b'The number associated with this footnote.', verbose_name=b'Footnote Number')),
                ('footnote_type', models.CharField(help_text=b'Footnote type: D - food description, M - measure description, N - nutrient value.', max_length=1, verbose_name=b'Footnote Type', choices=[(b'D', b'Description'), (b'M', b'Measure'), (b'N', b'Nutrient')])),
                ('footnote', models.CharField(help_text=b'Footnote.', max_length=200, verbose_name=b'Footnote')),
                ('food_item_id', models.ForeignKey(verbose_name=b'FoodItem ID', to='meal_planner.FoodItems', help_text=b'The database ID of the food item this footnote pertains to.')),
                ('food_item_nutrient_id', models.ForeignKey(default=None, to='meal_planner.FoodItemNutrients', blank=True, help_text=b'The database ID of the food item nutrient this footnote pertains to.', null=True, verbose_name=b'FoodItemNutrient ID')),
            ],
            options={
                'ordering': ['footnote_number'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NutrientCitations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('authors', models.CharField(default=None, max_length=255, blank=True, help_text=b'Authors.', null=True, verbose_name=b'Authors')),
                ('title', models.CharField(help_text=b'Title.', max_length=255, verbose_name=b'Title')),
                ('year', models.CharField(default=None, max_length=4, blank=True, help_text=b'Year.', null=True, verbose_name=b'Year')),
                ('journal', models.CharField(default=None, max_length=135, blank=True, help_text=b'Journal.', null=True, verbose_name=b'Journal')),
                ('volume', models.CharField(default=None, max_length=16, blank=True, help_text=b'Volume number of journals, city for events.', null=True, verbose_name=b'Volume or City')),
                ('issue', models.CharField(default=None, max_length=5, blank=True, help_text=b'Issue number for journals, State for events.', null=True, verbose_name=b'Issue or State')),
                ('start_page', models.PositiveIntegerField(default=None, help_text=b'Start page of article.', null=True, verbose_name=b'Start Page', blank=True)),
                ('end_page', models.PositiveIntegerField(default=None, help_text=b'End page of article.', null=True, verbose_name=b'End Page', blank=True)),
                ('food_item_nutrient_id', models.ForeignKey(verbose_name=b'FoodItemNutrient ID', to='meal_planner.FoodItemNutrients', help_text=b'The database ID of the food item nutrient this footnote pertains to.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NutrientDerivations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('derivation_id', models.CharField(help_text=b'The data derivation ID from the USDA NNDS SR 27.', max_length=4, verbose_name=b'Nutrient Derivation ID')),
                ('derivation_desc', models.CharField(help_text=b'How were the values in the nutrient determined.', max_length=120, verbose_name=b'Source Description')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NutrientSources',
            fields=[
                ('nutrient_source_id', models.PositiveIntegerField(help_text=b'The nutrient source ID from the USDA NNDS SR 27.', serialize=False, verbose_name=b'Nutrient Source ID', primary_key=True)),
                ('source_desc', models.CharField(help_text=b'Nutrient source description from the USDA NNDS SR 27.', max_length=60, verbose_name=b'Source Description')),
            ],
            options={
                'ordering': ['nutrient_source_id'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fooditemnutrients',
            name='nutrient_derivation_id',
            field=models.ForeignKey(default=None, to='meal_planner.NutrientDerivations', blank=True, help_text=b'The database ID of how this nutrient data was derived.', null=True, verbose_name=b'Nutrient Derivation ID'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fooditemnutrients',
            name='nutrient_source_id',
            field=models.ForeignKey(verbose_name=b'Nutrient Source ID', to='meal_planner.NutrientSources', help_text=b'The database ID of the nutrient source for this FoodItem Nutrient.'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='fooditemnutrients',
            unique_together=set([('food_item_id', 'nutrient_id')]),
        ),
        migrations.AlterModelOptions(
            name='fooditems',
            options={'ordering': ['ndb_id']},
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='carb_factor',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=4, blank=True, help_text=b'Factor for calculating calories from carbohydrate.', null=True, verbose_name=b'Carbohydrate Factor'),
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='fat_factor',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=4, blank=True, help_text=b'Factor for calculating calories from fat.', null=True, verbose_name=b'Fat Factor'),
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='nitrogen_factor',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=4, blank=True, help_text=b'Factor for converting nitrogen to protein', null=True, verbose_name=b'Nitrogen Factor'),
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='protein_factor',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=4, blank=True, help_text=b'Factor for calculating calories from protein.', null=True, verbose_name=b'Protein Factor'),
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='uid',
            field=models.CharField(help_text=b'Food Item UUID', unique=True, max_length=36, verbose_name=b'Food Item UUID'),
        ),
    ]
