from django.urls import path

from .views import (
    LocationDetailView,
    LocationListView,
    LocationSearchView,
)

urlpatterns = [
    path("", LocationListView.as_view(), name="location-list"),
    path("search/", LocationSearchView.as_view(), name="location-search"),
    path("<slug:slug>/", LocationDetailView.as_view(), name="location-detail"),
]