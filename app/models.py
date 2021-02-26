from django.db import models


class Geolocalization(models.Model):
    ip = models.GenericIPAddressField()
    type = models.CharField(max_length=200, null=True, blank=True)
    continent_code = models.CharField(max_length=200, null=True, blank=True)
    continent_name = models.CharField(max_length=200, null=True, blank=True)
    country_code = models.CharField(max_length=200, null=True, blank=True)
    country_name = models.CharField(max_length=200, null=True, blank=True)
    region_code = models.CharField(max_length=200, null=True, blank=True)
    region_name = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    zip = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True)
    location = models.JSONField(null=True, blank=True)

    def __str__(self):
        return str(self.ip)
