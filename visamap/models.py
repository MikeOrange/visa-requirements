from __future__ import unicode_literals

from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Demonym(models.Model):
    description = models.CharField(max_length=50)
    country = models.ForeignKey(Country)


class VisaType(models.Model):
    description = models.TextField(unique=True)


class Requirement(models.Model):
    origin_country = models.ForeignKey(Country)
    destination_country = models.ForeignKey(
        Country,
        related_name='destination_requirement')
    visa_type = models.ForeignKey(VisaType)
    observations = models.TextField(null=True)
    period = models.DurationField(null=True)