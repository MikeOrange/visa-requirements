from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from visamap.models import Country, Demonym, Requirement


def index(request):
    country_list = Country.objects.all().order_by('name')
    nationalities_list = Demonym.objects.all().order_by('description')
    return render(request, 'visamap/index.html', {
        'country_list': country_list,
        'nationalities_list': nationalities_list
    })


def country_requirements(request, country_id):
    requirements = Requirement.objects.filter(
        origin_country=country_id).all()
    res = {}
    for r in requirements:
        if r.visa_type.description not in res:
            res[r.visa_type.description] = []
        res[r.visa_type.description].append(
            r.destination_country.code.lower() if
            r.destination_country.code else None)
    return JsonResponse(res)


def specific_requirement(request, country_id, destination_id):
    requirement = Requirement.objects.filter(
        origin_country=country_id,
        destination_country=destination_id).first()
    if requirement:
        response = {
            'observations': requirement.observations or 'Data not found.'
        }
    else:
        response= {
            'observations': 'Data not found.'
        }
    return JsonResponse(response)
