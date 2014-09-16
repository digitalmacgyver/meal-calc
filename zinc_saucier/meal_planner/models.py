from django.db import models

class FoodItems( models.Model ):
    uid = models.CharField( "Food Item UUID",
                            max_length = 36,
                            help_text = "Food Item UUID" )

    ndb_id = models.CharField( "Nutrient Database ID", 
                               max_length = 5, 
                               help_text = "The 5-digit Nutrient Databank identifier of this food item.",
                               unique = True )

    food_group_id = models.CharField( "Food Group Code",
                                      max_length = 4,
                                      help_text = "The 4-digit food group code - currently only the first two digits are used." )

    food_group_desc = models.CharField( "Food Group Description",
                                        max_length = 60,
                                        help_text = "Food Group Description" )

    long_desc = models.CharField( "Long Description",
                                  max_length = 200,
                                  help_text = "200-character description of food item." )

    short_desc = models.CharField( "Short Description",
                                   max_length = 60,
                                   help_text = "60-character description of food item." )

    common_name = models.CharField( "Common Name",
                                    max_length = 100,
                                    help_text = "Common name",
                                    null = True,
                                    blank = True )

    manufacturer = models.CharField( "Manufacturer",
                          max_length = 65,
                          help_text = "The manufacturer of this food item.",
                          null = True,
                          blank = True )

    is_fndds = models.BooleanField( "Is In USDA FNDDS Database",
                                    default = False,
                                    help_text = "Whether this food item is in the USDA Food and Nutrient Database for Dietary Studies (FNDDS)" )
    
    refuse_desc = models.CharField( "Description of Inedible Parts",
                                    max_length = 125,
                                    help_text = "Description of inedible parts of food item, such as seeds or bone.",
                                    null = True,
                                    blank = True )

    refuse_pct = models.DecimalField( "Percentage of Inedible Parts",
                                      max_digits = 2,
                                      decimal_places = 0,
                                      help_text = "Percentage of inedible parts of food item.",
                                      null = True,
                                      blank = True )
                                      
    scientific_name = models.CharField( "Scientific Name",
                                        max_length = 65,
                                        help_text = "Scientific name - given for least processed form of the food item.",
                                        null = True,
                                        blank = True )
    
    nitrogen_factor = models.DecimalField( "Nitrogen Factor",
                                           max_digits = 6,
                                           decimal_places = 2,
                                           help_text = "Factor for converting nitrogen to protein",
                                           null = True,
                                           blank = True )

    protein_factor = models.DecimalField( "Protein Factor",
                                          max_digits = 6,
                                          decimal_places = 2,
                                          help_text = "Factor for calculating calories from protein.",
                                          null = True,
                                          blank = True )

    fat_factor = models.DecimalField( "Fat Factor",
                        max_digits = 6,
                        decimal_places = 2,
                        help_text = "Factor for calculating calories from fat.",
                        null = True,
                        blank = True )

    carb_factor = models.DecimalField( "Carbohydrate Factor",
                                       max_digits = 6,
                                       decimal_places = 2,
                                       help_text = "Factor for calculating calories from carbohydrate.",
                                       null = True,
                                       blank = True )

    langual_id = models.CharField( "LanguaL Food Thesaurus ID",
                          max_length = 5,
                          help_text = "The LanguaL food description thesaurus ID.",
                          null = True,
                          blank = True )

    langual_desc = models.CharField( "LanguaL Description",
                          max_length = 140,
                          help_text = "The description of this food item from the LanguaL food description thesaurus.",
                          null = True,
                          blank = True )

    def __unicode__( self ):
        return self.long_desc

    # DEBUG - can we find out the null attribute of the thing here?

    # Replace empty strings with null.
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(MyModel, self).save(*args, **kwargs)

    class Meta:
        pass
        '''unique_together, index_together, ordering'''


