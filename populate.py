#! /usr/bin/env python

import codecs
import datetime
from decimal import *
import os
import pprint
import re
import uuid

import django
django.setup()
from meal_planner.models import *

data_dir = '/wintmp/nutrition/full/'

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
    if value is None or value == 'N' or value == '':
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
    ( 'is_fndds', y2b ), 
    ( 'refuse_desc', nunicode ),
    ( 'refuse_pct', ndecimal ),
    ( 'scientific_name', nunicode ),
    ( 'nitrogen_factor', ndecimal ), 
    ( 'protein_factor', ndecimal ), 
    ( 'fat_factor', ndecimal ), 
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
    ( 'quantity', Decimal ),
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
    ( 'nutrient_source_id', int ), # FK to the nutrient sources table.
    ( 'nutrient_derivation_id', nunicode ),  #FK to derivation tables.
    ( 'reference_food_item_id', nunicode ), # NOTE - NOT USED - OUR APP HAS NO USE FOR PROVENANCE INFORMATION OF NUTRITION VALUES LIKE THIS.
    ( 'is_fortified', y2b ),
    ( 'studies', nint ),
    ( 'min_value', ndecimal ),
    ( 'max_value', ndecimal ),
    ( 'freedom_degrees', nint ),
    ( 'lower_error_bound', ndecimal ),
    ( 'upper_error_bound', ndecimal ),
    ( 'stat_comments', nunicode ),
    ( 'updated_date', ndate_handler ), 
    ( 'confidence_code', nunicode ) # NOT USED
]    

nutrient_data_definitions = [
    ( 'derivation_id', unicode ),
    ( 'derivation_desc', unicode )
]

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
        'import_order' : 9,
        'pk' : [ 'citation_id' ],
        'pk_idx' : [ 0 ]
    },
    { 
        'name' : 'NutrientCitationsLink',
        'filename' : 'DATSRCLN.txt',
        'columns' : citation_link_fields,
        'import_order' : 10,
        'pk' : [ 'ndb_id', 'nutrient_id', 'citation_id' ],
        'pk_idx' : [ 0, 1, 2 ]
    },
    { 
        'name' : 'NutrientDerivations',
        'filename' : 'DERIV_CD.txt',
        'columns' : nutrient_data_definitions,
        'import_order' : 1,
        'pk' : [ 'derivation_id' ],
        'pk_idx' : [ 0 ]
    },
    { 
        'name' : 'FoodGroups',
        'filename' : 'FD_GROUP.txt',
        'columns' : food_group_desc_fields,
        'import_order' : 2,
        'pk' : [ 'food_group_id' ],
        'pk_idx' : [ 0 ]
    },
    { 
        'name' : 'FoodItems',
        'filename' : 'FOOD_DES.txt',
        'columns' : food_desc_fields,
        'import_order' : 3,
        'pk' : [ 'ndb_id' ],
        'pk_idx' : [ 0 ]
    },
    { 
        'name' : 'Footnotes',
        'filename' : 'FOOTNOTE.txt',
        'columns' : footnote_fields,
        'import_order' : 8,
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
        'import_order' : 7,
        'pk' : [ 'ndb_id', 'nutrient_id' ],
        'pk_idx' : [ 0, 1 ]
    },
    { 
        'name' : 'FoodItemNutrientDefinition',
        'filename' : 'NUTR_DEF.txt',
        'columns' : nutrient_definition_fields,
        'import_order' : 6.5,
        'pk' : [ 'nutrient_id' ],
        'pk_idx' : [ 0 ]
    },
    { 
        'name' : 'NutrientSources',
        'filename' : 'SRC_CD.txt',
        'columns' : nutrient_sources,
        'import_order' : 0,
        'pk' : [ 'id' ],
        'pk_idx' : [ 0 ]
    },
    { 
        'name' : 'FoodItemServingSizes',
        'filename' : 'WEIGHT.txt',
        'columns' : weight_fields,
        'import_order' : 6,
        'pk' : [ 'ndb_id', 'sequence' ],
        'pk_idx' : [ 0, 1 ]
    },
]

data = {}
database = {}

for df in sorted( files, key=lambda x: x['import_order'] ):
    filename = "%s%s" % ( data_dir, df['filename'] )
    columns = df['columns']
    name = df['name']
    pk_idx = df['pk_idx']

    print "Working on %s - %s" % ( filename, name )
    if not os.path.exists( "%s" % ( filename ) ):
        raise Exception( "Couldn't find file: %s" % ( filename ) )
        
    f = open( filename, mode='r' )
    
    count = 1

    for line in f:
        line = unicode( line.decode( 'latin1' ) )

        # Skip blank lines.
        if re.search( u'^\s*$', line ):
            continue

        line = line.rstrip( "\n" )

        count += 1
        if count % 1000 == 0:
            print "Working on:", line

        column_data = line.split( '^' )
        if ( len( column_data ) != len( columns ) ):
            raise Exception( "Malformed line found, had %d columns, expected %d, line was: '%s'" %  ( len( column_data ), len( columns ), line ) )
        
        column_fields = []
                
        for col_no, field in enumerate( column_data ):
            field = field.strip( '~' )
            field_data = columns[col_no][1]( field )
            column_fields.append( field_data )
            #print "Column %s: %s -> %s" % ( columns[col_no][0], field, field_data )
            
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
        if name == 'NutrientSources':
            ns = NutrientSources.objects.create( nutrient_source_id = column_fields[0],
                                                 source_desc = column_fields[1] )
            if name in database:
                database[name][ns.nutrient_source_id] = ns
            else:
                database[name] = { ns.nutrient_source_id : ns }

        elif name == 'NutrientDerivations':
            nd = NutrientDerivations.objects.create( derivation_id = column_fields[0],
                                                     derivation_desc = column_fields[1] )
            if name in database:
                database[name][nd.derivation_id] = nd
            else:
                database[name] = { nd.derivation_id : nd }

        elif name == 'FoodItems':
            food_group = data['FoodGroups'][column_fields[1]]

            fi = FoodItems.objects.create( uid = str( uuid.uuid4() ),
                                           ndb_id = column_fields[0],
                                           food_group_id = column_fields[1],
                                           food_group_desc = food_group[1],
                                           long_desc = column_fields[2],
                                           short_desc = column_fields[3],
                                           common_name = column_fields[4],
                                           manufacturer = column_fields[5],
                                           is_fndds = column_fields[6],
                                           refuse_desc = column_fields[7],
                                           refuse_pct = column_fields[8],
                                           scientific_name = column_fields[9],
                                           nitrogen_factor = column_fields[10],
                                           protein_factor = column_fields[11],
                                           fat_factor = column_fields[12],
                                           carb_factor = column_fields[13] )

            if name in database:
                database[name][fi.ndb_id] = fi
            else:
                database[name] = { fi.ndb_id : fi }
            
        elif name == 'LanguaLLink':
            ndb_id = column_fields[0]
            langual_code = column_fields[1]
            langual_desc = data['LanguaLDesc'][langual_code][1]
            fi = database['FoodItems'][ndb_id]

            fild = FoodItemLanguaLDesc.objects.create( food_item_id = fi,
                                                       langual_id = langual_code,
                                                       langual_desc = langual_desc )

        elif name == 'FoodItemServingSizes':
            ndb_id = column_fields[0]
            fi = database['FoodItems'][ndb_id]

            fiss = FoodItemServingSizes.objects.create( food_item_id = fi,
                                                        quantity = column_fields[2],
                                                        unit = column_fields[3],
                                                        grams = column_fields[4],
                                                        data_points = column_fields[5],
                                                        std_dev = column_fields[6] )

        elif name == 'FoodItemNutrients':
            ndb_id = column_fields[0]
            nutrient_id = column_fields[1]
            fi = database['FoodItems'][ndb_id]

            find = data['FoodItemNutrientDefinition'][nutrient_id]

            unit = find[1]

            if unit == 'kJ':
                # We don't keep the redundant kJ and kcal information.
                continue

            nutrient_conversion_factors = {
                'g' : Decimal( '.01' ),
                'mg' : Decimal( '.00001' ),
                'ug' : Decimal( '.00000001' ),
                'IU' : Decimal( '.01' ),
                'kcal' : Decimal( '.01' )
            }

            amount = nutrient_conversion_factors[unit] * column_fields[2]
            
            nutrient_source_id = column_fields[5]
            nutrient_derivation_id = column_fields[6]
            ns = database['NutrientSources'][nutrient_source_id]

            nd = None
            if nutrient_derivation_id in database['NutrientDerivations']:
                nd = database['NutrientDerivations'][nutrient_derivation_id]

            fin = FoodItemNutrients.objects.create( food_item_id = fi,
                                                    nutrient_id = nutrient_id,
                                                    unit = find[1],
                                                    infoods_tag = find[2],
                                                    nutrient = find[3],
                                                    sort_order = find[5],
                                                    amount = amount,
                                                    data_points = column_fields[3],
                                                    std_err = column_fields[4],
                                                    nutrient_source_id = ns,
                                                    nutrient_derivation_id = nd,
                                                    is_fortified = column_fields[8],
                                                    studies = column_fields[9],
                                                    min_value = column_fields[10],
                                                    max_value = column_fields[11],
                                                    freedom_degrees = column_fields[12],
                                                    lower_error_bound = column_fields[13],
                                                    upper_error_bound = column_fields[14],
                                                    stat_comments = column_fields[15],
                                                    updated_date = column_fields[16] )

            if name in database:
                if ndb_id in database[name]:
                    database[name][ndb_id][nutrient_id] = fin
                else:
                    database[name][ndb_id] = { nutrient_id : fin }
            else:
                database[name] = { ndb_id : { nutrient_id : fin } }

        elif name == 'Footnotes':
            ndb_id = column_fields[0]
            nutrient_id = column_fields[3]

            fi = None
            fin = None

            if nutrient_id is not None:
                if nutrient_id not in database['FoodItemNutrients'][ndb_id]:
                    # A few oddball foodnotes pertain to a nutrient on
                    # a food item where that nutrient is not
                    # explicitly listed for the food item.
                    #
                    # In that case just put the note on the food item.
                    fi = database['FoodItems'][ndb_id]
                else:
                    fin = database['FoodItemNutrients'][ndb_id][nutrient_id]
            else:
                fi = database['FoodItems'][ndb_id]
                
            fo = Footnotes.objects.create( food_item_id = fi,
                                           food_item_nutrient_id = fin,
                                           footnote_number = column_fields[1],
                                           footnote_type = column_fields[2],
                                           footnote = column_fields[4] )
                                   
        elif name == 'NutrientCitationsLink':
            ndb_id = column_fields[0]
            nutrient_id = column_fields[1]
            citation_id = column_fields[2]

            fin = database['FoodItemNutrients'][ndb_id][nutrient_id]
            #fin = FoodItemNutrients.objects.get( pk = database['FoodItemNutrients'][ndb_id][nutrient_id] )
            cf = data['NutrientCitations'][citation_id]

            nc = NutrientCitations.objects.create( food_item_nutrient_id = fin,
                                                   authors = cf[1],
                                                   title = cf[2],
                                                   year = cf[3],
                                                   journal = cf[4],
                                                   volume = cf[5],
                                                   issue = cf[6],
                                                   start_page = cf[7],
                                                   end_page = cf[8] )


'''
class FoodItems( models.Model ):
class FoodItemServingSizes( models.Model ):
class NutrientSources( models.Model ):
class NutrientDerivations( models.Model ):
class FoodItemNutrients( models.Model ):
class Footnotes( models.Model ):
class NutrientCitations( models.Model ):

Order:
NutrientSources
NutrientDerivations

FoodGroups
LanguaL stuff
FoodItems
FoodItemServingSizes

FoodItemNutrients

Footnotes

NutrientCitations

'''

#pp = pprint.PrettyPrinter( indent=4 )

#pp.pprint( data )
