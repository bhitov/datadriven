# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render
import urllib2
import json
from django.views.decorators.csrf import csrf_exempt
from models import County, Metric, MetricValue
from django.core import serializers
from django.contrib.gis.geos import Polygon


def location_list(request):
    # figure out bounding box
    bbox = request.GET['bbox'].split(',')
    poly = Polygon.from_bbox(bbox)

    metric_names = Metric.objects.values_list('name', flat=True)
#    metric_names = [
#    'poor_health_days',
#    'pcp_availability',
#    'air_pollution',
#    'recreational_facilities',
#    'food_health',
#    ]
    # fetch counties
    counties = County.objects.filter(mpoly__intersects=poly)
    metrics = Metric.objects.filter(name__in=[metric_names]).order_by('county', 'metric')
    metric_values = [1,2]
    metric_values =


    # convert to geojson
    geojson_dict = {
        "type" : "FeatureCollection",
        "features": [county_to_geojson(county) for county in counties],
    }

    return HttpResponse(json.dumps(geojson_dict),
                            content_type='application/json')

def county_to_geojson(county, metric_values):
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
    return geojson_dict

@csrf_exempt
def rank_locations(request):
    # Parse the JSON
    try:
        objs = json.loads(request.POST.get('json'))
    except Exception as e:
        print e
        objs = {}
    data = []
    objs = objs.get('loc_data')
    for point in objs:
        try:
            location = 'POINT(' + point + ')'
            county = County.objects.get(mpoly__contains=location)
            data.append(county)
        except Exception as e:
            print e
    output = serializers.serialize("json", data, fields=('name', 'recfac', 'air_pol',
        'num_pcps', 'foodhealth', 'state_name',))
    return HttpResponse(json.dumps(output), mimetype='application/json')

