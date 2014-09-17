#! /usr/bin/env python

import codecs
import datetime
from decimal import *
import os
import pprint
import re

import django
django.setup()
from meal_planning import *

data_dir = '/wintmp/nutrition/'

# Column transformations.

def nullable( func ):
    def handle_nulls( value ):
        if value is None or value == '':
            return None
        else:
            return func( value )
    return handle_nulls

ndecimal = nullable( Decimal )
nunicode = nullable( unicode )
nint = nullable( int )

def y2b( value ):
    if value is None or value == 'N':
        return False
    else:
        return True

def date_handler( value ):
    return datetime.datetime.strptime( value, '%m/%Y' )

ndate_handler = nullable( date_handler )

food_group_desc_fields = [
    ( 'food_group_id', unicode ),
    ( 'food_group_desc', unicode )
]

food_desc_fields = [
    ( 'ndb_id', unicode ),
    ( 'food_group_id', unicode ), # FK, not used in our consolidated one.
    ( 'long_desc', unicode ),
    ( 'short_desc', unicode ),
    ( 'common_name', nunicode ),
    ( 'manufacturer', nunicode ),
    ( 'is_fndds', y2b ), # MUST CONVERT TO BOOLEAN
    ( 'refuse_desc', nunicode ),
    ( 'refuse_pct', ndecimal ),
    ( 'scientific_name', nunicode ),
    ( 'nitrogen_factor', ndecimal ), # CONVERT to 4.2 DECIMAL, SAME FOR NEXT THREE
    ( 'protein_factor', ndecimal ), # CONVERT
    ( 'fat_factor', ndecimal ), # convert
    ( 'carb_factor', ndecimal )
]

langual_factor_fields = [
    ( 'ndb_id', unicode ),
    ( 'langual_code', unicode )
]

langual_factor_desc_fields = [
    ( 'langual_code', unicode ),
    ( 'langual_desc', unicode )
]

weight_fields = [
    ( 'ndb_id', unicode ), # The FK into food_desc_fields
    ( 'sequence', int ), # Not used.
    ( 'quantity', Decimal ),# N 5.3
    ( 'unit', unicode ),
    ( 'grams', Decimal ),
    ( 'data_points', nint ),
    ( 'std_dev', ndecimal )
]

nutrient_sources = [
    ( 'id', int ), # NOTE - we must explicitly set this to ensure consistency.
    ( 'source_desc', unicode )
]

nutrient_fields = [
    ( 'ndb_id', unicode ), # FK
    ( 'nutrient_id', unicode ),
    ( 'amount', Decimal ), # NOTE - THIS MUST BE MODIFIED BY THE UNIT IN NUTRIENT_DEFINITION, AND DIVIDED BY 100.
    ( 'data_points', int ),
    ( 'std_err', ndecimal ),
    ( 'nutrient_source_id', unicode ), # FK to the nutrient sources table.
    ( 'nutrient_derivation_id', nunicode ),  #FK to derivation tables.
    ( 'reference_food_item_id', nunicode ), # NOTE - NOT USED - OUR APP HAS NO USE FOR PROVENANCE INFORMATION OF NUTRITION VALUES LIKE THIS.
    ( 'is_fortified', y2b ), # NOTE - MUST CONVERT FROM Y/N to BOOLEAN
    ( 'studies', nint ),
    ( 'min_value', ndecimal ),
    ( 'max_value', ndecimal ),
    ( 'freedom_degrees', nint ),
    ( 'lower_error_bound', ndecimal ),
    ( 'upper_error_bound', ndecimal ),
    ( 'stat_comments', nunicode ),
    ( 'updated_date', ndate_handler ), # NOTE - WE MUST EXPLICITLY SET THIS ONE TO NULL OR IT WILL PICK UP THE DEFAULT OF NOW.
    ( 'confidence_code', nunicode ) # NOT USED
]    

nutrient_data_definitions = [
    ( 'derivation_id', unicode ),
    ( 'derivation_desc', unicode )
]

nutrient_conversion_factors = {
    'g' : Decimal( '.01' ),
    'mg' : Decimal( '.00001' ),
    'ug' : Decimal( '.00000001' ),
    'UI' : Decimal( '.01' ),
    'kcal' : Decimal( '.01' )
}

nutrient_definition_fields = [
    ( 'nutrient_id', unicode ),
    ( 'unit', unicode ),# NOTE - ALL UNITS EXCEPT kcal and UI are converted into g
    # FURTHER NOTE, any kJ items are to be excluded.
    ( 'infoods_tag', nunicode ),
    ( 'nutrient', unicode ),
    ( 'decimal_places', nunicode ), # Not used.
    ( 'sort_order', int )
]

footnote_fields = [
    ( 'ndb_id', unicode ), # FK to nutrients
    ( 'footnote_number', int ),
    ( 'footnote_type', unicode ),
    ( 'nutrient_id', nunicode ), # FK to nutrients,
    ( 'footnote', unicode )
]

citation_link_fields = [
    ( 'ndb_id', unicode ), # Part of composite FK to food_item_nutrients
    ( 'nutrient_id', unicode ), # Other part of composite key
    ( 'citation_id', unicode ) # Not used, but FK to citations.
]

citation_fields = [
    ( 'citation_id', unicode ),
    ( 'authors', nunicode ),
    ( 'title', unicode ),
    ( 'year', nunicode ),
    ( 'journal', nunicode ),
    ( 'volume', nunicode ),
    ( 'issue', nunicode ),
    ( 'start_page', nint ),
    ( 'end_page', nint )
]


'''
DATA_SRC.txt  denormalized schema.txt  FD_GROUP.txt  FOOTNOTE.txt  LANGUAL.txt   NUTR_DEF.txt  WEIGHT.txt
DATSRCLN.txt  DERIV_CD.txt             FOOD_DES.txt  LANGDESC.txt  NUT_DATA.txt  SRC_CD.txt

class FoodItems( models.Model ):
class FoodItemServingSizes( models.Model ):
class NutrientSources( models.Model ):
class NutrientDerivations( models.Model ):
class FoodItemNutrients( models.Model ):
class Footnotes( models.Model ):
class NutrientCitations( models.Model ):
'''

files = [
    { 
        'name' : 'NutrientCitations',
        'filename' : 'DATA_SRC.txt',
        'columns' : citation_fields,
        'import_order' : 1,
        'pk' : [ 'citation_id' ],
        'pk_idx' : [ 0 ]
    },
    { 
        'name' : 'NutrientCitationsLink',
        'filename' : 'DATSRCLN.txt',
        'columns' : citation_link_fields,
        'import_order' : 0,
        'pk' : [ 'ndb_id', 'nutrient_id', 'citation_id' ],
        'pk_idx' : [ 0, 1, 2 ]
    },
    { 
        'name' : 'NutrientDerivations',
        'filename' : 'DERIV_CD.txt',
        'columns' : nutrient_data_definitions,
        'import_order' : 2,
        'pk' : [ 'derivation_id' ],
        'pk_idx' : [ 0 ]
    },
    { 
        'name' : 'FoodGroup',
        'filename' : 'FD_GROUP.txt',
        'columns' : food_group_desc_fields,
        'import_order' : 3,
        'pk' : [ 'food_group_id' ],
        'pk_idx' : [ 0 ]
    },
    { 
        'name' : 'FoodItems',
        'filename' : 'FOOD_DES.txt',
        'columns' : food_desc_fields,
        'import_order' : 7,
        'pk' : [ 'ndb_id' ],
        'pk_idx' : [ 0 ]
    },
    { 
        'name' : 'Footnotes',
        'filename' : 'FOOTNOTE.txt',
        'columns' : footnote_fields,
        'import_order' : 11,
        'pk' : None,
        'pk_idx' : None
    },
    { 
        'name' : 'LanguaLDesc',
        'filename' : 'LANGDESC.txt',
        'columns' : langual_factor_desc_fields,
        'import_order' : 4,
        'pk' : [ 'langual_code' ],
        'pk_idx' : [ 0 ]
    },
    { 
        'name' : 'LanguaLLink',
        'filename' : 'LANGUAL.txt',
        'columns' : langual_factor_fields,
        'import_order' : 5,
        'pk' : [ 'ndb_id', 'langual_code' ],
        'pk_idx' : [ 0, 1 ]
    },
    { 
        'name' : 'FoodItemNutrients',
        'filename' : 'NUT_DATA.txt',
        'columns' : nutrient_fields,
        'import_order' : 10,
        'pk' : [ 'ndb_id', 'nutrient_id' ],
        'pk_idx' : [ 0, 1 ]
    },
    { 
        'name' : 'FoodItemNutrientDefinition',
        'filename' : 'NUTR_DEF.txt',
        'columns' : nutrient_definition_fields,
        'import_order' : 7,
        'pk' : [ 'nutrient_id' ],
        'pk_idx' : [ 0 ]
    },
    { 
        'name' : 'NutrientSources',
        'filename' : 'SRC_CD.txt',
        'columns' : nutrient_sources,
        'import_order' : 8,
        'pk' : [ 'id' ],
        'pk_idx' : [ 0 ]
    },
    { 
        'name' : 'FoodItemServingSizes',
        'filename' : 'WEIGHT.txt',
        'columns' : weight_fields,
        'import_order' : 9,
        'pk' : [ 'ndb_id', 'sequence' ],
        'pk_idx' : [ 0, 1 ]
    },
]

data = {}

# DONT FILL THIS OUT TILL THINGS ARE CLEARER...
'''
relations = [
    {
        'parent' : varname,
        'child' : varname,
        'keys' : [ 'keycol1', 'keycol2' ]
    },
]
'''

# DEBUG - see if we can initialize a DB row from a hash, if so then
# maybe make a mapping hash.

# DEBUG - What data structure builds up common relations?

for df in sorted( files, key=lambda x: x['import_order'] ):
    filename = "%s%s" % ( data_dir, df['filename'] )
    columns = df['columns']
    name = df['name']
    pk_idx = df['pk_idx']

    print "Working on %s - %s" % ( filename, name )
    if not os.path.exists( "%s" % ( filename ) ):
        raise Exception( "Couldn't find file: %s" % ( filename ) )
        
    f = open( filename, mode='r' )
    
    for line in f:
        line = unicode( line.decode( 'latin1' ) )

        # Skip blank lines.
        if re.search( u'^\s*$', line ):
            continue

        line = line.rstrip( "\n" )
        column_data = line.split( '^' )
        if ( len( column_data ) != len( columns ) ):
            raise Exception( "Malformed line found, had %d columns, expected %d, line was: '%s'" %  ( len( column_data ), len( columns ), line ) )
        
        column_fields = []
                
        for col_no, field in enumerate( column_data ):
            field = field.strip( '~' )
            field_data = columns[col_no][1]( field )
            column_fields.append( field_data )
            print "Column %s: %s -> %s" % ( columns[col_no][0], field, field_data )
            
        if pk_idx is not None:
            if name not in data:
                data[name] = {}

            #import pdb
            #pdb.set_trace()
            keys = len( pk_idx )
            current = data[name]
            for idx, key in enumerate( pk_idx ):
                value = column_fields[pk_idx[idx]]
                if idx < keys-1:
                    if value in current:
                        current = current[value]
                    else:
                        current[value] = {}
                        current = current[value]
                else:
                    if value in current:
                        raise Exception( "PK Uniqeness violation!" )
                    else:
                        current[value] = column_fields
        else:
            if name in data:
                data[name].append( column_fields )
            else:
                data[name] = [ column_fields ]

        # Now or never - start adding to the ORM.

pp = pprint.PrettyPrinter( indent=4 )

pp.pprint( data )

FoodItems = [
    'uid'
]

FoodItems += food_desc_fields + food_group_desc_fields + langual_factor_desc_fields

# Add to food items.
FoodItemServingSizes = [ weight_fields[2:] ]

#FoodItemNutrients = DEBUG

