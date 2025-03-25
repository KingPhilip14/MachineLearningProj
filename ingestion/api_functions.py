import json
import requests
import os

base_url: str = 'https://pokeapi.co/api/v2/'


def get_generation_pokedex(pokedex_ids: list[int]) -> dict[str, str]:
    """
    Using the Pokedex endpoint and the list of Pokedex IDs given, a new dictionary is created combining the info of
    all Pokemon found.
    :param pokedex_ids:
    :return:
    """
    url: str = base_url + 'pokedex/'

    pokedexes: list[dict] = list()
    output: dict[str, str] = dict()

    for size, pokedex_id in enumerate(pokedex_ids):
        data: dict = requests.get(url + f'{pokedex_id}/').json()
        pokedexes.append(data)

    for pokedex in pokedexes:
        for entry in pokedex['pokemon_entries']:
            species_name: str = entry['pokemon_species']['name']

            if species_name not in output:
                output.update({
                    species_name: entry['pokemon_species']['url']
                })

    return output


def is_fully_evolved():
    pass


# output = get_generation_pokedex(pokedex_ids=[12, 13, 14, 15])
#
# print(output)
