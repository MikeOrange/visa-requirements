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
    """
    Represents a single Visa requirement from a country to a nationality
    used tp organize and store the information on the Database
    """
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
        """
        Determines country of origin from the nationality using the
        demonyms table
        :param nationality: string containing nationality to be checked
        :raise OriginCountryNotFound if the country determined does not exist
        """
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
        """
        Getter for country of origin
        :return:
        """
        return self._origin_country

    @property
    def destination_country(self):
        """
        Getter for destination country
        :return: string containing the object from the Country
        model of the destination country
        """
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
        """
        Returns visa type object, creating it in the database
        if it does not exist
        :return: VisaType object
        """
        if not self._visa_type:
            visa_type, created = VisaType.objects.get_or_create(
                description=self._visa_description)

            self._visa_type = visa_type

        return self._visa_type

    @property
    def notes(self):
        """
        :return: string containing the observations related to the visa
        """
        return unicode(self._notes)

    @property
    def period(self):
        """
        Extracted period from notes in days
        :return: timedelta object containing the period of the visa
        """
        r_days = re.compile('(\d+) day')
        matched = r_days.search(self.notes)
        if matched:
            return timedelta(days=int(matched.group(1)))
        r_months = re.compile('(\d+) month')
        matched = r_months.search(self.notes)
        if matched:
            return timedelta(days=int(matched.group(1))*30)

    def save_to_db(self):
        """
        Saves info contained in the instance to a database
        """
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
    """
    Gets a nationality from a link title
    :param title: Title of a link from the country list page
    :return: string containing extracted nationality
    """
    weird_nationality_re = re.compile('Visa requirements for .+ (?:c|C)itizens of (.+)')
    matched = weird_nationality_re.search(title)
    if matched:
        return matched.group(1)

    nationality_re = re.compile('Visa requirements for (.+) citizens')
    matched = nationality_re.search(title)
    if matched:
        return matched.group(1)


def add_country_requirements_to_db(nationality, all_requirements):
    """
    Builds VisaRequirementRecord instances from parsed requirements
    :param nationality: string containing nationality of origin
    :param all_requirements: dict with destination countries as keys
    and all requirements structured as a list of tuples as its values
    """
    for country_name in all_requirements:
        try:
            record = VisaRequirementRecord(nationality,
                                           country_name,
                                           all_requirements[country_name][0],
                                           all_requirements[country_name][1])
            record.save_to_db()
        except OriginCountryNotFound:
            # TODO: Save detailed error to log
            print "Origin country not found!"
            continue
        except DestinationCountryNotFound:
            # TODO: Save detailed error to log
            print "Destination country not found!"
            continue


class Command(BaseCommand):
    help = 'Extracts visa requirements for all countries and saves them to DB'

    def add_arguments(self, parser):
        """ Optional arguments """
        parser.add_argument('--starting',
                            dest='starting',
                            default=False,
                            help="Start parsing from this nationality")
        parser.add_argument('--single',
                            dest='single',
                            default=False,
                            help="Parse only this nationality")

    @staticmethod
    def process_requirements(nationality, link):
        requirements = RequirementsPage(link.get("href")).get_requirements()
        add_country_requirements_to_db(nationality, requirements)

    def handle(self, *args, **options):
        country_links = CountryListParser().requirements_links()

        # starting point
        for link in country_links:
            nationality = get_nationality_from_link_title(link.get('title'))

            if options.get('single'):
                if nationality == options.get('single'):
                    self.process_requirements(nationality, link)
                    return
            elif options.get('starting'):
                process = False
                if nationality == options.get('starting'):
                    process = True
                if process:
                    self.process_requirements(nationality, link)
            else:
                self.process_requirements(nationality, link)