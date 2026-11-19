from django.urls import path

from .views import (
    LocationDetailView,
    LocationListView,
    LocationSearchView,
    locations_page,
)

urlpatterns = [
    path("", locations_page, name="locations-page"),
    path("api/", LocationListView.as_view(), name="location-list"),
    path("api/search/", LocationSearchView.as_view(), name="location-search"),
    path("<slug:slug>/", LocationDetailView.as_view(), name="location-detail"),
]