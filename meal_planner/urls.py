from django.conf.urls import patterns, url

from meal_planner import views

urlpatterns = patterns( '',
                        url( r'^$', views.index, name='index' ),
                        url( r'^fi/(?P<food_item_id>\d+)/$', views.food_item, name='food_item' ),
                        url( r'^fin/(?P<food_item_nutrient_id>\d+)/$', views.nutrient, name='food_item_nutrient' ),
                        url( r'^planner/$', views.planner, name='planner' ),
                        url( r'^hwaj/', views.hwaj, name='hwaj' ),
                        url( r'^hw/$', views.hw, name='hw' )
)

