from django.db import models


class PointOfSale(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    working_hours = models.CharField(max_length=100)

    def __str__(self):
        return self.name
