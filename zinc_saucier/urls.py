from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns( '',
                        # Examples:
                        # url(r'^$', 'zinc_saucier.views.home', name='home'),
                        # url(r'^blog/', include('blog.urls')),

                        url( r'^mp/', include( 'meal_planner.urls' ) ),
                        url(r'^admin/', include(admin.site.urls)),
                         )

