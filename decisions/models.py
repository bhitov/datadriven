
from django.contrib.gis.db import models
from django.contrib.gis import admin

# Create your models here.

class County(models.Model):
    fips = models.IntegerField(unique=True, primary_key=True)
    state_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    mpoly = models.MultiPolygonField()

    def __unicode__(self):
        return self.name


class Metric(models.Model):
    """
    Name and value to opacity conversion for county metrics
    """
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    verbose_name = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.name

class MetricValue(models.Model):
    """
    Value for a county by metric
    """
    metric = models.ForeignKey(Metric)
    county = models.ForeignKey(County)
    value = models.FloatField()

    def __unicode__(self):
        return "%s %s" % (self.metric.name, self.county.name)


admin.site.register(County, admin.GeoModelAdmin)

