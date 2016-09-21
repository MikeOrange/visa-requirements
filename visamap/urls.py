from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^by_destination/$', views.MapByDestinationView.as_view(),
        name='by_destination'),
    url(r'^requirements/(?P<country_id>[0-9]+)/$',
        views.DestinationsByVisaType.as_view(),
        name='requirements'),
    url(r'^requirements_reversed/(?P<country_id>[0-9]+)/$',
        views.OriginsByVisaType.as_view(),
        name='requirements_reversed'),
    url(r'^requirements/(?P<country_id>[0-9]+)/' +
        '(?P<destination_code>[a-zA-Z]{2})/$',
        views.SpecificRequirementForDestination.as_view(),
        name='specific_requirements'),
    url(r'^requirements/(?P<country_code>[a-zA-Z]{2})/' +
        '(?P<destination_id>[0-9]+)/$',
        views.SpecificRequirementForOrigin.as_view(),
        name='specific_requirements_reversed'),
]