from django.core.management.base import BaseCommand
from visamap.models import Country, Demonym
from _wikipedia_parser import DemonymsParser


def insert_demonyms_to_db(country, country_demonyms):
    for demonym in country_demonyms:
        # Will accept "Dominican" only for Dominica or
        # Dominican Republic, will have to differentiate
        # manually
        demonym_object, created = Demonym.objects.get_or_create(
            description=demonym,
            country=country
        )
        demonym_object.save()


def insert_countries_to_db(all_demonyms):
    for country_name in all_demonyms:
        country, created = Country.objects.get_or_create(
            name=country_name)
        insert_demonyms_to_db(country,
                              all_demonyms.get(country_name))
        if created:
            country.save()


class Command(BaseCommand):
    help = 'Extracts country demonyms from Wikipedia and saves them to our DB'

    def handle(self, *args, **options):
        all_demonyms = DemonymsParser().get_demonyms()
        insert_countries_to_db(all_demonyms)
