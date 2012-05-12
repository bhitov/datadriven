__author__ = 'ben'
import os
from django.contrib.gis.utils import LayerMapping
from models import County
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
#['FIPS', 'STATE', 'COUNTY', 'POORHLTH', 'PCP', 'AIRPOL', 'RECFAC', 'FOODHLTH']
#poor_health_days = models.IntegerField(null=True)
#num_pcps = models.IntegerField(null=True)
#air_pol = models.IntegerField(null=True)
#recfac = models.IntegerField(null=True)
#foodhealth = models.IntegerField(null=True)
# os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/UScounties.shp'))
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



