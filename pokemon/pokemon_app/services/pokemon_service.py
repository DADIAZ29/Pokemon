import requests
from ..models import Pokemon, PokemonSprites

API_URL = "https://pokeapi.co/api/v2/pokemon/"
TIMEOUT_SECONDS = 15


def get_pokemon(name):
    try:
        response = requests.get(f"{API_URL}{name}", timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Error consultando pokemon {name}: {exc}")
        return None
    return response.json()


def get_pokemons(offset=0, limit=20):
    try:
        response = requests.get(
            f"{API_URL}?offset={offset}&limit={limit}",
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Error consultando lista de pokemons (offset={offset}): {exc}")
        return []
    return response.json().get("results", [])


def load_pokemons():
    try:
        response = requests.get(f"{API_URL}?offset=0&limit=1", timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException as exc:
        return f"No se pudo obtener la cantidad total de pokémon de la API: {exc}"

    total_pokemon = response.json().get("count", 0)
    if not total_pokemon:
        return "No se pudo obtener la cantidad total de pokémon de la API."

    loaded_count = Pokemon.objects.count()
    if loaded_count >= total_pokemon:
        return f"Pokemons ya cargados: {loaded_count}"

    offset = 0
    limit = 100
    total_cargados = 0
    seen_names = set(Pokemon.objects.values_list("name", flat=True))

    while offset < total_pokemon:
        pokemons_responses = get_pokemons(
            offset=offset,
            limit=min(limit, total_pokemon - offset)
        )
        if not pokemons_responses:
            break

        for pr in pokemons_responses:
            name = pr["name"]
            if name in seen_names:
                continue

            pokemon = get_pokemon(name)
            if not pokemon:
                continue

            sprite_data = pokemon.get("sprites", {})
            sprites, _ = PokemonSprites.objects.get_or_create(
                front_default=sprite_data.get("front_default") or "",
                back_default=sprite_data.get("back_default") or "",
                front_shiny=sprite_data.get("front_shiny") or "",
                back_shiny=sprite_data.get("back_shiny") or "",
            )

            Pokemon.objects.get_or_create(
                id=pokemon.get("id"),
                name=pokemon.get("name"),
                height=pokemon.get("height"),
                weight=pokemon.get("weight"),
                order=pokemon.get("order"),
                sprites=sprites,
            )

            seen_names.add(pokemon.get("name"))
            total_cargados += 1
            print("Cargando ", pokemon.get("id"), pokemon.get("name"))

        offset += len(pokemons_responses)

    return f"Pokemons cargados: {Pokemon.objects.count()} (total insertados: {total_cargados})"
