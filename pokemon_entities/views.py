import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def get_pokemon_img_url(request, pokemon):
    if pokemon.img:
        return request.build_absolute_uri(pokemon.img.url)
    else:
        return DEFAULT_IMAGE_URL


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons_entities = PokemonEntity.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            get_pokemon_img_url(request, pokemon_entity.pokemon)
        )
    
    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': get_pokemon_img_url(request, pokemon),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon_object = Pokemon.objects.get(id=int(pokemon_id))
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    pokemon_img_url = get_pokemon_img_url(request, pokemon_object)

    pokemon_entities = pokemon_object.entities.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_img_url
        )

    pokemon = {
        'img_url': pokemon_img_url,
        'title_ru': pokemon_object.title,
        'title_en': pokemon_object.title_en,
        'title_jp': pokemon_object.title_jp,
        'description': pokemon_object.description,
    }
    if pokemon_object.parent:
        pokemon['previous_evolution'] = {
            'title_ru': pokemon_object.parent.title,
            'pokemon_id': pokemon_object.parent.id,
            'img_url': get_pokemon_img_url(request, pokemon_object.parent),
        }
    pokemon_children = pokemon_object.children.all()
    if pokemon_children:
        pokemon_child = pokemon_children[0]
        pokemon['next_evolution'] = {
            'title_ru': pokemon_child.title,
            'pokemon_id': pokemon_child.id,
            'img_url': get_pokemon_img_url(request, pokemon_child),
        }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
