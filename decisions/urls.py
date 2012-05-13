__author__ = 'ben'
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'datadriven.views.home', name='home'),
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'base.html'}),
    (r'^index.html$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    (r'^maps/$', 'django.views.generic.simple.direct_to_template', {'template': 'map.html'}),
    (r'^google/', 'decisions.views.google_maps'),

    url(r'^rank/$', 'decisions.views.rank_locations'),
    url(r'^county.json$', 'decisions.views.location_list'),



    #url(r'^decisions/', include('datadriven.decisions.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)