from datetime import timedelta
from mixer.backend.django import mixer
from django.test import TestCase
from visamap import models


class TestCountryCodeFormatting(TestCase):
    def test_obtain_formatted_country_code(self):
        country = models.Country(name="Russia",
                                 code="RU")
        country.save()
        self.assertEqual("ru", country.formatted_code)

    def test_obtain_none_if_no_code_present(self):
        country = models.Country(name="Russia",
                                 code=None)
        country.save()
        self.assertIsNone(country.formatted_code)


class TestRequirementsByOrigin(TestCase):

    def setUp(self):
        # Creating instances on DB quickly
        mixer.cycle(5).blend(models.Requirement,
                             origin_country__id=5,
                             period=timedelta(days=1))
        mixer.cycle(3).blend(models.Requirement,
                             origin_country__id=3,
                             period=timedelta(days=1))

    def test_obtain_requirements_by_origin(self):
        self.assertEqual(
            3,
            len(models.Requirement.for_nationals_of(3)))

    def test_is_actually_country(self):
        for requirement in models.Requirement.for_nationals_of(5):
            self.assertEqual(5, requirement.origin_country.id)

    def test_for_nonexistent_country(self):
        self.assertEqual(
            0,
            len(models.Requirement.for_nationals_of(1))
        )