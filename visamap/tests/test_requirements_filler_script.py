from datetime import timedelta
from django.test import TestCase
from visamap.management.commands.fill_requirements import (
    VisaRequirementRecord, get_nationality_from_link_title,
    OriginCountryNotFound, DestinationCountryNotFound)
from visamap.models import Country, Demonym, VisaType, Requirement


class VisaRecordTests(TestCase):

    def setUp(self):
        origin_country = Country(name='testland', code='xx')
        origin_country.save()
        new_demonym = Demonym(description='testian',
                              country=origin_country)
        new_demonym.save()
        dest_country = Country(name='paradise',
                               code='yy')
        dest_country.save()

    def test_correctly_created(self):
        self.visa = VisaRequirementRecord(
            'testian',
            'paradise',
            'visa required',
            '')
        self.assertEqual(self.visa.origin_country.name,
                         'testland')
        self.assertEqual(self.visa.destination_country.name,
                         'paradise')

    def test_visa_type_created(self):
        self.visa = VisaRequirementRecord(
            'testian',
            'paradise',
            'visa required',
            '')
        self.assertEqual(self.visa.visa_type.description,
                         'visa required')
        visa_type_name = VisaType.objects.first().description
        self.assertEqual('visa required', visa_type_name)

    def test_its_saved_to_db_correctly(self):
        self.visa = VisaRequirementRecord(
            'testian',
            'paradise',
            'visa required',
            '')
        self.visa.save_to_db()
        requirement = Requirement.objects.first()
        self.assertEqual(requirement.destination_country.name, 'paradise')
        self.assertEqual(requirement.origin_country.name, 'testland')
        self.assertEqual(requirement.visa_type.description, 'visa required')

    def test_trying_to_create_with_non_existing_origin_country(self):
        self.assertRaises(OriginCountryNotFound,
                          VisaRequirementRecord,
                          'selenite',
                          'paradise',
                          'visa required',
                          '')

    def test_trying_to_create_with_non_existing_destination_country(self):
        self.visa = VisaRequirementRecord(
            'testian',
            'jungle',
            'visa required',
            '')
        with self.assertRaises(DestinationCountryNotFound):
            self.visa.destination_country


class PeriodExtractionTests(TestCase):
    def setUp(self):
        new_country = Country(name='testland', code='xx')
        new_country.save()
        new_demonym = Demonym(description='testian',
                              country=new_country)
        new_demonym.save()
        self.visa = VisaRequirementRecord(
            'testian',
            'testland',
            'visa required',
            ''
        )

    def test_period_in_days_alone(self):
        self.visa._notes = "5 days"
        self.assertEqual(timedelta(days=5),
                         self.visa.period)

    def test_period_in_months_alone(self):
        self.visa._notes = "7 months"
        self.assertEqual(timedelta(days=210),
                         self.visa.period)

    def test_period_in_days_with_more(self):
        self.visa._notes = "other stuff, 5 days ..."
        self.assertEqual(
            timedelta(days=5),
            self.visa.period)

    def test_period_in_months_with_more(self):
        self.visa._notes = "Come on 7 months, 55"
        self.assertEqual(timedelta(days=210),
                         self.visa.period)

    def test_single_month(self):
        self.visa._notes = "1 month"
        self.assertEqual(timedelta(days=30),
                         self.visa.period)

    def test_mixed_days_and_months_only_pays_attention_to_days(self):
        self.visa._notes = "7 months or 15 days"
        self.assertEqual(timedelta(days=15),
                         self.visa.period)

    def test_returns_none_if_nothing_found(self):
        self.visa._notes = "whatever"
        self.assertEqual(None,
                         self.visa.period)
        self.visa._notes = ""
        self.assertEqual(None,
                         self.visa.period)


class NationalityExtractionTests(TestCase):
    def test_extracts_denonym_nationality(self):
        self.assertEqual(
            "Venezuelan",
            get_nationality_from_link_title("Visa requirements for Venezuelan citizens"))

    def test_extracts_country_name_nationality(self):
        self.assertEqual(
            "United States",
            get_nationality_from_link_title("Visa requirements for United States citizens"))

    def test_extracts_when_different_words_used(self):
        self.assertEqual(
            "Turks and Caicos Islands",
            get_nationality_from_link_title(
                "Visa requirements for British Overseas Territories Citizens of Turks and Caicos Islands"))

        self.assertEqual(
            "Hong Kong",
            get_nationality_from_link_title(
                "Visa requirements for Chinese citizens of Hong Kong"))
