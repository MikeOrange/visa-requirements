from __future__ import unicode_literals
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=2, unique=True, null=True)

    @property
    def formatted_code(self):
        """
        :return: Returns lowercase country code if present
        else returns None
        """
        return self.code.lower() if self.code else None


class Demonym(models.Model):
    description = models.CharField(max_length=50)
    country = models.ForeignKey(Country)

    class Meta:
        unique_together = (("description", "country"),)


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

    class Meta:
        unique_together = (("origin_country", "destination_country"),)

    @staticmethod
    def for_nationals_of(origin_country_id):
        return Requirement.objects.filter(
            origin_country=origin_country_id).all()

    @staticmethod
    def for_visitors_to(destination_country_id):
        return Requirement.objects.filter(
            destination_country=destination_country_id).all()