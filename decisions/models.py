
from django.contrib.gis.db import models

# Create your models here.


#class State(models.Model):
#    fips = models.IntegerField(unique=True, primary_key=True)
#    mpoly = models.MultiPolygonField()
#    objects = models.GeoManager()
#    name = models.CharField()
#
#    def __unicode__(self):
#        return self.fips


class County(models.Model):
    fips = models.IntegerField(unique=True, primary_key=True)
    state_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    mpoly = models.MultiPolygonField()
    objects = models.GeoManager()

    poor_health_days = models.IntegerField(null=True)
    num_pcps = models.IntegerField(null=True)
    air_pol = models.IntegerField(null=True)
    recfac = models.IntegerField(null=True)
    foodhealth = models.IntegerField(null=True)
