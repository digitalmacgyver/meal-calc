#!/usr/bin/env python

import django
django.setup()
from meal_planner.models import *


Footnotes.objects.all().delete()

# Work around idiotic ORM memory usage.
count = 0
for thing in FoodItemNutrients.objects.iterator():
    thing.delete()
    count += 1
    if ( count % 1000 ) == 0:
        print "."

NutrientSources.objects.all().delete()
NutrientDerivations.objects.all().delete()
NutrientCitations.objects.all().delete()

FoodItemServingSizes.objects.all().delete()

FoodItems.objects.all().delete()
