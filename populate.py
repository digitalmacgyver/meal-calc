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

    
]

FoodItems = [
    'uid'
]
FoodItems += food_desc_fields + food_group_desc_fields


n= models.DecimalField( "",
                        max_digits = 2,
                        decimal_places = 0,
                        help_text = "",
                        null = True,
                        blank = True )
