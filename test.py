#!/usr/bin/env python

import scipy.optimize

'''
# Example:
fun = lambda x: (x[0] - 1)**2 + (x[1] - 2.5)**2
cons = ({'type': 'ineq', 'fun': lambda x:  x[0] - 2 * x[1] + 2},
        {'type': 'ineq', 'fun': lambda x: -x[0] - 2 * x[1] + 6},
        {'type': 'ineq', 'fun': lambda x: -x[0] + 2 * x[1] + 2})
bnds = ((0, None), (0, None))
res = minimize(fun, (2, 0), method='SLSQP', bounds=bnds,
               constraints=cons)
'''

# DEBUG FIX THE MADNESS WITH 1/2 LABELS AND 1/2 INDICES, CONSIDER
# MAKING EVERYTHING A CLASS.
# macro_nuts [ class::macro_nut( 'protein', 300, 0.8, 1.2 )... ]

macro_nuts = [ 'protein', 'carbs', 'fat' ]
macro_goals = [ 300, 400, 300 ]
macro_lower_bound = 0.8
macro_upper_bound = 1.2

micro_nuts = [ 'vitamin C', 'calcium' ]
micro_goals = [ 0.075, 0.8 ]

# All nutritional values per gram.

# DEBUG - additional food parameters:
# OPTIONAL Serving size - then we can keep the min/max of the food to 1/2 and 4 servings?
# (fillers have no serving size)

foods = [ 
    { 'name' : 'asparagus',
      'micro_nuts' : {
          'vitamin C' : 0.000077,
          'calcium' : .00023
      },
      'kcal' : 0.22, 
      'macro_nuts' : {
          'protein' : 0.096,
          'carbs' : 0.1644,
          'fat' : 0.0198
      },
  },
    { 'name' : 'chicken',
      'micro_nuts' : {
          'vitamin C' : 0,
          'calcium' : 0.00006
      },
      'kcal' : 0.79,
      'macro_nuts' : {
          'protein' : 0.6716,
          'carbs' : 0.0868,
          'fat' : 0.0351
      },
  },
    { 'name' : 'protein filler',
      'micro_nuts' : {
          'vitamin C' : 0,
          'calcium' : 0
      },
      'kcal' : 4.0,
      'macro_nuts' : {
          'protein' : 4.0,
          'carbs' : 0.0,
          'fat' : 0.0
      },
  },
    { 'name' : 'carb filler',
      'micro_nuts' : {
          'vitamin C' : 0,
          'calcium' : 0
      },
      'kcal' : 4.0,
      'macro_nuts' : {
          'protein' : 0.0,
          'carbs' : 4.0,
          'fat' : 0.0
      },
  },
    { 'name' : 'fat filler',
      'micro_nuts' : {
          'vitamin C' : 0,
          'calcium' : 0
      },
      'kcal' : 9.0,
      'macro_nuts' : {
          'protein' : 0.0,
          'carbs' : 0.0,
          'fat' : 9.0
      },
  },
]

def micro_nutrient_goodness( x ):
    '''Calculate the micronutrient goodness for input array of foods x.'''
    result = 0

    for idx, micro_nut in enumerate( micro_nuts ):
        micro_total = 0
        for inner_idx, val in enumerate( x ):
            micro_total += val*foods[inner_idx]['micro_nuts'][micro_nut]

        result += ( max( micro_goals[idx] - micro_total, 0 ) / micro_goals[idx] )**2

    return result
    
cons = ( 
    # goal*.8 <= protein <= goal*1.2
    { 'type' : 'ineq', 'fun' : lambda x: reduce( lambda y, z: y+foods[z]['macro_nuts']['protein']*x[z], range( len( x ) ), 0 ) - macro_lower_bound*macro_goals[0] },
    { 'type' : 'ineq', 'fun' : lambda x: macro_upper_bound*macro_goals[0] - reduce( lambda y, z: y+foods[z]['macro_nuts']['protein']*x[z], range( len( x ) ), 0 )},

    # goal*.8 <= carbs <= goal*1.2
    { 'type' : 'ineq', 'fun' : lambda x: reduce( lambda y, z: y+foods[z]['macro_nuts']['carbs']*x[z], range( len( x ) ), 0 ) - macro_lower_bound*macro_goals[1] },
    { 'type' : 'ineq', 'fun' : lambda x: macro_upper_bound*macro_goals[1] - reduce( lambda y, z: y+foods[z]['macro_nuts']['carbs']*x[z], range( len( x ) ), 0 )},

    # goal*.8 <= fat <= goal*1.2
    { 'type' : 'ineq', 'fun' : lambda x: reduce( lambda y, z: y+foods[z]['macro_nuts']['fat']*x[z], range( len( x ) ), 0 ) - macro_lower_bound*macro_goals[2] },
    { 'type' : 'ineq', 'fun' : lambda x: macro_upper_bound*macro_goals[2] - reduce( lambda y, z: y+foods[z]['macro_nuts']['fat']*x[z], range( len( x ) ), 0 )},

    # kcal == goal
    { 'type' : 'eq', 'fun' : lambda x: reduce( lambda a, b: a+b, macro_goals ) - reduce( lambda c, d: c+foods[d]['macro_nuts']['protein']*x[d] + foods[d]['macro_nuts']['carbs']*x[d] + foods[d]['macro_nuts']['fat']*x[d], range( len( x ) ), 0 ) },

)

def max_grams( food ):
    '''Puts out the maximum value of this food that does not cause it to
    exceed half of any macro or micronutrient.
    '''

    max_so_far = float( 'inf' )
    for idx, macro_nut in enumerate( macro_nuts ):
        if food['macro_nuts'][macro_nut] != 0:
            current_max = macro_goals[idx] / food['macro_nuts'][macro_nut]
            if current_max < max_so_far:
                max_so_far = current_max

    return max_so_far

def initial_grams( food ):
    '''Puts out the maximum value of this food that does not cause it to
    exceed half of any macro or micronutrient.
    '''

    initial_so_far = max_grams( food )
    if initial_so_far < float( 'inf' ):
        initial_so_far = initial_so_far / 2

    for idx, micro_nut in enumerate( micro_nuts ):
        if food['micro_nuts'][micro_nut] != 0:
            current_initial = micro_goals[idx] / 2*food['micro_nuts'][micro_nut]
            if current_initial < initial_so_far:
                initial_so_far = current_initial

    return initial_so_far
            


bnds = map( lambda x: ( 0, max_grams( x ) ), foods )

res = scipy.optimize.minimize( micro_nutrient_goodness, ( initial_grams(foods[0]), initial_grams(foods[1]), 0, 0, 0 ), method='SLSQP', bounds=bnds, constraints=cons )

print "Minimization success = %s, micronutrient_goodness = %0.02f" % ( res['success'], res['fun'] )

def cals_from_food( food, grams ):
    return food['macro_nuts']['protein']*grams + food['macro_nuts']['carbs']*grams+ food['macro_nuts']['fat']*grams


total_cals = 0
total_micro_nuts = [ 0, 0 ]
total_macro_nuts = [ 0, 0, 0]
for idx, food in enumerate( foods ):
    print "Included %0.01f grams of %s for %0.01f calories." % ( res['x'][idx], food['name'], cals_from_food( food, res['x'][idx] ) )
    total_cals += cals_from_food( food, res['x'][idx] )

    for inner_idx, micro_nut in enumerate( micro_nuts ):
        print "\tIncluded %0.01f milligrams of %s for %0.02f%% of DRI." % ( 1000*res['x'][idx]*food['micro_nuts'][micro_nut], micro_nut, 100*res['x'][idx]*food['micro_nuts'][micro_nut] / micro_goals[inner_idx] )
        total_micro_nuts[inner_idx] += 100*res['x'][idx]*food['micro_nuts'][micro_nut] / micro_goals[inner_idx]

    for inner_idx, macro_nut in enumerate( macro_nuts ):
        print "\tIncluded %0.01f kcal of %s for %0.02f%% of DRI." % ( res['x'][idx]*food['macro_nuts'][macro_nut], macro_nut, 100*res['x'][idx]*food['macro_nuts'][macro_nut] / macro_goals[inner_idx] )
        total_macro_nuts[inner_idx] += 100*res['x'][idx]*food['macro_nuts'][macro_nut] / macro_goals[inner_idx]

print "\n"        
                                                         
print "Micronutrients:"
for inner_idx, micro_nut in enumerate( micro_nuts ):
    print "\tMeal supplied %0.02f%% of %s DRI." % ( total_micro_nuts[inner_idx], micro_nut )

print "Macronutrients:"
for inner_idx, macro_nut in enumerate( macro_nuts ):
    print "\tMeal supplied %0.02f%% of %s DRI." % ( total_macro_nuts[inner_idx], macro_nut )

print "Total calories: %0.01f" % ( total_cals )
