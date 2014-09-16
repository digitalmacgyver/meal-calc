food_group_desc_fields = [
    'food_group_id',
    'food_group_desc'
]

food_desc_fields = [
    'ndb_id',
    'long_desc',
    'common_name',
    'manufacturer',
    'is_fndds', # MUST CONVERT O BOOLEAN
    'refuse_desc',
    'scientific_name',
    'nitrogen_factor', # CONVERT to 4.2 DECIMAL, SAME FOR NEXT THREE
    'protien_factor', # CONVERT
    'fat_factor', # convert
]

langual_factor_fields = [
    'ndb_id',
    'langual_code'
]

langual_factor_desc_fields = [
    'langual_code',
    'langual_desc'
]

weight_fields = [
    'ndb_id' # The FK into food_desc_fields
    'sequence', # Not used.
    'quantity', # N 5.3
    'unit',
    'grams',
    'data_points',
    'std_dev'
]

nutrient_sources = [
    'id', # NOTE - we must explicitly set this to ensure consistency.
    'source_desc'
]

nutrient_fields = [
    'ndb_id', # FK
    'nutrient_id',
    'amount', # NOTE - THIS MUST BE MODIFIED BY THE UNIT IN NUTRIENT_DEFINITION, AND DIVIDED BY 100.
    'data_points',
    'std_err',
    'source_id', # FK to the nutrient sources table.
    'reference_food_item_id', # NOTE - NOT USED - OUR APP HAS NO USE FOR PROVENANCE INFORMATION OF NUTRITION VALUES LIKE THIS.
    'is_fortified', # NOTE - MUST CONVERT FROM Y/N to BOOLEAN
    'studies',
    'min_value',
    'max_value',
    'freedom_degrees',
    'lower_error_bound',
    'upper_error_bound',
    'stat_comments',
    'updated_date', # NOTE - WE MUST EXPLICITLY SET TIS ONE TO NULL OR IT WILL PICK UP THE DEFAULT OF NOW.
    'confidence_code', # NOT USED
]    

nutrient_data_definitions = [
    'derivation_id',
    'derivation_desc'
]

from decimal import *

nutrient_conversion_factors = {
    'g' : Decimal( '.01' )
    'mg' : Decimal( '.00001' )
    'ug' : Decimal( '.00000001' )
    'UI' : Decimal( '.01' )
    'kcal' : Decimal( '.01' )
}

nutrient_definition_fields = [
    'nutrient_id',
    'unit', # NOTE - ALL UNITS EXCEPT kcal and UI are converted into g
    # FURTHER NOTE, any kJ items are to be excluded.
    'infoods_tag',
    'nutrient',
    'decimal_places', # Not used.
    'sort_order'
]

footnote_fields = [
    'ndb_id', # FK to nutrients
    'footnote_number',
    'footnote_type',
    'nutrient_id' # FK to nutrients,
    'footnote'
]

citation_link_fields = [
    'ndb_id', # Part of composite FK to food_item_nutrients
    'nutrient_id', # Other part of composite key
    'citation_id' # Not used, but FK to citations.
]

citation_fields = [
    'citation_id',
    'authors',
    'title',
    'year',
    'journal',
    'volume',
    'issue',
    'start_page',
    'end_page'
]

FoodItems = [
    'uid'
]

FoodItems += food_desc_fields + food_group_desc_fields + langual_factor_desc_fields

# Add to food items.
FoodItemServingSizes = [ weight_fields[2:] ]

FoodItemNutrients = DEBUG

    x = models.CharField( "",
                          max_length = x,
                          help_text = "",
                          null = True,
                          blank = True,
                          default = None )

    n = models.DecimalField( "",
                            max_digits = 2,
                            decimal_places = 0,
                            help_text = "",
                            null = True,
                            blank = True,
                            default = None )
