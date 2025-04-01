import json

import requests
import time
import threading

base_url: str = 'https://pokeapi.co/api/v2/'


def get_generation_pokedex(pokedex_ids: list[int]) -> dict[str, str]:
    """
    Using the Pokédex endpoint and the list of Pokédex IDs given, a new dictionary is created combining the info of
    all Pokémon found.
    :param pokedex_ids:
    :return:
    """
    url: str = base_url + 'pokedex/'

    pokedexes: list[dict] = list()
    collection: dict[str, str] = dict()

    # collect the JSON for every Pokédex from the API
    for index, pokedex_id in enumerate(pokedex_ids):
        data: dict = requests.get(url + f'{pokedex_id}/').json()
        pokedexes.append(data)

    for pokedex in pokedexes:
        # find each Pokémon's species name
        for entry in pokedex['pokemon_entries']:
            species_name: str = entry['pokemon_species']['name']

            # if the species name is not in the output dict, add it with it's "pokemon-species/" URL
            if species_name not in collection:
                collection.update({
                    species_name: entry['pokemon_species']['url']
                })

    return collection


def is_fully_evolved(pokemon_species: dict[str, str]) -> dict[str, dict]:
    result: dict[str, dict] = dict()

    for pokemon_name, species_url in pokemon_species.items():
        # will be used to add weight to how desirable a Pokémon is; increases by 0.5 for criteria met
        weight: float = 0.0

        # get the evolution chain from the URL
        chain_url: str = requests.get(species_url).json()['evolution_chain']['url']
        evolution_chain: dict | None = requests.get(chain_url).json()['chain']

        if evolution_chain["species"]["name"] == pokemon_name:
            fully_evolved = len(evolution_chain["evolves_to"]) == 0

            # If it has no further evolutions, it's fully evolved
            result.update(
                {
                    pokemon_name: {
                        'is_fully_evolved': fully_evolved,
                        'weight': 1.0 if fully_evolved else weight,
                    }
                })

            print(f'{pokemon_name} added to result')
            continue

        for evolution in evolution_chain["evolves_to"]:
            evo_chain_result: tuple[bool, float] | None = __find_pokemon_in_chain(pokemon_name, evolution, weight)

            if evo_chain_result is not None:
                result.update(
                    {
                        pokemon_name: {
                            'is_fully_evolved': evo_chain_result[0],
                            'weight': evo_chain_result[1]
                        }
                    })
                print(f'{pokemon_name} added to result')

    return result


def __find_pokemon_in_chain(pokemon_name: str, chain: dict, weight: float) -> tuple[bool, float] | None:
    """
    Moves up the chained JSON objects to find the given Pokémon. Returns if that Pokémon is fully evolved or not 
    (single-stage Pokémon count as fully evolved). If a Pokémon is partially evolved, its weight will be 0.5.
    :param pokemon_name: 
    :param chain: 
    :param weight: 
    :return: 
    """
    weight += 0.5

    if chain["species"]["name"] == pokemon_name:
        # if the Pokémon can't evolve, it's fully evolved
        fully_evolved = len(chain["evolves_to"]) == 0
        return fully_evolved, 1.0 if fully_evolved else weight

    for evolution in chain["evolves_to"]:
        # recursively climb up the chain
        result = __find_pokemon_in_chain(evolution['species']['name'], evolution, weight)
        if result is not None:
            return result

    return None


def __get_move_coverage(moves: list[dict]) -> list:
    coverage_collection: list = []

    for move in moves:
        move_url: str = move['move']['url']
        move_data: dict = requests.get(move_url).json()

        result: str = move_data['type']['name'] + ' ' + move_data['damage_class']['name']
        coverage_collection.append(result)

    return coverage_collection


def __get_most_common_move_categories(moves: list[str]) -> list[str]:
    categories: dict[str, int] = {
        'physical': 0,
        'special': 0,
        'status': 0
    }

    for move in moves:
        # get the category from the string (e.g., 'Dragon Special' returns 'special')
        category: str = move.split()[1]

        # increase the amount of times the category is present in the dict
        if category in categories:
            categories[category] += 1

    maximum: int = max(categories.values())

    # return the move categories that equal the maximum amount of appearances
    return [key for key, value in categories.items() if value == maximum]


def get_additional_info(pokemon_name: str) -> dict[str, dict]:
    output: dict[str, dict] = dict()
    wanted_data: dict = dict()

    url: str = f'{base_url}/pokemon/{pokemon_name}/'
    all_data: dict = requests.get(url).json()

    wanted_data.update({
        'type_1': all_data['types'][0]['type']['name'],
        'type_2': all_data['types'][1]['type']['name'] if len(all_data['types']) > 1 and all_data['types'][1]['type'][
            'name'] is not None else '',
        'hp': all_data['stats'][0]['base_stat'],
        'attack': all_data['stats'][1]['base_stat'],
        'defense': all_data['stats'][2]['base_stat'],
        'special-attack': all_data['stats'][3]['base_stat'],
        'special-defense': all_data['stats'][4]['base_stat'],
        'speed': all_data['stats'][5]['base_stat'],
        'abilities': [ability_dict['ability']['name'] for ability_dict in all_data['abilities']],
        'move_coverage': __get_move_coverage(all_data['moves']),
    })

    # call update again to get the data already collected from the 'move_coverage' key
    wanted_data.update({
        'highest_move_categories': __get_most_common_move_categories(wanted_data['move_coverage'])
    })

    output.update({pokemon_name: wanted_data})

    return output


if __name__ == '__main__':
    print('Collecting from pokedex(s)')
    # pokemon = get_generation_pokedex(pokedex_ids=[12, 13, 14, 15])
    pokemon = get_generation_pokedex(pokedex_ids=[2])

    time.sleep(5)

    output: dict[str, dict] = is_fully_evolved(pokemon)

    time.sleep(5)

    more_info: dict[str, dict] = dict()

    print('Getting extra info for all pokemon in pokedex(s)')
    for name in pokemon.keys():
        print(f'Getting extra info for {[name]}')
        time.sleep(0.1)
        more_info.update(get_additional_info(name))

    print(more_info)

    input('Continue >')

    print('Combining extra info to fully evolved data\n\n')
    for name in output.keys():
        output[name].update(more_info[name])

    print(f'{json.dumps(output, indent=4)}')
