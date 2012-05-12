# Create your views here.

from django.shortcuts import render
import urllib2
import json
from models import County


def rank_locations(request):
    # Parse the JSON
    objs = json.loads(request.POST)
    data = []
    for address in objs.get('addresses', []):
        try:
            location = 'POINT(' + address['location'].replace(',', '') + ')'
            county = County.objects.get(mpoly__contains=location)
            data.append(county)
        except Exception as e:
            print e



    #    {
    #    "addresses": [
    #            {
    #            "address": "dfgdf",
    #            "location": "-71, 42"
    #        }
    #    ],
    #    "slider1": 3,
    #    "slider2": 3,
    #    "slider3": 3,
    #    "slider4": 3
    #}






    pass


def google_maps(request):

    get_str = request.GET

    print get_str
    print "meta req: \n", request.META.get('QUERY_STRING', '')
    #print "req:", request
    post_string = "http://maps.google.com/maps/geo?output=csv&q=blah"
    result = urllib2.urlopen(post_string).read()
    print "result:"
    print result
    return render(request, "base.html")

    pass