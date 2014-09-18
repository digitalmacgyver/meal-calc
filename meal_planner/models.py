import datetime
from django.db import models

class FoodItems( models.Model ):
    uid = models.CharField( "Food Item UUID",
                            max_length = 36,
                            help_text = "Food Item UUID",
                            unique = True )

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
                                    blank = True,
                                    default = None )

    manufacturer = models.CharField( "Manufacturer",
                          max_length = 65,
                          help_text = "The manufacturer of this food item.",
                          null = True,
                          blank = True,
                          default = None )

    is_fndds = models.BooleanField( "Is In USDA FNDDS Database",
                                    default = False,
                                    help_text = "Whether this food item is in the USDA Food and Nutrient Database for Dietary Studies (FNDDS)" )
    
    refuse_desc = models.CharField( "Description of Inedible Parts",
                                    max_length = 135,
                                    help_text = "Description of inedible parts of food item, such as seeds or bone.",
                                    null = True,
                                    blank = True,
                                    default = None )

    refuse_pct = models.DecimalField( "Percentage of Inedible Parts",
                                      max_digits = 2,
                                      decimal_places = 0,
                                      help_text = "Percentage of inedible parts of food item.",
                                      null = True,
                                      blank = True,
                                      default = None )
                                      
    scientific_name = models.CharField( "Scientific Name",
                                        max_length = 65,
                                        help_text = "Scientific name - given for least processed form of the food item.",
                                        null = True,
                                        blank = True,
                                        default = None )
    
    nitrogen_factor = models.DecimalField( "Nitrogen Factor",
                                           max_digits = 4,
                                           decimal_places = 2,
                                           help_text = "Factor for converting nitrogen to protein",
                                           null = True,
                                           blank = True,
                                           default = None )

    protein_factor = models.DecimalField( "Protein Factor",
                                          max_digits = 4,
                                          decimal_places = 2,
                                          help_text = "Factor for calculating calories from protein.",
                                          null = True,
                                          blank = True,
                                          default = None )

    fat_factor = models.DecimalField( "Fat Factor",
                        max_digits = 4,
                        decimal_places = 2,
                        help_text = "Factor for calculating calories from fat.",
                        null = True,
                        blank = True,
                        default = None )

    carb_factor = models.DecimalField( "Carbohydrate Factor",
                                       max_digits = 4,
                                       decimal_places = 2,
                                       help_text = "Factor for calculating calories from carbohydrate.",
                                       null = True,
                                       blank = True,
                                       default = None )

    def __unicode__( self ):
        return self.long_desc

    # There is probably a better way to do this, using _meta, but
    # we"ll pass on that for the time being.
    #
    # Replace empty strings with null.
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith("_"):
                if self.__dict__[var] == "":
                    self.__dict__[var] = None
        super( FoodItems, self ).save( *args, **kwargs )

    class Meta( object ):
        ordering = [ "ndb_id" ]
        verbose_name = 'Food Item'
        verbose_name_plural = 'Food Items'


class FoodItemLanguaLDesc( models.Model ):
    food_item_id = models.ForeignKey( FoodItems, 
                                      verbose_name="FoodItem ID",
                                      help_text = "The database ID of the food item this LanguaL description pertains to." )

    langual_id = models.CharField( "LanguaL Food Thesaurus ID",
                          max_length = 5,
                          help_text = "The LanguaL food description thesaurus ID." )

    langual_desc = models.CharField( "LanguaL Description",
                          max_length = 140,
                          help_text = "The description of this food item from the LanguaL food description thesaurus." )

    def __unicode__( self ):
        return self.langual_desc

    # There is probably a better way to do this, using _meta, but
    # we"ll pass on that for the time being.
    #
    # Replace empty strings with null.
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith("_"):
                if self.__dict__[var] == "":
                    self.__dict__[var] = None
        super( FoodItemLanguaLDesc, self ).save( *args, **kwargs )

    class Meta( object ):
        verbose_name = 'Food Item LanguaL Description'
        verbose_name_plural = 'Food Item LanguaL Descriptions'


class FoodItemServingSizes( models.Model ):
    food_item_id = models.ForeignKey( FoodItems, 
                                      verbose_name="FoodItem ID",
                                      help_text = "The database ID of the food item this serving size pertains to." )

    quantity = models.DecimalField( "Quantity",
                                    max_digits = 5,
                                    decimal_places = 3,
                                    help_text = "The number of units (e.g. 1 in 1 cup)." )

    unit = models.CharField( "Unit",
                          max_length = 84,
                          help_text = "The unit to which quantity pertains (e.g. cup in 1 cup)." )

    grams = models.DecimalField( "Grams",
                            max_digits = 7,
                            decimal_places = 1,
                            help_text = "Weight in grams." )

    data_points = models.PositiveIntegerField( "Number of Data Points",
                                               help_text = "Number of data points.",
                                               null = True,
                                               blank = True,
                                               default = None )

    std_dev = models.DecimalField( "Standard Deviation",
                            max_digits = 7,
                            decimal_places = 3,
                            help_text = "Standard deviation in the data points.",
                            null = True,
                            blank = True,
                            default = None )


    def __unicode__( self ):
        return "%7.1f grams - %5.3f %s" % ( self.grams, self.quantity, self.unit )

    # There is probably a better way to do this, using _meta, but
    # we"ll pass on that for the time being.
    #
    # Replace empty strings with null.
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith("_"):
                if self.__dict__[var] == "":
                    self.__dict__[var] = None
        super( FoodItemServingSizes, self ).save( *args, **kwargs )

    class Meta( object ):
        verbose_name = 'Food Item Serving Size'
        verbose_name_plural = 'Food Item Serving Sizes'


class NutrientSources( models.Model ):
    '''NOTE: We explicitly set and manage the PK of this class to be
    nutrient_source_id to maintain the same values as are present in
    the USDA NNDS SR 27.
    '''
    nutrient_source_id = models.PositiveIntegerField( "Nutrient Source ID", 
                                                      primary_key = True,
                                                      help_text = "The nutrient source ID from the USDA NNDS SR 27." )
    
    
    source_desc = models.CharField( "Source Description",
                                    max_length = 60,
                                    help_text = "Nutrient source description from the USDA NNDS SR 27." )

    def __unicode__( self ):
        return self.source_desc

    # There is probably a better way to do this, using _meta, but
    # we"ll pass on that for the time being.
    #
    # Replace empty strings with null.
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith("_"):
                if self.__dict__[var] == "":
                    self.__dict__[var] = None
        super( NutrientSources, self ).save( *args, **kwargs )

    class Meta( object ):
        ordering = [ "nutrient_source_id" ]
        verbose_name = 'Nutrient Source'
        verbose_name_plural = 'Nutrient Sources'


class NutrientDerivations( models.Model ):
    derivation_id = models.CharField( "Nutrient Derivation ID", 
                                      max_length = 4,
                                      help_text = "The data derivation ID from the USDA NNDS SR 27." )
    
    derivation_desc = models.CharField( "Source Description",
                                    max_length = 120,
                                    help_text = "How were the values in the nutrient determined." )

    def __unicode__( self ):
        return self.derivation_desc

    # There is probably a better way to do this, using _meta, but
    # we"ll pass on that for the time being.
    #
    # Replace empty strings with null.
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith("_"):
                if self.__dict__[var] == "":
                    self.__dict__[var] = None
        super( NutrientDerivations, self ).save( *args, **kwargs )

    class Meta( object ):
        verbose_name = 'Nutrient Derivation'
        verbose_name_plural = 'Nutrient Derivations'

class FoodItemNutrients( models.Model ):
    food_item_id = models.ForeignKey( FoodItems,
                                      verbose_name = "FoodItem ID",
                                      help_text = "The database ID of the food item this nutrient is associated with." )

    nutrient_id = models.CharField( "Nutrient ID",
                          max_length = 3,
                          help_text = "Unique 3-digit identifier for a nutrient." )

    # These columns denormalized
    unit_choices = ( 
        ( 'g', 'Grams' ),
        ( 'mg', 'Milligrams' ),
        ( 'ug', 'Micrograms' ),
        ( 'IU', 'International unit' ),
        ( 'kcal', 'Kilocalorie' )
    )

    unit = models.CharField( "Unit",
                             max_length = 7,
                             help_text = "Nutrient unit (e.g. kcal, IU, g).",
                             choices = unit_choices )


    infoods_tag = models.CharField( "INFOODS Tagname",
                                    max_length = 20,
                                    help_text = "International Network of Food Data Systems (INFOODS) Tagname.",
                                    null = True,
                                    blank = True,
                                    default = None )

    nutrient = models.CharField( "Nutrient",
                                 max_length = 60,
                                 help_text = "Name of the nutrient/food component." )

    sort_order = models.IntegerField( "Sort Order",
                                      help_text = "The order to display this nutrient in to be consistent with various USDA reports." )
    # End denormalization
    
    amount = models.DecimalField( "Amount of Nutrient in 1 g of Food Item",
                                  max_digits = 18,
                                  decimal_places = 11,
                                  help_text = "Amount of nutrient in 1 edible gram of a food item." )

    data_points = models.PositiveIntegerField( "Number of Data Points",
                                               help_text = "Number of analyses used to calculate nutrient value.  If zero, then the value was calculated or imputed." )

    std_err = models.DecimalField( "Standard Error",
                                   max_digits = 8,
                                   decimal_places = 3,
                                   help_text = "Standard error, null if the error can not be calculated or if fewer than three data points.",
                                   null = True,
                                   blank = True,
                                   default = None )

    nutrient_source_id = models.ForeignKey( NutrientSources,
                                            verbose_name = "Nutrient Source ID",
                                            help_text = "The database ID of the nutrient source for this FoodItem Nutrient." )

    nutrient_derivation_id = models.ForeignKey( NutrientDerivations,
                                                verbose_name = "Nutrient Derivation ID",
                                                help_text = "The database ID of how this nutrient data was derived.",
                                                null = True,
                                                blank = True,
                                                default = None )

    is_fortified = models.BooleanField( "Is Fortified",
                                        default = False,
                                        help_text = "Indicates that this nutrient was added for fortification or enrichment." )

    studies = models.PositiveIntegerField( "Number of Studies",
                                           help_text = "Number of studies.",
                                           null = True,
                                           blank = True,
                                           default = None )

    min_value = models.DecimalField( "Minimum Value",
                                     max_digits = 10,
                                     decimal_places = 3,
                                     help_text = "Minimum value.",
                                     null = True,
                                     blank = True,
                                     default = None )

    max_value = models.DecimalField( "Maximum Value",
                                     max_digits = 10,
                                     decimal_places = 3,
                                     help_text = "Maximum value.",
                                     null = True,
                                     blank = True,
                                     default = None )

    freedom_degrees = models.PositiveIntegerField( "Degrees of Freedom",
                                                   help_text = "Degrees of freedom.",
                                                   null = True,
                                                   blank = True,
                                                   default = None )
                                                   
    lower_error_bound = models.DecimalField( "Lower Error Bound",
                                             max_digits = 10,
                                             decimal_places = 3,
                                             help_text = "Lower 95% error bound.",
                                             null = True,
                                             blank = True,
                                             default = None )

    upper_error_bound = models.DecimalField( "Upper Error Bound",
                                             max_digits = 10,
                                             decimal_places = 3,
                                             help_text = "Upper 95% error bound.",
                                             null = True,
                                             blank = True,
                                             default = None )

    stat_comments = models.CharField( "Statistical Comments",
                                      max_length = 10,
                                      help_text = "Statistical comments.",
                                      null = True,
                                      blank = True,
                                      default = None )
    updated_date = models.DateField( "Updated Date",
                          help_text = "When this value was added or last modified.",
                          null = True,
                          blank = True )

    def __unicode__( self ):
        return "FoodItem: %d has %f grams of %s per edible gram" % ( self.food_item_id.pk, self.amount, self.nutrient )

    # There is probably a better way to do this, using _meta, but
    # we"ll pass on that for the time being.
    #
    # Replace empty strings with null.
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith("_"):
                if self.__dict__[var] == "":
                    self.__dict__[var] = None
        super( FoodItemNutrients, self ).save( *args, **kwargs )

    class Meta( object ):
        ordering = [ "sort_order" ]
        unique_together = ( ( 'food_item_id', 'nutrient_id' ) )
        verbose_name = 'Food Item Nutrient'
        verbose_name_plural = 'Food Item Nutrients'

class Footnotes( models.Model ):
    food_item_id = models.ForeignKey( FoodItems, 
                                      verbose_name = "FoodItem ID",
                                      help_text = "The database ID of the food item this footnote pertains to.",
                                      null = True,
                                      blank = True,
                                      default = None )

    food_item_nutrient_id = models.ForeignKey( FoodItemNutrients, 
                                               verbose_name = "FoodItemNutrient ID",
                                               help_text = "The database ID of the food item nutrient this footnote pertains to.",
                                               null = True,
                                               blank = True,
                                               default = None )
    
    footnote_number = models.PositiveIntegerField( "Footnote Number",
                                                   help_text = "The number associated with this footnote." )

    footnote_type_choices = (
        ( "D", "Description" ),
        ( "M", "Measure" ),
        ( "N", "Nutrient" )
        )

    footnote_type = models.CharField( "Footnote Type",
                                      max_length = 1,
                                      help_text = "Footnote type: D - food description, M - measure description, N - nutrient value.",
                                      choices = footnote_type_choices )

    footnote = models.CharField( "Footnote",
                                 max_length = 200,
                                 help_text = "Footnote." )

    def __unicode__( self ):
        return self.footnote

    # There is probably a better way to do this, using _meta, but
    # we"ll pass on that for the time being.
    #
    # Replace empty strings with null.
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith("_"):
                if self.__dict__[var] == "":
                    self.__dict__[var] = None
        super( Footnotes, self ).save( *args, **kwargs )

    class Meta( object ):
        ordering = [ "footnote_number" ]
        verbose_name = 'Footnote'
        verbose_name_plural = 'Footnotes'


class NutrientCitations( models.Model ):
    food_item_nutrient_id = models.ForeignKey( FoodItemNutrients, 
                                               verbose_name = "FoodItemNutrient ID",
                                               help_text = "The database ID of the food item nutrient this footnote pertains to." )

    authors = models.CharField( "Authors",
                                max_length = 255,
                                help_text = "Authors.",
                                null = True,
                                blank = True,
                                default = None )

    title = models.CharField( "Title",
                              max_length = 255,
                              help_text = "Title." )

    year = models.CharField( "Year",
                             max_length = 4,
                             help_text = "Year.",
                             null = True,
                             blank = True,
                             default = None )

    journal = models.CharField( "Journal",
                                max_length = 135,
                                help_text = "Journal.",
                                null = True,
                                blank = True,
                                default = None )

    volume = models.CharField( "Volume or City",
                               max_length = 16,
                               help_text = "Volume number of journals, city for events.",
                               null = True,
                               blank = True,
                               default = None )

    issue = models.CharField( "Issue or State",
                              max_length = 5,
                              help_text = "Issue number for journals, State for events.",
                              null = True,
                              blank = True,
                              default = None )

    start_page = models.PositiveIntegerField( "Start Page",
                                              help_text = "Start page of article.",
                                              null = True,
                                              blank = True,
                                              default = None )

    end_page = models.PositiveIntegerField( "End Page",
                                              help_text = "End page of article.",
                                              null = True,
                                              blank = True,
                                              default = None )

    def __unicode__( self ):
        return "Authors: %s, '%s', %s, %s" % ( self.authors, self.title, self.journal, self.year )

    # There is probably a better way to do this, using _meta, but
    # we"ll pass on that for the time being.
    #
    # Replace empty strings with null.
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith("_"):
                if self.__dict__[var] == "":
                    self.__dict__[var] = None
        super( NutrientCitations, self ).save( *args, **kwargs )

    class Meta( object ):
        verbose_name = 'Nutrient Citation'
        verbose_name_plural = 'Nutrient Citations'

