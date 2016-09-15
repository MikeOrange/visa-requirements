from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from visamap.models import Country, Demonym, Requirement


class IndexView(View):
    """
    Main page to show in a map requirements by country
    """
    def get(self, request):
        country_list = Country.objects.all().order_by('name')
        nationalities_list = Demonym.objects.all().order_by('description')
        return render(request, 'visamap/index.html', {
            'country_list': country_list,
            'nationalities_list': nationalities_list
        })


class CountriesByVisaType(View):
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
            destination_code = req.destination_country.formatted_code

            if visa_name not in destinations_by_visa:
                destinations_by_visa[visa_name] = []

            destinations_by_visa[visa_name].append(destination_code)

        return destinations_by_visa

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
        return JsonResponse(codes_by_visa_name)


class SpecificRequirementView(View):
    def get(self, request, country_id, destination_id):
        """
        Controller to be used via AJAX, that returns observations for a
        determined visa of an specific destination
        :param country_id: id of the country of the nationality of the traveler
        :param destination_id: country_id of the destination country
        :return JSON containing an object with observations related to the visa
        """
        requirement = Requirement.objects.filter(
            origin_country=country_id,
            destination_country=destination_id).first()

        if requirement and requirement.observations:
            observations = requirement.observations
        else:
            observations = 'Data not found.'

        return JsonResponse({'observations': observations})
