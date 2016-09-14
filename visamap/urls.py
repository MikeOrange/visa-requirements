from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^requirements/(?P<country_id>[0-9]+)$',
        views.country_requirements,
        name='requirements'),
    url(r'^requirements/(?P<country_id>[0-9]+)/' +
        '(?P<destination_id>[0-9]+)$',
        views.specific_requirement,
        name='requirements_specific'),
]