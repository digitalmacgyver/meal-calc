from django import forms

class MealForm( forms.Form ):
    '''
    forms.Field arguments:
    required=True|False
    label='Blah blah blah'
    initial=default value
    widget = the Widget class to use when rendering this field
    help_text = 'blah blah'
    error_messages = { 'required' : 'MUST HAVE', 'error 2' : 'Not allowed' }
    
    Field types:
    BooleanField
    CharField
    ChoiceField - choices, an iterable of 2-tuples ( "VALUE", "NAME" )
    DecimalField - max_value, min_value
    FloatField - max_value, min_value
    IntegerField - max_value, min_value
    
    '''

    def __init__( self, *args, **kwargs ):
        calories = kwargs.pop( 'calories', None )
        if 'selected_foods' in kwargs:
            selected_foods = kwargs.pop( 'selected_foods' )
        else:
            selected_foods = { k[15:] : kwargs[k] for k in kwargs.keys() if k.startswith( 'selected_foods_' ) }
            for selected_food in selected_foods.keys():
                kwargs.pop( 'selected_foods_%s' % ( selected_food ) )

        food_group = kwargs.pop( 'food_group', None )
        food_choices = kwargs.pop( 'food_choices', None )

        super( MealForm, self ).__init__( *args, **kwargs )

        if selected_foods is not None:
            for food_item_uid, food_item_name in selected_foods.items():
                self.fields[ "selected_foods_%s" % ( food_item_uid ) ] = forms.CharField( initial=food_item_name,
                                                                                     widget=forms.HiddenInput() )

        if food_choices is not None:
            self.fields[ 'food_choices' ] = forms.ChoiceField( food_choices )

        if calories is None:
            self.fields[ 'calories' ] = forms.IntegerField( min_value = 0, max_value = 10000 )
        else:
            self.fields[ 'calories' ] = forms.IntegerField( initial = calories,
                                                            widget = forms.HiddenInput() )

        self.fields['food_group'] = forms.CharField( initial=food_group, 
                                                     widget=forms.HiddenInput() )
            
        
