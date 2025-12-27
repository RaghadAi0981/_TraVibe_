from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("", lambda request: redirect("countries"), name="home"),
    path("countries/", views.countries_list, name="countries"),
    path("countries/<int:country_id>/cities/", views.cities_list, name="cities"),
    path("cities/<int:city_id>/places/", views.places_list, name="places"),
    path("places/<int:place_id>/", views.place_detail, name="place_detail"),
    path("cities/<int:city_id>/add-place/", views.add_place_search, name="add_place"),
    path("places/<int:place_id>/edit-location/", views.edit_place_location, name="edit_place_location"),

]
