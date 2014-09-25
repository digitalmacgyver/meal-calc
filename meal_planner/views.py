from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse

import scipy.optimize

from meal_planner.models import *
from meal_planner.forms import *

import lib.NutritionCalc as nc

# Create your views here.

def index( request ):
    food_items = FoodItems.objects.all()

    context = { 'food_items' : food_items }
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

food_groups = {
    'carbs' : {
        '2000' : 'Cereal Grains and Pasta',
        '1800' : 'Baked Products'
    },
    'fats' : {
        '0100' : 'Dairy and Egg Products',
        '0400' : 'Fats and Oils'
    },
    'proteins' : {
        '0500' : 'Poultry Products',
        '1600' : 'Legumes and Legume Products',
        '1500' : 'Finfish and Shellfish Products',
        '1300' : 'Beef Products',
        '1700' : 'Lamb, Veal, and Game Products',
        '1000' : 'Pork Products',
        '0700' : 'Sausages and Luncheon Meats'
    },
    'vegetables' : {
        '1100' : 'Vegetables and Vegetable Products'
    },
    'fruits_and_nuts' : {
        '1200' : 'Nut and Seed Products',
        '0900' : 'Fruits and Fruit Juices'
    },
    'beverages' : { 
        '1400' : 'Beverages'
    }
}

food_group_ordering = [ 'vegetables', 'proteins', 'carbs', 'fruits_and_nuts', 'fats', 'beverages' ]

energy = 1359.42

nutrient_goals = [
    ('Calcium, Ca', .8),
    ('Carbohydrate, by difference', 130),
    ('Choline, total', .25),
    ('Copper, Cu', .44 / 1000),
    ('Energy', energy),
    ('Fiber, total dietary', 19.03188),
    ('Fluoride, F', 1000.0 / ( 1000*1000 )),
    ('Folate, total', 200.0 / ( 1000*1000 )),
    ('Histidine', .408),
    ('Iron, Fe', 10.0 / 1000),
    ('Isoleucine', .561),
    ('Leucine', 1.2495),
    ('Lutein + zeaxanthin', 6000.0 / ( 1000*1000 )),
    ('Lysine', 1.173),
    ('Magnesium, Mg', 130.0 / 1000),
    ('Manganese, Mn', 1.5 / 1000),
    ('Niacin', 8.0 / 1000),
    ('Pantothenic acid', 3.0 / 1000),
    ('Phosphorus, P', .5),
    ('Potassium, K', 3.8),
    ('Protein', 20.4),
    ('Riboflavin', 0.6 / 1000),
    ('Selenium, Se', 30.0 / ( 1000*1000 )),
    ('Sodium, Na', 1.2),
    ('Thiamin', 0.6 / 1000),
    ('Threonine', .612),
    ('Tryptophan', .153),
    ('Valine', .714),
    ('Vitamin A, RAE', 400.0 / ( 1000*1000 )),
    ('Vitamin B-12', 1.2 / ( 1000*1000 )),
    ('Vitamin B-6', 0.6 / 1000),
    ('Vitamin C, total ascorbic acid', 25.0 / 1000),
    ('Vitamin D (D2 + D3)', 5.0 / ( 1000*1000 )),
    ('Vitamin E (alpha-tocopherol)', 7.0 / 1000),
    ('Vitamin K (phylloquinone)', 55.0 / ( 1000*1000 )),
    ('Water', 1700),
    ('Zinc, Zn', 5.0 / 1000),
    ('Fat - Unsaturated' , 10.9),
    ('Methionine and Cystine' , 0.561),
    ('Phenylalanine and Tyrosine' , 1.0455 )
]

nutrient_goal_hash = {}
for goal in nutrient_goals:
    nutrient_goal_hash[goal[0]] = goal[1]

def planner( request ):
    current_meal = None

    FIs = nc.FoodItems()
    food_items = FIs.get_food_items()
            
    pfill = None
    cfill = None
    ffill = None
    
    for fi in food_items:
        if fi.name == 'protein filler':
            pfill = fi
        elif fi.name == 'carbs filler':
            cfill = fi
        elif fi.name == 'fat filler':
            ffill = fi

    if request.method == 'POST':
        
        #import pdb
        #pdb.set_trace()

        #pcalories = request.POST.get( 'calories', None )
        #pfood_group = None
        #pfood_choices = 
        #for food_group_element in food_group_ordering:
        #    if food_group_element in request.POST:
        #        pfood_group = food_group_element
                
        #pselected_food_items = {}
        #for key, value in request.POST.items():
        #    if key[:10] == 'food_item_':
        #        pselected_food_items[key[10:]] = value

        form = MealForm( request.POST )
        #calories = pcalories, 
        #                 food_group = pfood_group, 
        #                 selected_food_items=pselected_food_items )

        if form.is_valid():
            food_group = None
            selected_food_group = form.data['food_group']

            for idx, food_group_element in enumerate( food_group_ordering ):
                if food_group_element == selected_food_group:
                    if idx + 1 < len( food_group_ordering ):
                        food_group = food_group_ordering[ idx + 1 ]
                    else:
                        food_group = 'done'

            # Now food_group is either our last item or the next one
            # we want to process.
            if food_group == 'done':
                initial_meal = nc.Meal( 'Current Meal',
                                        nutrient_equality_constraints = [ ( 'Energy', energy ) ],
                                        nutrient_limit_constraints = [ ( 'Protein', energy*.3*.8/4, energy*.3*1.2/4 ),
                                                                       ( 'Carbohydrate, by difference',   energy*.4*.8/4, energy*.4*1.2/4 ),
                                                                       ( 'Total lipid (fat)',     energy*.3*.8/9, energy*.3*1.2/9 ) ],
                                        nutrient_goals = nutrient_goals )

                selected_foods = { form.data['food_choices'] : 'selected_foods_%s' % ( form.data['food_choices'] ) }
                for food_item_label in [ x for x in form.data.keys() if x.startswith( 'selected_foods_' ) ]:
                    selected_foods[food_item_label[15:]] = form.data[food_item_label]
                    initial_meal.add_food_item( food_item_label[15:], 0 )

                result = nc.meal_planner( initial_meal, [ FIs.get_food_item( form.data['food_choices'] ) ], [ pfill, cfill, ffill ] )

                if len( result ):
                    current_score, current_ingredient, current_meal = result[0]

                form = None
            else:
                initial_meal = nc.Meal( 'Current Meal',
                                        nutrient_equality_constraints = [ ( 'Energy', energy ) ],
                                        nutrient_limit_constraints = [ ( 'Protein', energy*.3*.8/4, energy*.3*1.2/4 ),
                                                                       ( 'Carbohydrate, by difference',   energy*.4*.8/4, energy*.4*1.2/4 ),
                                                                       ( 'Total lipid (fat)',     energy*.3*.8/9, energy*.3*1.2/9 ) ],
                                        nutrient_goals = nutrient_goals )
                


                # DEBUG - We're only getting one ingredient at a time.
                selected_foods = { form.data['food_choices'] : 'selected_foods_%s' % ( form.data['food_choices'] ) }
                for food_item_label in [ x for x in form.data.keys() if x.startswith( 'selected_foods_' ) ]:
                    selected_foods[food_item_label[15:]] = form.data[food_item_label]
                    initial_meal.add_food_item( food_item_label[15:], 0 )
                    
                #import pdb
                #pdb.set_trace()
                result = nc.meal_planner( initial_meal, [ FIs.get_food_item( form.data['food_choices'] ) ], [ pfill, cfill, ffill ] )

                if len( result ):
                    current_score, current_ingredient, current_meal = result[0]

                new_ingredients = []

                # DEBUG
                db_food_items = FoodItems.objects.filter( food_group_id__in = food_groups[food_group].keys() )[:21]
                
                for db_food_item in db_food_items:
                    new_ingredients.append( FIs.get_food_item( db_food_item.uid ) )

                candidate_meals = nc.meal_planner( current_meal, new_ingredients, [ pfill, cfill, ffill ] )
                                   
                food_choices = [ ( x[1].uid, x[1].name ) for x in candidate_meals[:20] ]

                form = MealForm( 
                    calories = 1230,
                    selected_foods = selected_foods,
                    food_group = food_group,
                    food_choices = food_choices )
            
    else:

        empty_meal = nc.Meal( 'Current Meal',
                              nutrient_equality_constraints = [ ( 'Energy', energy ) ],
                              nutrient_limit_constraints = [ ( 'Protein', energy*.3*.8/4, energy*.3*1.2/4 ),
                                                             ( 'Carbohydrate, by difference',   energy*.4*.8/4, energy*.4*1.2/4 ),
                                                             ( 'Total lipid (fat)',     energy*.3*.8/9, energy*.3*1.2/9 ) ],
                              nutrient_goals = nutrient_goals )
        
        current_meal = empty_meal

        food_group = food_group_ordering[0]

        # DEBUG
        db_food_items = FoodItems.objects.filter( food_group_id__in = food_groups[food_group].keys() )[:21]

        new_ingredients = []
        for db_food_item in db_food_items:
            new_ingredients.append( FIs.get_food_item( db_food_item.uid ) )

        candidate_meals = nc.meal_planner( empty_meal, new_ingredients, [ pfill, cfill, ffill ] )

        food_choices = [ ( x[1].uid, x[1].name ) for x in candidate_meals[:20] ]

        form = MealForm( food_group = food_group,
                         food_choices = food_choices )

        
    current_meal_nutrients = {}
    if current_meal is not None:
        for nutrient, amount in current_meal.get_nutrients().items():
            goal_amount = -1.0
            if nutrient in nutrient_goal_hash:
                goal_amount = nutrient_goal_hash[nutrient]
            current_meal_nutrients[nutrient] = "%0.02f%% of DRI - %f grams" % ( 100.0 * amount / goal_amount,  amount )
    return render( request, 'meal_planner/planner.html', { 
        'form' : form, 
        'current_meal' : current_meal.get_food_items(),
        'current_meal_nutrients' : current_meal_nutrients,
        'food_group' : food_group
    } )
