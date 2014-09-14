#!/usr/bin/env python

import copy
import scipy.optimize
import uuid

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
    
    Outputs: An array of ( meal_score, added_food_item, new_meal )
    tuples, lower scores are better.

    For each food_item if it is possible to craft a new Meal that has
    a better (e.g. lower) fitness function value by adding that item
    and optional filler_items to the base Meal, a new ( meal_score,
    added_food_item meal ) tuple is added to the output.

    '''
    result_meals = []

    '''The input to the lambda function is an array of amounts, where the
    i'th item corresponds to the i'th fitness_food_item.
    
    We want to sum up the food_item.get_nutrition()[nutrition] for
    the calculation.

    So: given x, the numerical index of the fitness food item, how do
    we infer the food_item of the it's position of
    fitness_food_items...

    '''

    for fi in food_items:
        fitness_food_items = [ x[0] for x in meal.get_food_items ] + [ fi ] + filler_items

        constraints = []
        for nutrient, constraint_type, amount in meal.nutrient_constraints:
            if constraint_type == 'eq':
                constraints.append( {
                    'type' : 'eq',
                    'fun' : lambda amounts: amount - reduce( lambda tot, ffi_idx: tot + fitness_food_items[ffi_idx].get_nutrition()[nutrient]*amounts[ffi_idx], range( len( amounts ) ), 0 ) } )
            elif constraint_type == 'lt':
                constraints.append( {
                    'type' : 'ineq',
                    'fun' : lambda amounts: amount - reduce( lambda tot, ffi_idx: tot + fitness_food_items[ffi_idx].get_nutrition()[nutrient]*amounts[ffi_idx], range( len( amounts ) ), 0 ) } )
            elif constraint_type == 'gt':
                constraints.append( {
                    'type' : 'ineq',
                    'fun' : lambda amounts: reduce( lambda tot, ffi_idx: tot + fitness_food_items[ffi_idx].get_nutrition()[nutrient]*amounts[ffi_idx], range( len( amounts ) ), 0 ) - amount } )

        bounds = []

        fitness_food_items_map = {}
        for idx, ffi in enumerate( fitness_food_items ):
            fitness_food_items_map[ffi.uuid] = idx

        for ffi in fitness_food_items:
            bounds.append( ( None, None ) )

        for food_item_id, constraint_type, bounds in meal.food_item_constraints:
            bounds_idx = None
            if food_item_id in fitness_food_items_map:
                bounds_idx = fitness_food_items_map[food_item_id]

                bounds[bounds_idx] = bounds
        
        def meal_fitness_function( food_item_amounts ):
            return fitness_function( meal, fitness_food_items, food_item_amounts )

        result = scipy.optimize.minimize( meal_fitness_function, 
                                          [0]*len( fitness_food_items ), # Initial guess all 0
                                          method='SLSQP', 
                                          bounds=bounds, 
                                          constraints=constraints )
        
        if result['success']:
            meal_score = result['fun']
            meal_food_items = []
            for ffi_idx, food_item_amount in enumerate( result['x'] ):
                food_item = fitness_food_items[ffi_idx]
                meal_food_items.append( ( food_item.uuid, food_item_amount ) )
            new_meal = copy.deepcopy( meal )
            new_meal.replace_food_items( meal_food_items )
            result_meals.append( ( meal_score, fi, new_meal ) )

    return sorted( result_meals, reverse=True )
                
            
def sum_lesser_squares( meal, food_items, food_item_amounts ):
    '''A fitness function to be minimized, returns:
    
    sum over all food_items and nutrition goals such that:
       max( 0, ( 1 - % of goal met by food items and food item amounts )^2 )
    '''
    result = 0.0
    for nutrient, goal in meal.nutrient_goals.items():
        current = 0.0
        if goal != 0:
            for fi_idx, fi in enumerate( food_items ):
                current += fi.get_nutrients()[nutrient] * food_item_amounts[fi_idx]

            result += ( max( 0.0, ( goal - current ) ) / goal )**2

    food_items_map = {}
    for fi_idx, fi in enumerate( food_items ):
        food_items_map[fi.uuid] = fi_idx

    for food_item_id, goal in meal.foot_item_goals.items():
        if goal != 0:
            if food_item_id in food_items_map:
                result += ( max( 0.0, ( goal - food_item_amounts[food_items_map[food_item_id]] ) ) / goal )**2

    return result

            
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
      + Note: food_item_constraints are ignored if that food item is
        not present in the Meal or being considered for addition to
        the Meal (e.g. a constraint of at least 100 grams of peanut
        butter does not cause a constraint violation in a recipe
        involving only tortillas, chicken, and lettuce - however once
        peanut butter is considered as an addition then a constraint
        violation could occur if the meal could not accommodate 100
        grams of peanut butter.
    * nutrient_goals - A dictionary of nutrient-> amount goals for this meal
    * food_item_goals - A dictionary of food_item_id -> amount goals for this meal

    Methods:
    add_food_item( food_item_id, amount )
    add_nutrient_constraint( nutrient, constraint_type, amount )
    add_food_item_constraint( food_item_id, type, amount )
    type is one of 'eq' or 'limits'
    If type is 'eq' amount is a number expressed in units of the Nutrients object.
    If type is 'limits' amount is a ( lower_bound, upper_bound ) tuple,
    where an amount of None means there is no bound in that direction.

    add_nutrient_goal( nutrient, amount )
    add_nutrient_goal( food_item_id, amount )

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
                  nutrient_equality_constraints = [],  # List of ( nutrient_name, amount ) 
                  nutrient_limit_constraints = [],     # List of ( nutrient_name, lower, upper )
                  food_item_equality_constraints = [], # List of ( food_item_id, amount ) 
                  food_item_limit_constraints = [],    # List of ( food_item_id, lower, upper )
                  nutrient_goals = [],                 # List of ( nutrient_name, goal amount )
                  food_item_goals = [] ):              # List of ( food_item_id, goal amount )
        '''
        '''
        
        self.name = name
        
        self.FIs = FoodItems()
        self.food_items = {}
        for food_item_id, amount in food_items:
            self.add_food_item( food_item_id, amount )
               
        self.NUTs = Nutrients().get_nutrient_types()
        self.nutrient_constraints = []
        for nutrient, amount in nutrient_equality_constraints:
            self.add_nutrient_constraint( nutrient, 'eq', amount )

        for nutrient, lower_bound, upper_bound in nutrient_limit_constraints:
            self.add_nutrient_constraint( nutrient, 'limits', ( lower_bound, upper_bound ) )

        self.food_item_constraints = []
        for food_item_id, amount in food_item_equality_constraints:
            self.add_food_item_constraint( food_item_id, 'eq', amount )

        for food_item_id, lower_bound, upper_bound in food_item_limit_constraints:
            self.add_food_item_constraint( food_item_id, 'limits', ( lower_bound, upper_bound ) )

        self.nutrient_goals = {}
        for nutrient, amount in nutrient_goals:
            self.add_nutrient_goal( nutrient, amount )

        self.food_item_goals = {}
        for food_item_id, amount in food_item_goals:
            self.add_food_item_goal( food_item_id, amount )

    def add_food_item( self, food_item_id, amount ):
        if self.FIs.get_food_item( food_item_id ): 
            self.food_items[food_item_id] = amount

    def add_nutrient_constraint( self, nutrient, constraint_type, amount ):
        if nutrient not in self.NUTs:
            raise Exception( "No such nutrient: %s, valid nutrients are: %s" % ( nutrient, self.NUTs.keys() ) )

        if constraint_type == 'eq':
            self.nutrient_constraints.append( ( nutrient, 'eq', amount ) )
        elif constraint_type == 'limits':
            lower_bound = amount[0]
            upper_bound = amount[1]
            if lower_bound is not None:
                self.nutrient_constraints.append( nutrient, 'gt', lower_bound )
            if upper_bound is not None:
                self.nutrient_constraints.append( nutrient, 'lt', upper_bound )

    def add_food_item_constraint( self, food_item_id, constraint_type, amount ):
        if self.FIs.get_food_item( food_item_id ):
            if constraint_type == 'eq':
                self.food_item_constraints.append( ( food_item_id, ( amount, amount ) ) )
            elif constraint_type == 'limits':
                self.food_item_constraints.append( food_item_id, amount )

    def add_nutrient_goal( self, nutrient, amount ):
        if nutrient not in self.NUTs:
            raise Exception( "No such nutrient: %s, valid nutrients are: %s" % ( nutrient, self.NUTs.keys() ) )

        self.nutrient_goals[nutrient] = amount

    def add_food_item_goal( self, food_item_id, amount ):
        if self.FIs.get_food_item( food_item_id ):
            self.food_item_goals[food_item_id] = amount

    def replace_food_items( self, food_items ):
        '''Replace the current self.food_items with the ( food_item_id, amount
        ) tuples in food_items.'''
        self.food_items = {}
        for food_item_id, amount in food_items:
            self.add_food_item( food_item_id, amount )
    

    def get_food_items( self ):
        '''Return all our food items, in descending order of their amounts.'''
        return sorted( [ ( a, b ) for a, b in self.food_items.items() ], key=lambda x: x[1], reverse=True )

    def get_nutrients( self ):
        result = {}
        for fi, amount in self.food_items.items():
            for nutrient, amount_per in self.FIs.get_food_item( fi ).get_nutrients().items():
                if nutrient in result:
                    result[nutrient] += amount * amount_per
                else:
                    result[nutrient] = amount * amount_per
        return result

class FoodItem( object ):
    '''Something that can be added to a meal in some quantity.
    
    Fields:
    * uuid - unique across FoodItems
    * name - The name - duplication permitted
    * serving_size - Optional - grams per serving
    * _nutrients - A dictionary of nutrient_name -> amount per gram of
      FoodItem.  This member is private, get_nutrients must be used to
      access it.

    Methods:
    * add_nutrient( nutrient, amount_per_gram ) - Add a nutrient to the
    FoodItem with amount_per_gram of the nutrient per gram of
    FoodItem.
    * get_nutrients - Returns a dictionary of nutrient_name->amount per
    gram of FoodItem

    '''

    def __init__( self, name, nutrients={}, serving_size=None, uuid=None ):
        '''Inputs:
        * name - The name of this food item.
        * nutrients - Optional, a dictionary of
          nutrient->amount_per_gram_of_FoodItem, defaults to empty.
        * serving_size - Optional, defaults to None.
        * uuid - Optional, defaults to a new uuid.
        '''

        self.NUTs = Nutrients().get_nutrient_types()

        self.name = name
        self._nutrients = nutrients
        self.serving_size = serving_size

        if uuid is not None:
            self.uuid = uuid
        else:
            self.uuid = str( uuid.uuid4() )

    def add_nutrient( self, nutrient, amount_per_gram ):
        if nutrient in self.NUTs:
            self._nutrients[nutrient] = amount_per_gram

    def get_nutrients( self ):
        return self._nutrients

class Recipe( FoodItem ):
    '''A collection of FoodItems that make up a new FoodItem of type Recipe.

    Fields:
    * serving_size - Optional - grams per serving
    * ingredients - An array of ( food_item_id, amount ) tuples (note -
      Recipe's can't be included as an ingredient, only FoodItem base
      class instances.
 
    Methods:
    * add_ingredient( food_item_id, amount )
    * get_nutrients - Returns a dictionary of nutrient_name->amount per gram of recipe
    '''

    def __init__( self, name, ingredients=[], serving_size=None, uuid=None ):
        '''Inputs:
        * name - The name of this food item.
        * ingredients - Optional, an array of FoodItem, amount tuples.
        * serving_size - Optional, defaults to None.
        * uuid - Optional, defaults to a new uuid.
        '''

        super( Recipe, self ).__init__( name, nutrients={}, serving_size=serving_size, uuid=uuid )

        self.FIs = FoodItems()

        for food_item_id, amount in ingredients:
            self.add_ingredient( food_item_id, amount )

    def add_nutrient( self ):
        '''You can't add nutrients to a recipe, only ingredients.'''
        raise NotImplementedError()

    def add_ingredient( self, food_item_id, amount ):
        fi = self.FIs.get_food_item( food_item_id )
            
        for nutrient, amount_per in fi.get_nutrients().items():
            if nutrient in self._nutrients:
                self._nutrients += amount * amount_per
            else:
                self._nutrients[nutrient] = amount * amount_per

    def get_nutrients( self ):
        return self._nutrients
        

class Nutrients( object ):
    '''Singleton-esque class for managing our Nutrients and their units.'''

    # Class level variable that defines what our possible nutrients
    # are, and their units.
    nutrients = {
        'kcal'      : 'kcal', # Not technically a nutrient, but convenient.
        'fat'       : 'grams',
        'carbs'     : 'grams',
        'protein'   : 'grams',
        'vitamin C' : 'grams',
        'calcium'   : 'grams'
    }

    def __init__( self ):
        self.nutrients = Nutrients.nutrients

    def get_nutrient_types( self ):
        return self.nutrients

class FoodItems( object ):
    '''Singleton-eqsue class for managing our database of FoodItems and Recipes.
    
    Members:
    food_items - Dictionary of food_item / recipe uuid -> FoodItem

    DEBUG - Document all this.
    '''

    food_items = None

    def __init__( self, DEBUG ):
        if FoodItems.food_items is None:
            # Connect to database and load in all the food_items.

            # DEBUG - for a toy implementation we try this.
            asparagus = FoodItem( 'asparagus',
                                  nutrients = {
                                      'vitamin C' : 0.000077,
                                      'calcium' : .00023,
                                      'kcal' : 0.22, 
                                      'protein' : 0.024,
                                      'carbs' : 0.0411,
                                      'fat' : 0.0198/9
                                  } )
            FoodItems.food_items[asparagus.uuid] = asparagus

            chicken = FoodItem( 'chicken',
                                nutrients = {
                                    'vitamin C' : 0,
                                    'calcium' : 0.00006,
                                    'kcal' : 0.79,
                                    'protein' : 0.6/4,
                                    'carbs' : 0.0868/4,
                                    'fat' : 0.0351/9
                                } )
            FoodItems.food_items[chicken.uuid] = chicken
                                  
            pfill = FoodItem( 'protein filler',
                              nutrients = {
                                  'vitamin C' : 0,
                                  'calcium' : 0,
                                  'kcal' : 4.0,
                                  'protein' : 1.0,
                                  'carbs' : 0.0,
                                  'fat' : 0.0
                              }
            FoodItems.food_items[pfill.uuid] = pfill

            cfill = FoodItem( 'carbs filler',
                              nutrients = {
                                  'vitamin C' : 0,
                                  'calcium' : 0,
                                  'kcal' : 4.0,
                                  'protein' : 0.0,
                                  'carbs' : 1.0,
                                  'fat' : 0.0
                              }
            FoodItems.food_items[cfill.uuid] = cfill

            ffill = FoodItem( 'fat filler',
                              nutrients = {
                                  'vitamin C' : 0,
                                  'calcium' : 0,
                                  'kcal' : 9.0,
                                  'protein' : 0.0,
                                  'carbs' : 0.0,
                                  'fat' : 1.0
                              }
            FoodItems.food_items[ffill.uuid] = ffill


    def get_food_item( self, food_item_id, types = [] ):
        '''Given a FoodItem.id returns the corresponding FoodItem object. If
        types is provided return only items whose types match those
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
        result will be restricted to the provided types, e.g. Recipe
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



