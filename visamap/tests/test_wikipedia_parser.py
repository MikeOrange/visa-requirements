import mock
from django.test import TestCase
from visamap.management.commands._wikipedia_parser import (
    PageParser, RequirementsPage, CountryListParser,
    DemonymsParser)


PAGE_WITH_TABLE = '<!DOCTYPE html>' \
                  '<header></header>' \
                  '<body><table>hello</table></body>'
PAGE_WITHOUT_TABLE = '<!DOCTYPE html>' \
                  '<header></header>' \
                  '<body><div>bye</div></body>'


class TestBasePageParser(TestCase):

    @mock.patch('visamap.management.commands.'
                '_wikipedia_parser.requests')
    def test_get_table_from_html(self, mock_requests):
        mock_requests.get.return_value.text = PAGE_WITH_TABLE
        parser = PageParser('anything')
        self.assertEqual(parser.table.text, "hello")

    @mock.patch('visamap.management.commands.'
                '_wikipedia_parser.requests')
    def test_get_table_from_html_without_it(self, mock_requests):
        mock_requests.get.return_value.text = PAGE_WITHOUT_TABLE
        parser = PageParser('anything')
        self.assertIsNone(parser.table)


class TestRequirementsParser(TestCase):

    def setUp(self):
        self.page_html = open(
            'visamap/tests/resources/example_requirements.html',
            'r').read()

    @mock.patch('visamap.management.commands.'
                '_wikipedia_parser.requests')
    def test_get_table_from_html(self, mock_requests):
        mock_requests.get.return_value.text = self.page_html
        parser = RequirementsPage('anything')
        self.assertEqual(parser.table.attrs.get('class'),
                         ["sortable", "wikitable"])

    @mock.patch('visamap.management.commands.'
                '_wikipedia_parser.requests')
    def test_get_requirements(self, mock_requests):
        mock_requests.get.return_value.text = self.page_html
        parser = RequirementsPage('anything')
        self.assertEqual(
            parser.get_requirements().get('Albania'),
            ('Visa required',
             'Holders of valid multiple entry visa '
             'issued by the USA/United Kingdom/Schengen States are exempt'))
        self.assertEqual(
            parser.get_requirements().get('Afghanistan'),
            ('Visa required',
             ''))

    @mock.patch('visamap.management.commands.'
                '_wikipedia_parser.requests')
    def test_invalid_page(self, mock_requests):
        mock_requests.get.return_value.text = PAGE_WITHOUT_TABLE
        parser = RequirementsPage('anything')
        self.assertEqual({}, parser.get_requirements())


class CountryParserTests(TestCase):
    def setUp(self):
        self.page_html = open(
            'visamap/tests/resources/example_country_list.html',
            'r').read()

    @mock.patch('visamap.management.commands.'
                '_wikipedia_parser.requests')
    def test_get_table_from_html(self, mock_requests):
        mock_requests.get.return_value.text = self.page_html
        parser = CountryListParser()
        self.assertTrue('nowraplinks' in parser.table.attrs.get('class'))

    @mock.patch('visamap.management.commands.'
                '_wikipedia_parser.requests')
    def test_get_all_links(self, mock_requests):
        mock_requests.get.return_value.text = self.page_html
        parser = CountryListParser()
        self.assertEqual(
            'Angolan',
            parser.requirements_links()[0].get_text())

    @mock.patch('visamap.management.commands.'
                '_wikipedia_parser.requests')
    def test_invalid_page(self, mock_requests):
        mock_requests.get.return_value.text = PAGE_WITHOUT_TABLE
        parser = CountryListParser()
        with self.assertRaises(AttributeError):
            parser.requirements_links()


class DemonymsParserTests(TestCase):
    def setUp(self):
        self.page_html = open(
            'visamap/tests/resources/example_demonyms.html',
            'r').read()

    @mock.patch('visamap.management.commands.'
                '_wikipedia_parser.requests')
    def test_get_table_from_html(self, mock_requests):
        mock_requests.get.return_value.text = self.page_html
        parser = DemonymsParser()
        classes = parser.table.attrs.get('class')
        classes.sort()
        self.assertEqual(classes,
                         ["sortable", "wikitable"])

    @mock.patch('visamap.management.commands.'
                '_wikipedia_parser.requests')
    def test_get_all_demonyms(self, mock_requests):
        mock_requests.get.return_value.text = self.page_html
        parser = DemonymsParser()
        self.assertEqual(
            ['Antiguan', 'Barbudan'],
            parser.get_demonyms().get("Antigua and Barbuda"))

    @mock.patch('visamap.management.commands.'
                '_wikipedia_parser.requests')
    def test_invalid_page(self, mock_requests):
        mock_requests.get.return_value.text = PAGE_WITHOUT_TABLE
        parser = DemonymsParser()
        with self.assertRaises(AttributeError):
            parser.get_demonyms()