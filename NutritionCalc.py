#!/usr/bin/env python

from functools import wraps
import scipy.optimize

'''
NOTE: Food items live in a database. There is also a recipes table,
and a recipe_food_items join table with recipe_id, food_item_id, and
amount.

NEXT UP:

1. Implement classes as above.
2. Stub out FoodItems and Nutrients with toy data from other example, verify things are working.
2. Implement Flask/SQLalchemy local schema for Ingredients
3. Populate Ingredients from USDA website.

Great tutorial on Heroku/flask/postgres:
https://realpython.com/blog/python/flask-by-example-part-1-project-setup/

Shorter writeup on flask/sqlalchemy/heroku:
http://blog.y3xz.com/blog/2012/08/16/flask-and-postgresql-on-heroku

Some short notes on environment variables to implement locally.
http://beatofthegeek.com/2013/04/how-to-setup-postgresql-python-flask.html

'''

def meal_planner( meal, fitness_function, food_items, filler_items=[] ):
    '''Inputs:
    * meal - A Meal object
    * fitness_function - A function to be minimized, it takes as input
      a meal and a list of FoodItems and their amounts and returns a
      score, lower numbers are better.
    * food_items - An array of FoodItem objects
    * filler_items - An array of FoodItem objects, ideally with
      nutrients such that they do not contribute anything at all to
      the fitness_function.

    Behavior: Given a current Meal, meal_planner iterates over all
    food_items and attempts to create new Meals.  This is done by
    minimizing the fitness_function over the:
    * The ingredients present in the input Meal
    * The ingredient in question from food_items
    * All ingredients available in filler_items
    
    Outputs: An array of ( new_meal, fitness_value ) tipples.

    For each food_item if it is possible to craft a new Meal
    that has a better (e.g. lower) fitness function value by adding
    that item and optional filler_items to the base Meal, a new (
    meal, fitness_value ) tuple is added to the output.

    '''
    fitness_food_items = [ 'DEBUG - get all food items from meal, append our food item of interest, and all the filler items.' ]

    def meal_fitness_function( food_items_amounts ):
        return fitness_function( meal, fitness_food_items, food_item_amounts )

            
def sum_lesser_squares( meal, food_items, food_item_amounts ):
    '''A fitness function, returns:
    
    sum over all food_items and nutrition goals such that:
       max( 0, ( 1 - % of goal met by food items and food item amounts )^2 )
    '''
    pass
            
class Meal( object ):
    '''A collection of food items and their amounts, as well as a set of
    nutritional constraints and goals.

    Constraints and Goals: 

    A constraint is a requirement of the meal, e.g. kcal=400, or
    fat_grams in ( 0, 30 ).  If the meal_planner can not meet the
    constraints with the food_items and filler_items provided, no meal
    will be generated.

    A goals is a desired feature of the meal, e.g. .300 of Calcium or
    100 grams of french fries.  Goals are interpreted by the
    fitness_function to determine how good this meal is compared to
    other meals.  See fitness function documentation for how
    shortfalls and excesses of goals impact the score of the meal.

    Fields: 
    * name
    * food_items - A dictionary of FoodItem.id's -> amount in grams
    * nutrient_constraints - A list of constraints on nutrients for this meal
    * food_item_constraints - A list of constraints on food items for this meal
    * nutrient_goals - A list of goals for nutrients in this meal
    * food_item_goals - A list of goals for floor items in this meal

    Methods:
    add_nutrient_constraint( nutrient, type, value )
    add_food_item_constraint( food_item_id, type, value )
    type is one of 'eq' or 'limits'
    If type is 'eq' value is a number expressed in units of the Nutrients object.
    If type is 'limits' value is a ( lower_bound, upper_bound ) tuple,
    where a value of None means there is no bound in that direction.

    add_nutrient_goal( nutrient, value )
    add_nutrient_goal( food_item_id, value )

    get_food_items() - Returns an array of ( food_item, amount ) tuples.
    get_nutrients() - Returns a dictionary of nutrient->amount values

    NOTE: Combining food_item and nutrient constraints can cause
    unsolvable states, e.g. if french fries have 8 calories per gram,
    and we insist calories have a limit of 800 and that 110 grams of
    french fries be in the meal, there will be no solution (baring
    negative calorie food items).

    '''

    def __init__( self,
                  name,
                  food_items = [],                     # List of ( food_item_id, amount in grams )
                  nutrient_equality_constraints = [],  # List of ( nutrient_name, value ) 
                  nutrient_limit_constraints = []      # List of ( nutrient_name, lower, upper )
                  food_item_equality_constraints = [], # List of ( food_item_id, value ) 
                  food_item_limit_constraints = []     # List of ( food_item_id, lower, upper )
                  nutrient_goals = [],                 # List of ( nutrient_name, goal value )
                  food_item_goals = [] ):              # List of ( food_item_id, goal value )
        '''
        '''
        
        self.name = name
        
        FIs = FoodItems()

        self.food_items = {}
        for food_item_id, amount in food_items:
           if FIs.get_food_item( food_item_id ): 
               self.food_items[food_item_id] = amount
               
        self.nutrient_constraints = []
        for nutrient_equality_constraint in nutrient_equality_constraints:
            


class FoodItem( object ):
    '''Something that can be added to a meal in some quantity.
    
    Fields:
    * uuid - unique across FoodItems
    * name - The name - duplication permitted
    * serving_size - Optional - grams per serving
    * _nutrients - A dictionary of nutrient_name -> amount per gram of
      FoodItem

    Methods:
    get_nutrients - Returns a dictionary of nutrient_name->amount per
    gram of FoodItem
    '''

    def __init__( self, DEBUG ):
        '''
        '''
        pass

    def some_recipe_only_thing( self ):
        '''Clients must override this method.'''
        raise NotImplementedError()

class Recipe( FoodItem ):
    '''A collection of FoodItems that make up a new FoodItem of type Recipe.

    Fields:
    * serving_size - Optional - grams per serving
    * ingredients - An array of FoodItems (note - Recipe's can't be ingredients)
    
    Methods:
    get_nutrients - Returns a dictionary of nutrient_name->amount per gram of recipe
    '''

    def __init__( self, DEBUG ):
        # DEBUG - strongly consider a **kwargs argument approach, and
        # then any remaining args become nutrients? Or we iterate over
        # the list of nutrients.
        '''
        '''
        super( Recipe, self ).__init__( args )
        pass


# DEBUG - We'll have a method, class, or static objects that defined
# what nutrient feilds we are interested in and their units?
#
# We support a get_nutrients method that takes in the raw food item
# and returns a smaller dictionary of the desired fields that we care
# about for Nutrients.
# 
# A row from the database can be turned into a dict with the
# to_serializable_dict() method.
#
# Then its keys are the nutrient names (give or take - we don't care
# about id, uuid, created_date, ...)



class FoodItems( object ):
    '''Singleton class for managing our database of FoodItems and Recipes.
    
    Members:
    food_items - Dictionary of food_item / recipe uuid -> FoodItem

    DEBUG - Document all this.
    '''

    food_items = None

    def __init__( self, DEBUG ):
        if FoodItems.food_items is None:
            # Connect to database and load in all the food_items.
            pass
        pass

    def get_food_item( self, food_item_id, types = [] ):
        '''Given a FoodItem.id returns the corresponding FoodItem object. If
        types is provided returon only items whose types match those
        in the types array, e.g. FoodItem or Recipe.
        '''

        food_item = None
        if food_item_id in FoodItems.food_items:
            food_item = FoodItems.food_items[food_item_id]
        else:
            raise Exception( "No such food item found: %s" % ( food_item_id ) )

        if food_item and len( types ) == 0:
            return food_item
        else:
            for food_type in types:
                if food_item.type() == food_type:
                    return food_item
            raise Exception( "Food item %s exists, but is of the wrong type: %s" % ( food_item_id, food_item.type() ) )

    def get_food_items( self, types = [] ):
        '''Returns an array of all food items.  If types is provided, the
        result will be restircted to the provided types, e.g. Recipe
        or FoodItem.
        '''
        all_types = False
        types_map = {}
        if len( types ) == 0:
            all_types = True
        else:
            for food_type in types:
                types_map[food_type] = True

        return [ x[1] for x in sorted( FoodItems.food_items.items() ) if ( all_types or x[1].type() in types_map ) ]

    def add_food_item( self, food_item ):
        '''Stores new FoodItem in database.'''
        pass

    def add_recipe( self, recipe ):
        '''Stores new Recipe in database.'''
        pass



