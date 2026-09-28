from django.urls import path
from .views import *

urlpatterns = [
    path("", pokemon_list, name="pokemon_list"),
    path("crear/", pokemon_create, name="pokemon_create"),
    path("<int:id>/", pokemon_details, name="pokemon_details"),
    path("<int:id>/editar/", pokemon_update, name="pokemon_update"),
    path("<int:id>/eliminar/", pokemon_delete, name="pokemon_delete"),
]