import abc
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.db.models import Count
from visamap.models import Country, Demonym, Requirement


class MapByOriginView(View):
    """
    Main page to show in a map requirements by country
    """
    def get(self, request):
        # Returns only countries with more than 1
        # requirement on the DB
        country_list = Country.objects.annotate(
            num_requirements=Count(
                'requirement')).filter(
            num_requirements__gt=1).order_by('name')

        # Returns only demonyms with more than 1
        # requirement for its country on the DB
        nationalities_list = Demonym.objects.annotate(
            num_reqs=Count('country__requirement')).filter(
            num_reqs__gt=1).order_by('description')

        return render(request, 'visamap/index.html', {
            'country_list': country_list,
            'nationalities_list': nationalities_list
        })


class MapByDestinationView(View):
    def get(self, request):
        # Returns only countries with more than 1
        # requirement on the DB
        country_list = Country.objects.annotate(
            num_requirements=Count(
                'destination_requirement')).filter(
            num_requirements__gt=1).order_by('name')
        return render(request, 'visamap/by_destination.html', {
            'country_list': country_list,
        })


class CountriesByVisaBase(View):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def _interest_code(self, requirement):
        pass

    def _format_response(self, requirements_for_country):
        """
        Formats response so that it can be easily usable by the frontend
        :param requirements_for_country: list of Requirement model objects
        :return: destinations_by_visa, dictionary containing visa names as keys
        and a list of country codes that require it as values.
        """
        destinations_by_visa = {}

        for req in requirements_for_country:
            visa_name = req.visa_type.description
            interest_code = self._interest_code(req)

            if visa_name not in destinations_by_visa:
                destinations_by_visa[visa_name] = []

            destinations_by_visa[visa_name].append(interest_code)

        return destinations_by_visa

    def _add_origin_country(self, codes_by_visa_name, country_id):
        origin_country = Country.objects.filter(id=country_id).first()
        if origin_country:
            codes_by_visa_name['origin country'] = [origin_country.formatted_code]
        return codes_by_visa_name


class DestinationsByVisaType(CountriesByVisaBase):

    def _interest_code(self, requirement):
        return requirement.destination_country.formatted_code

    def get(self, request, country_id):
        """
        Controller to be used via AJAX, that returns
        all visa types by destination country
        :param country_id: id of the country of the nationality of the traveler
        :return JSON containing visa types as it keys and a list of country
        codes as its values
        example: {'visa required': ['xx', 'yy', 'zz'],
                  'visa not required': ['ww', 'jj'],
                  'eVisa': ['xy']
                  }
        """
        requirements_for_country = Requirement.for_nationals_of(country_id)
        codes_by_visa_name = self._format_response(requirements_for_country)
        codes_by_visa_name = self._add_origin_country(codes_by_visa_name, country_id)
        return JsonResponse(codes_by_visa_name)


class OriginsByVisaType(CountriesByVisaBase):

    def _interest_code(self, requirement):
        return requirement.origin_country.formatted_code

    def get(self, request, country_id):
        """
        Controller to be used via AJAX, that returns
        all visa types by origin country
        :param country_id: id of the destination country
        :return JSON containing visa types as it keys and a list of country
        codes as its values
        example: {'visa required': ['xx', 'yy', 'zz'],
                  'visa not required': ['ww', 'jj'],
                  'eVisa': ['xy']
                  }
        """
        requirements_for_country = Requirement.for_visitors_to(country_id)
        codes_by_visa_name = self._format_response(requirements_for_country)
        codes_by_visa_name = self._add_origin_country(codes_by_visa_name, country_id)
        return JsonResponse(codes_by_visa_name)


class SpecificRequirementBase(View):

    def _get_observations(self, requirement):
        observations = ""
        if requirement:
            if requirement.visa_type:
                observations = requirement.visa_type.description
            if requirement.observations:
                observations += " - " + requirement.observations
        else:
            observations = 'Data not found.'
        return JsonResponse({'observations': observations})


class SpecificRequirementForDestination(SpecificRequirementBase):
    def get(self, request, country_id, destination_code):
        """
        Controller to be used via AJAX, that returns observations for a
        determined visa of an specific destination
        :param country_id: id of the country of the nationality of the traveler
        :param destination_id: country_id of the destination country
        :return JSON containing an object with observations related to the visa
        """
        requirement = Requirement.objects.filter(
            origin_country=country_id,
            destination_country__code=destination_code.upper()).first()
        return self._get_observations(requirement)


class SpecificRequirementForOrigin(SpecificRequirementBase):
    def get(self, request, country_code, destination_id):
        """
        Controller to be used via AJAX, that returns observations for a
        determined visa of an specific origin
        :param country_code: code of the destination
        :param destination_id: country_id of the origin country
        :return JSON containing an object with observations related to the visa
        """
        requirement = Requirement.objects.filter(
            origin_country__code=country_code.upper(),
            destination_country=destination_id).first()
        return self._get_observations(requirement)