from django.contrib import admin

from meal_planner.models import *

model_classes = [ FoodItems, NutrientSources, NutrientDerivations, FoodItemNutrients ]

for mc in model_classes:
    admin.site.register( mc )
