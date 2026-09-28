import requests
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .forms import PokemonForm, PokemonSpritesForm
from .models import Pokemon
from .services.pokemon_service import load_pokemons


def pokemon_list(request):
    try:
        total_api = requests.get("https://pokeapi.co/api/v2/pokemon/?offset=0&limit=1").json().get("count", 0)
    except Exception:
        total_api = 0

    if total_api and Pokemon.objects.count() < total_api:
        load_pokemons()

    pokemons = Pokemon.objects.order_by("id")
    paginator = Paginator(pokemons, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    current = page_obj.number
    total_pages = paginator.num_pages

    if total_pages <= 7:
        page_numbers = list(range(1, total_pages + 1))
    elif current <= 4:
        page_numbers = [1, 2, 3, 4, 5, "...", total_pages]
    elif current >= total_pages - 3:
        page_numbers = [1, "...", total_pages - 4, total_pages - 3, total_pages - 2, total_pages - 1, total_pages]
    else:
        page_numbers = [1, "...", current - 1, current, current + 1, "...", total_pages]

    return render(request, "pokemon/pokemon_list.html", {
        "pokemons": page_obj,
        "page_obj": page_obj,
        "page_numbers": page_numbers,
    })


def pokemon_details(request, id):
    pokemon = get_object_or_404(Pokemon, id=id)
    return render(request, "pokemon/pokemon_details.html", {"pokemon": pokemon})


def pokemon_create(request):
    if request.method == "POST":
        form = PokemonForm(request.POST)
        sprites_form = PokemonSpritesForm(request.POST)

        if form.is_valid() and sprites_form.is_valid():
            sprite = sprites_form.save()
            pokemon = form.save(commit=False)
            pokemon.sprites = sprite
            pokemon.save()
            messages.success(request, "Pokémon creado correctamente.")
            return redirect("pokemon_list")
    else:
        form = PokemonForm()
        sprites_form = PokemonSpritesForm()

    return render(request, "pokemon/pokemon_form.html", {
        "form": form,
        "sprites_form": sprites_form,
        "pokemon": None,
    })


def pokemon_update(request, id):
    pokemon = get_object_or_404(Pokemon, id=id)

    if request.method == "POST":
        form = PokemonForm(request.POST, instance=pokemon)
        sprites_form = PokemonSpritesForm(request.POST, instance=pokemon.sprites)

        if form.is_valid() and sprites_form.is_valid():
            sprites_form.save()
            form.save()
            messages.success(request, "Pokémon actualizado correctamente.")
            return redirect("pokemon_list")
    else:
        form = PokemonForm(instance=pokemon)
        sprites_form = PokemonSpritesForm(instance=pokemon.sprites)

    return render(request, "pokemon/pokemon_form.html", {
        "form": form,
        "sprites_form": sprites_form,
        "pokemon": pokemon,
    })


def pokemon_delete(request, id):
    pokemon = get_object_or_404(Pokemon, id=id)

    if request.method == "POST":
        pokemon.sprites.delete()
        pokemon.delete()
        messages.success(request, "Pokémon eliminado correctamente.")
        return redirect("pokemon_list")

    return render(request, "pokemon/pokemon_confirm_delete.html", {"pokemon": pokemon})
