from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^by_destination/$', views.MapByDestinationView.as_view(),
        name='by_destination'),
    url(r'^requirements/(?P<country_id>[0-9]+)/$',
        views.CountriesByVisaType.as_view(),
        name='requirements'),
    url(r'^requirements/(?P<country_id>[0-9]+)/' +
        '(?P<destination_code>[a-zA-Z]{2})/$',
        views.SpecificRequirementView.as_view(),
        name='requirements_specific'),
]