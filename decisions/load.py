__author__ = 'ben'
import os
from django.contrib.gis.utils import LayerMapping
from models import County, Metric, MetricValue
import csv

county_mapping = {
    'fips' : 'FIPS',
    'name' : 'NAME',
    'state_name' : 'STATE_NAME',
    'mpoly' : 'MULTIPOLYGON',
    }

county_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/UScounties.shp'))

def run(verbose=True):
    lm = LayerMapping(County, county_shp, county_mapping,
        transform=False, encoding='iso-8859-1')

    lm.save(strict=True, verbose=verbose)

county_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/CountyHealthText.csv'))

def load_csv():
    c = csv.reader(open(county_csv, 'r'))
    c.next()
    for line in c:
        try:
            print line
            county = County.objects.get(fips=int(line[0]))
            county.poor_health_days = int(line[3])
            county.num_pcps = int(line[4])
            county.air_pol = int(line[5])
            county.recfac = int(line[6])
            county.foodhealth = int(line[7])
            county.save()
        except Exception as e:
            print e

def metric_abstraction_migration():

    metric_name_data = {
        'poor_health_days': ['poor_health_days', 'Poor health days', 'filler'],
        'num_pcps' : ['pcp_availability', 'Number of PCPs', 'Number of primary care physicians'],
        'air_pol' : ['air_pollution', 'Air polution', 'Air polution'],
        'recfac' : ['recreational_facilities', 'Recreational facilities', 'Availability of recreational facilities'],
        'foodhealth' : ['food_health', 'Food health', 'Availability of healthy food']
    }

    counties = County.objects.all()
    for metric_name in metric_name_data:
        data = metric_name_data[metric_name]
        metric = (Metric.objects.create(name=data[0], verbose_name=data[1],
                                        description=data[2]))
        print "created Metric: ", metric
        for county in counties:
            metric_value = getattr(county, metric_name)
            if metric_value is not None:
                m = MetricValue.objects.create(metric=metric, county=county, value=metric_value)
                print "created MetricValue: ", m


