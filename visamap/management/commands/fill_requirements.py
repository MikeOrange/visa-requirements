import re
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from visamap.management.commands._wikipedia_parser import (CountryListParser,
                                                           RequirementsPage)
from visamap.models import Country, Demonym, Requirement, VisaType


class DestinationCountryNotFound(Exception):
    pass


class OriginCountryNotFound(Exception):
    pass


class VisaRequirementRecord(object):
    def __init__(self,
                 nationality,
                 destination_country_name,
                 visa_description,
                 notes):
        self._visa_description = visa_description
        self._notes = notes
        self._visa_type = None
        self._destination_country = None
        self._destination_country_name = destination_country_name
        self._origin_country = None
        self._get_country_from_nationality(nationality)

    def _get_country_from_nationality(self, nationality):
        demonym = Demonym.objects.filter(description=nationality).first()
        if demonym:
            self._origin_country = demonym.country
        else:
            country = Country.objects.filter(name=nationality).first()
            if country:
                self._origin_country = country
            else:
                raise OriginCountryNotFound(
                    self._destination_country_name +
                    " has not been found on the DB")

    @property
    def origin_country(self):
        return self._origin_country

    @property
    def destination_country(self):
        if not self._destination_country:
            try:
                self._destination_country = Country.objects.get(
                    name=self._destination_country_name)
            except ObjectDoesNotExist:
                raise DestinationCountryNotFound(
                    self._destination_country_name +
                    " has not been found on the DB")
        return self._destination_country

    @property
    def visa_type(self):
        if not self._visa_type:
            visa_type, created = VisaType.objects.get_or_create(
                description=self._visa_description)

            self._visa_type = visa_type

        return self._visa_type

    @property
    def notes(self):
        return unicode(self._notes)

    @property
    def period(self):
        r_days = re.compile('(\d+) day')
        matched = r_days.search(self.notes)
        if matched:
            return timedelta(days=int(matched.group(1)))
        r_months = re.compile('(\d+) month')
        matched = r_months.search(self.notes)
        if matched:
            return timedelta(days=int(matched.group(1))*30)

    def save_to_db(self):
        requirement, created = Requirement.objects.get_or_create(
            origin_country=self.origin_country,
            destination_country=self.destination_country,
            visa_type=self.visa_type,
            observations=self.notes,
            period=self.period
        )
        if created:
            requirement.save()


def get_nationality_from_link_title(title):
    weird_nationality_re = re.compile('Visa requirements for .+ (?:c|C)itizens of (.+)')
    matched = weird_nationality_re.search(title)
    if matched:
        return matched.group(1)

    nationality_re = re.compile('Visa requirements for (.+) citizens')
    matched = nationality_re.search(title)
    if matched:
        return matched.group(1)


def add_country_requirements_to_db(nationality, all_requirements):
    for country_name in all_requirements:
        try:
            record = VisaRequirementRecord(nationality,
                                           country_name,
                                           all_requirements[country_name][0],
                                           all_requirements[country_name][1])
            record.save_to_db()
        except OriginCountryNotFound:
            # TODO: Save detailed error to log
            continue
        except DestinationCountryNotFound:
            # TODO: Save detailed error to log
            continue


class Command(BaseCommand):
    help = 'Extracts visa requirements for all countries and saves them to DB'

    def handle(self, *args, **options):
        country_links = CountryListParser().requirements_links()
        # TODO: add parameter to set individual country or
        # starting point
        for link in country_links:
            nationality = get_nationality_from_link_title(link.get('title'))
            requirements = RequirementsPage(link.get("href")).get_requirements()
            add_country_requirements_to_db(nationality, requirements)