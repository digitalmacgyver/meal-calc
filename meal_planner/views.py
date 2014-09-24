from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse

import scipy.optimize

from meal_planner.models import *

# Create your views here.

def index( request ):
    food_items = FoodItems.objects.all()

    context = { 'food_items' : food_items,
                'boilerplate' : scipy.optimize.minimize.func_doc }
    return render( request, 'meal_planner/index.html', context )

def food_item( request, food_item_id ):
    food_item = FoodItems.objects.get( pk=food_item_id )
    nutrients = FoodItemNutrients.objects.filter( food_item_id__pk=food_item.pk )

    context = { 'food_item' : food_item,
                'food_item_fields' :  serializers.serialize( "python", [ food_item ] ),
                'nutrients' : nutrients }
    return render( request, 'meal_planner/fi.html', context )


def nutrient( request, food_item_nutrient_id ):
    nutrient = FoodItemNutrients.objects.get( pk=food_item_nutrient_id )

    context = { 'nutrient_desc' : unicode( nutrient ),
                'food_item_id' : nutrient.food_item_id.pk,
                'nutrient' : serializers.serialize( "python", [ nutrient ] ) }
    return render( request, 'meal_planner/fin.html', context )


