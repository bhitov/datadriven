# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render
import urllib2
import json
from django.views.decorators.csrf import csrf_exempt
from models import County
from django.core import serializers
from django.contrib.gis.geos import Polygon


def location_list(request):
    # figure out bounding box
    bbox = request.GET['bbox'].split(',')
    poly = Polygon.from_bbox(bbox)

    # fetch counties
    counties = County.objects.filter(mpoly__intersects=poly)
    print "found counties:", counties

    # convert to geojson
    geojson_dict = {
        "type" : "FeatureCollection",
        "features": [county_to_geojson(county) for county in counties],
    }

#    print geojson_dict

    # return response
    return HttpResponse(json.dumps(geojson_dict),
                            content_type='application/json')

    pass

def county_to_geojson(county):
    # poor_health_days num_pcps air_pol recfac foodhealth
    geojson_dict =  {
        "type" : "Feature",
        "geometry" : json.loads(county.mpoly.geojson),
        "properties" : {
            "state_name" : county.state_name,
            "name" : county.name,
            "poor_health_days" : county.poor_health_days,
            "num_pcps" : county.num_pcps,
            "air_pol" : county.air_pol,
            "recfac" : county.recfac,
            "foodhealth" : county.foodhealth,
        },
        "id": county.fips
    }
    print "gj_dict: ", geojson_dict
    return geojson_dict

@csrf_exempt
def rank_locations(request):
    print "IN RANK"
    # Parse the JSON
    print request.POST
    print request.POST.get('loc_data')
    print request.GET
    try:
        objs = json.loads(request.POST.get('json'))
        #objs = request.POST.get('loc_data')
        #objs = json.loads(request.POST.copy())
    except Exception as e:
        print e
        objs = {}
        print "=("
    print "objs: ", objs
    data = []
    objs = objs.get('loc_data')
    for point in objs:
        try:
            location = 'POINT(' + point + ')'
            print "Point: ", point
            county = County.objects.get(mpoly__contains=location)
            data.append(county)
        except Exception as e:
            print e
    print "Printing data: \n"
    print data
    #output = data
    output = serializers.serialize("json", data, fields=('name', 'recfac', 'air_pol',
        'num_pcps', 'foodhealth', 'state_name',))
    print output
#    output = [{'name' : county.name,
#               'health_days' : county.poor_health_days} for county in data]
    return HttpResponse(json.dumps(output), mimetype='application/json')



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