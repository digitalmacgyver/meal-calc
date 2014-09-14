#!/usr/bin/env python

import pprint

import NutritionCalc as nc

pp = pprint.PrettyPrinter( indent = 4 )

# An empty meal with some constraints and goals.
initial_meal = nc.Meal(
    name = 'Test Meal',
    nutrient_equality_constraints = [ ( 'kcal',  1000 ) ],
    nutrient_limit_constraints = [ ( 'protein', 1000*.3*.8, 1000*.3*1.2 ),
                                   ( 'carbs',   1000*.4*.8, 1000*.4*1.2 ),
                                   ( 'fat',     1000*.3*.8, 1000*.3*1.2 ) ],
    nutrient_goals = [ ( 'vitamin C', 0.075 ),
                       ( 'calcium', 0.8 ) ]
    )

food_items = nc.FoodItems().get_food_items()

chicken = None
asparagus = None
pfill = None
cfill = None
ffill = None

for fi in food_items:
    if fi.name == 'asparagus':
        asparagus = fi
    elif fi.name == 'chicken':
        chicken = fi
    elif fi.name == 'protein filler':
        pfill = fi
    elif fi.name == 'carbs filler':
        cfill = fi
    elif fi.name == 'fat filler':
        ffill = fi
    else:
        raise Exception( "Unknown food item type: %s" % ( fi) )

potential_meals = nc.meal_planner( initial_meal,
                                   [ asparagus ],
                                   [ pfill, cfill, ffill ] )

for score, added_item, potential_meal in potential_meals:
    print "Adding %s to %s yeilded a score of: %f" % ( added_item.name, potential_meal.name, score )

    print "Food items were:"
    pp.pprint( potential_meal.get_food_items() )
    
    print "Nutrients were:"
    pp.pprint( potential_meal.get_nutrients )
