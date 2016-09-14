from datetime import timedelta
from django.test import TestCase
from visamap.management.commands.fill_requirements import (
    get_period_from_notes, get_nationality_from_link_title)


class PeriodExtractionTests(TestCase):
    def test_period_in_days_alone(self):
        self.assertEqual(timedelta(days=5),
                         get_period_from_notes("5 days"))

    def test_period_in_months_alone(self):
        self.assertEqual(timedelta(days=210),
                         get_period_from_notes("7 months"))

    def test_period_in_days_with_more(self):
        self.assertEqual(
            timedelta(days=5),
            get_period_from_notes("other stuff, 5 days ..."))

    def test_period_in_months_with_more(self):
        self.assertEqual(timedelta(days=210),
                 get_period_from_notes("Come on 7 months, 55"))

    def test_single_month(self):
        self.assertEqual(timedelta(days=30),
                 get_period_from_notes("1 month"))

    def test_mixed_days_and_months_only_pays_attention_to_days(self):
        self.assertEqual(timedelta(days=15),
                 get_period_from_notes("7 months or 15 days"))

    def test_returns_none_if_nothing_found(self):
        self.assertEqual(None,
                 get_period_from_notes("whatever"))
        self.assertEqual(None,
                 get_period_from_notes(""))


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
