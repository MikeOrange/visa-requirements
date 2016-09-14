from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from visamap.models import Country, Demonym, Requirement


# CODE-REVIEW: a CBV would be better
def index(request):
    """
    Main page to show in a map requirements by country
    """
    country_list = Country.objects.all().order_by('name')
    nationalities_list = Demonym.objects.all().order_by('description')
    return render(request, 'visamap/index.html', {
        'country_list': country_list,
        'nationalities_list': nationalities_list
    })


def country_requirements(request, country_id):
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
    requirements = Requirement.objects.filter(
        origin_country=country_id).all()
    res = {}

    for r in requirements:
        if r.visa_type.description not in res:
            res[r.visa_type.description] = []
        # CODE-REVIEW: the following lines are difficult to read
        res[r.visa_type.description].append(
            r.destination_country.code.lower() if
            r.destination_country.code else None)
    return JsonResponse(res)


def specific_requirement(request, country_id, destination_id):
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
