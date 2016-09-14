from datetime import timedelta
from json import loads
from django.test import TestCase, Client
from visamap.models import Country, Requirement, Demonym, VisaType
from visamap.views import country_requirements, specific_requirement


class CountryRequirementsTests(TestCase):

    def setUp(self):
        self._client = Client()
        self.origin_country = Country(name='testland', code='xx')
        self.origin_country.save()
        self.new_demonym = Demonym(description='testian',
                                   country=self.origin_country)
        self.new_demonym.save()
        self.dest_country = Country(name='paradise',
                                    code='yy')
        self.dest_country.save()
        self.visa_type = VisaType(description='visa required')
        self.visa_type.save()
        self.requirement = Requirement(
            origin_country=self.origin_country,
            destination_country=self.dest_country,
            visa_type=self.visa_type,
            observations='hello',
            period=timedelta(days=5)
        )
        self.requirement.save()

    def test_get_country_requirement(self):
        response = self._client.get('/requirements/' + str(self.origin_country.id))
        self.assertEqual(200, response.status_code)
        content = loads(response.content)
        self.assertEqual(content, {
            'visa required': ['yy']
        })

    def test_get_country_from_non_existant_country_return_empty(self):
        response = self._client.get('/requirements/0')
        self.assertEqual(200, response.status_code)
        content = loads(response.content)
        self.assertEqual(content, {})

    def test_get_specific_requirement(self):
        response = self._client.get(
            '/requirements/' +
            str(self.origin_country.id) + '/' +
            str(self.dest_country.id)
        )
        self.assertEqual(200, response.status_code)
        content = loads(response.content)
        self.assertEqual(content,
                         {'observations': 'hello'})

    def test_get_specific_requirement_for_non_existing_destination(self):
        response = self._client.get(
            '/requirements/' +
            str(self.origin_country.id) + '/0'
        )
        self.assertEqual(200, response.status_code)
        content = loads(response.content)
        self.assertEqual(content,
                         {'observations': 'Data not found.'})

    def test_get_specific_requirement_for_non_existing_origin(self):
        response = self._client.get(
            '/requirements/0/' + str(self.dest_country.id)
        )
        self.assertEqual(200, response.status_code)
        content = loads(response.content)
        self.assertEqual(content,
                         {'observations': 'Data not found.'})

    def test_get_specific_requirement_where_both_dont_exists(self):
        response = self._client.get(
            '/requirements/0/0'
        )
        self.assertEqual(200, response.status_code)
        content = loads(response.content)
        self.assertEqual(content,
                         {'observations': 'Data not found.'})

    def test_get_specific_requirement_for_country_with_empty_notes(self):
        self.requirement.observations = ''
        self.requirement.save()
        response = self._client.get(
            '/requirements/' +
            str(self.origin_country.id) + '/' +
            str(self.dest_country.id)
        )
        self.assertEqual(200, response.status_code)
        content = loads(response.content)
        self.assertEqual(content,
                         {'observations': 'Data not found.'})