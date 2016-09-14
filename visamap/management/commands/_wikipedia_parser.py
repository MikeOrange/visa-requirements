from bs4 import BeautifulSoup
import requests
import re

BASE_URL = "https://en.wikipedia.org"


class PageParser(object):
    def __init__(self, url):
        self._table = None
        request = requests.get(
           BASE_URL + url)
        page_html = request.text
        self.page_soup = BeautifulSoup(page_html)

    @property
    def table(self):
        if not self._table:
            self._table = self.page_soup.find("table")
        return self._table

class RequirementsPage(PageParser):
    def __init__(self, url):
        super(RequirementsPage, self).__init__(url)
        self.requirements = {}

    def get_requirements(self):
        """

        :return: Dictionary of requirements where the key
        is the name of the country and the content is a tuple
        of visa requirement description and notes.
        """
        if self.requirements or not self.table:
            return self.requirements

        for row in self.table.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) >= 3:
                visa_description = columns[1].contents[0]
                if not isinstance(visa_description, basestring):
                    visa_description = str(visa_description.contents[0])
                notes = columns[2].contents[0] if columns[2].contents else \
                    columns[2].get_text()

                self.requirements[columns[0].get_text().strip()] = (
                    visa_description,
                    notes)
            else:
                print "Ignored row, ", columns
        return self.requirements


class CountryListParser(PageParser):
    def __init__(self):
        super(CountryListParser, self).__init__(
           "/wiki/Category:Visa_requirements_by_nationality")
        self._links = []

    def _get_links(self):
        for link in self.table.find_all('a'):
            title = link.get("title")
            if title and title.startswith("Visa requirements for"):
                self._links.append(link)

    def requirements_links(self):
        if not self._links:
            self._get_links()
        return self._links


class DemonymsParser(PageParser):
    def __init__(self):
        super(DemonymsParser, self).__init__(
            "/wiki/List_of_adjectival_and_demonymic"
            "_forms_for_countries_and_nations")
        self._demonyms = {}

    def _filter_out_info_links(self, country_demonyms):
        """ Filters out information links like [1] """
        r = re.compile('^\[[0-9]+\]$')
        return filter(lambda x: not r.match(x), country_demonyms)

    def _extract_country_name(self, columns):
        return columns[0].find('a').get_text()

    def _extract_country_demonyms(self, columns):
        return [a.get_text() for a in columns[1].find_all('a')]

    def _get_single_country_demonyms(self, columns):
        country_name = self._extract_country_name(columns)
        country_demonyms = self._extract_country_demonyms(columns)
        country_demonyms = self._filter_out_info_links(country_demonyms)
        self._demonyms[country_name] = country_demonyms

    def get_demonyms(self):
        if not self._demonyms:
            for row in self.table.find_all('tr'):
                columns = row.find_all('td')
                if len(columns) >= 2:
                    self._get_single_country_demonyms(columns)
                else:
                    print "Data unclear for", columns
        return self._demonyms
