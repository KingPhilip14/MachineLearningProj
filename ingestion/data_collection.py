#%%
import os
from typing import Any
import json
import requests
import time

from tqdm import tqdm
from utils import file_exists, save_json_file

base_url: str = 'https://pokeapi.co/api/v2/'


def get_generation_pokedex(pokedex_ids: list[int]) -> dict[str, str]:
    """
    Using the Pokédex endpoint and the list of Pokédex IDs given, a new dictionary is created combining the info of
    all Pokémon found. The first step in collecting data.
    :param pokedex_ids:
    :return:
    """
    url: str = base_url + 'pokedex/'

    pokedexes: list[dict] = list()
    collection: dict[str, str] = dict()

    print('Collecting Pokédex info for the selected generation...')

    # collect the JSON for every Pokédex from the API
    for index, pokedex_id in enumerate(pokedex_ids):
        data: dict = requests.get(url + f'{pokedex_id}/').json()
        pokedexes.append(data)

    for pokedex in tqdm(pokedexes):
        # find each Pokémon's species name
        for entry in pokedex['pokemon_entries']:
            species_name: str = entry['pokemon_species']['name']

            # if the species name is not in the output dict, add it with it's "pokemon-species/" URL
            if species_name not in collection:
                collection.update({
                    species_name: entry['pokemon_species']['url']
                })

    print('Pokédex info collected.')

    return collection


def get_species_data(pokemon_species: dict[str, str]) -> dict[str, dict]:
    """
    Given the data of a Pokémon species, extra information is gathered, such as if the Pokémon is fully evolved
    and if it's a legendary or mythical. The third step in the data collection.
    :param pokemon_species:
    :return:
    """
    print('\nAdding "is_fully_evolved" to all collected Pokémon...\n')

    result: dict[str, dict] = dict()

    for pokemon_name, species_url in tqdm(pokemon_species.items()):
        # will be used to add weight to how desirable a Pokémon is; increases by 0.5 for criteria met
        evo_weight: float = 0.0

        species_json: dict = requests.get(species_url).json()

        is_legend_or_mythical: bool = species_json['is_legendary'] or species_json['is_mythical']

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
                        'evo_weight': 1.0 if fully_evolved else evo_weight,
                        'is_legend_or_mythical': is_legend_or_mythical
                    }
                })

            # print(f'{pokemon_name} added to result')
            continue

        for evolution in evolution_chain["evolves_to"]:
            evo_chain_result: tuple[bool, float] | None = __find_pokemon_in_chain(pokemon_name, evolution, evo_weight)

            if evo_chain_result is not None:
                result.update(
                    {
                        pokemon_name: {
                            'is_fully_evolved': evo_chain_result[0],
                            'evo_weight': evo_chain_result[1],
                            'is_legend_or_mythical': is_legend_or_mythical
                        }
                    })
                # print(f'{pokemon_name} added to result')

    return result


def __find_pokemon_in_chain(pokemon_name: str, chain: dict, evo_weight: float) -> tuple[bool, float] | None:
    """
    Moves up the chained JSON objects to find the given Pokémon. Returns if that Pokémon is fully evolved or not 
    (single-stage Pokémon count as fully evolved). If a Pokémon is partially evolved, its weight will be 0.5.
    :param pokemon_name: 
    :param chain: 
    :param evo_weight:
    :return: 
    """
    evo_weight += 0.5

    if chain["species"]["name"] == pokemon_name:
        # if the Pokémon can't evolve, it's fully evolved
        fully_evolved = len(chain["evolves_to"]) == 0
        return fully_evolved, 1.0 if fully_evolved else evo_weight

    for evolution in chain["evolves_to"]:
        # recursively climb up the chain
        result = __find_pokemon_in_chain(evolution['species']['name'], evolution, evo_weight)
        if result is not None:
            return result

    return None


def __get_move_coverage(moves: list[dict]) -> set:
    coverage_collection: set = set()

    for move in moves:
        move_url: str = move['move']['url']
        move_data: dict = requests.get(move_url).json()

        result: str = move_data['type']['name'] + ' ' + move_data['damage_class']['name']
        coverage_collection.add(result)

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


def __get_additional_info(pokemon_name: str) -> dict[str, dict]:
    output: dict[str, dict] = dict()
    wanted_data: dict = dict()

    url: str = f'{base_url}/pokemon/{pokemon_name}/'

    response = requests.get(url)

    if response.status_code != 200:
        print(f'\nCould not collect data for "{pokemon_name}". API response text: "{response.text}"\n')
        return {pokemon_name: None}

    all_data: dict = response.json()

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
        'move_coverage': list(__get_move_coverage(all_data['moves'])),
    })

    # call update again to get the data already collected from the 'move_coverage' key
    wanted_data.update({
        'highest_move_categories': __get_most_common_move_categories(wanted_data['move_coverage'])
    })

    output.update({pokemon_name: wanted_data})

    return output


def add_extra_info_to_data(pokemon_data: dict[str, dict]) -> dict[str, dict]:
    """
    Adds the additional information for a Pokémon needed and returns a dict with the info. The second step
    in data collection.
    :param pokemon_data:
    :return:
    """
    print('\nGetting extra info for all pokemon in Pokédex(s)\n')

    more_info: dict[str, dict] = dict()

    for pokemon_name in tqdm(pokemon_data.keys()):
        more_info.update(__get_additional_info(pokemon_name))

    return more_info


def combine_data(add_to: dict[str, dict], more_info: dict[str, dict]) -> None:
    """
    Adds the data from more_info to the given add_to dict. The final step in data collection,
    :param add_to:
    :param more_info:
    :return:
    """
    print('Combining extra info to fully evolved data\n\n')
    for pokemon_name in add_to.keys():
        if more_info[pokemon_name] is None:
            add_to.pop(pokemon_name)
            print(f'Removed {pokemon_name} from data since the additional gathered data cannot be accessed.')
            continue

        add_to[pokemon_name].update(more_info[pokemon_name])


def collect_data(filename: str, pokedex_ids: list[int]) -> None:
    """
    Using the filename and given Pokédex IDs, it is first determined if the given file exists. If not, methods are
    called to start the data collection. The program will pause for a few seconds after each step to not
    receive a timeout by the API.
    :param filename:
    :param pokedex_ids:
    :return:
    """
    if file_exists(filename):
        print(f'The file "{filename}" already exists containing the Pokédex data requested. '
              f'A new one will not be created.')
        return

    pause_time: int = 10
    pokemon: dict[str, str] = get_generation_pokedex(pokedex_ids)

    print(f'\nPausing for {pause_time} seconds to not time out during data collection. Please wait...')
    time.sleep(pause_time)

    output: dict[str, dict] = get_species_data(pokemon)

    print(f'\nPausing again for {pause_time} seconds to not time out during data collection. Please wait...')
    time.sleep(pause_time)

    extra_info: dict[str, dict] = add_extra_info_to_data(output)

    combine_data(output, extra_info)

    save_json_file(output, filename, False)


def clean_data(filename: str) -> None:
    """
    Looks at every Pokémon stored in a JSON file. If the entry is missing the 'hp' key, the data is identified as
    malformed as is removed.
    :return:
    """
    print('\n\n---------------------------------------------------------')
    data_path: str = os.path.join(os.getcwd(), 'data')
    file_path: str = os.path.join(data_path, filename)

    with open(file_path, 'r') as f:
        data = json.load(f)

    to_remove: list[str] = []
    modified: bool = False

    for pokemon_name, pokemon_data in data.items():
        if data[pokemon_name].get('hp', None) is None:
            modified = True
            to_remove.append(pokemon_name)

    for name in to_remove:
        data.pop(name)
        print(f'Removed "{name}" because its data was incomplete.')

    if modified:
        save_json_file(data, filename, True)
        return

    print(f'No malformed/incomplete data was found in {filename}')


def __classify_role_by_dynamic_stats(data: dict[str, Any]) -> str:
    move_categories: list[str] = ['highest_move_categories']

    hp = data['hp']
    atk = data['attack']
    defense = data['defense']
    spa = data['special-attack']
    sp_def = data['special-defense']
    spd = data['speed']

    # The base stat total of the Pokémon
    bst = atk + spa + spd + hp + defense + sp_def

    # Percentage thresholds based on total stats
    high_stat_threshold = 0.19 * bst  # stat is considered high if ≥19% of total; 19 to help with better classifications
    balanced_offense_margin = 0.05 * bst  # if atk/spa are close within 5% of BST

    # return versatile immediately if all stats are equal
    if hp == atk == defense == spa == sp_def == spd:
        return 'versatile'

    # Wall / tank detection
    if hp >= 0.20 * bst:
        if defense >= 0.18 * bst and sp_def < 0.15 * bst:
            return 'physical wall'
        elif sp_def >= 0.18 * bst and defense < 0.15 * bst:
            return 'special wall'
        elif defense >= 0.16 * bst and sp_def >= 0.16 * bst:
            return 'mixed wall'

    # Classified as a tank only if both defenses are high
    if defense >= high_stat_threshold and sp_def >= high_stat_threshold:
        return 'tank'

    # Utility/support detection
    if move_categories == ['status'] and atk < high_stat_threshold and spa < high_stat_threshold:
        return 'utility/support'

    # Sweeper detection (speed + high offense)
    if spd >= 0.18 * bst:
        if atk > spa and atk >= high_stat_threshold:
            return 'physical sweeper'
        elif spa > atk and spa >= high_stat_threshold:
            return 'special sweeper'

    # Attacker roles
    if atk >= high_stat_threshold and atk > spa + balanced_offense_margin:
        return 'physical attacker'
    elif spa >= high_stat_threshold and spa > atk + balanced_offense_margin:
        return 'special attacker'
    elif abs(atk - spa) <= balanced_offense_margin:
        return 'mixed attacker'

    # Fallback
    return 'versatile'


def define_pokemon_role(filename: str) -> None:
    """
    By calling another method to define a Pokémon's role, it's then saved in the JSON file for each Pokémon stored.
    """
    data_path: str = os.path.join(os.getcwd(), 'data')
    file_path: str = os.path.join(data_path, filename)

    data: dict[str, dict]

    print('Classifying roles...')

    with open(file_path, 'r') as f:
        data = json.load(f)

        for pokemon_name, pokemon_data in data.items():
            poke_data: dict[str, Any] = data[pokemon_name]
            role: str = __classify_role_by_dynamic_stats(poke_data)

            data[pokemon_name].update({'role': role})

    save_json_file(data, filename, True)

    print(f'Pokemon roles have been saved to {filename}')


def add_bst(filename: str) -> None:
    """
    Calculates a Pokemon's base stat total (BST) by finding the sum of all stats (HP, attack, defense, etc.).
    """
    data_path: str = os.path.join(os.getcwd(), 'data')
    file_path: str = os.path.join(data_path, filename)

    data: dict[str, dict]

    print('Calculating BSTs...')

    with open(file_path, 'r') as f:
        data = json.load(f)

        for pokemon_name, pokemon_data in data.items():
            poke_data: dict[str, Any] = data[pokemon_name]

            hp = poke_data['hp']
            atk = poke_data['attack']
            defense = poke_data['defense']
            spa = poke_data['special-attack']
            spd_def = poke_data['special-defense']
            spd = poke_data['speed']

            # The base stat total of the Pokémon
            bst: int = atk + spa + spd + hp + defense + spd_def

            data[pokemon_name].update({'bst': bst})

    save_json_file(data, filename, True)

    print(f'Base stat totals have been saved to {filename}')


def clean_and_update_data_files() -> None:
    """
    Iterates through every file in the /data folder to clean and update the stored data.
    :return:
    """
    data_path: str = os.path.join(os.getcwd(), 'data')

    for filename in os.listdir(data_path):
        # clean data
        clean_data(filename)
        define_pokemon_role(filename)
        add_bst(filename)

# # if __name__ == '__main__':
#     # pokemon = get_generation_pokedex(pokedex_ids=[12, 13, 14, 15])
# #%%
# pokemon: dict[str, str] = get_generation_pokedex(pokedex_ids=[2])
#
# time.sleep(5)
#
# #%%
# output: dict[str, dict] = is_fully_evolved(pokemon)
#
# time.sleep(5)
#
# #%%
# extra_info: dict[str, dict] = add_extra_info_to_data(output)
#
# # for name in pokemon.keys():
# #     print(f'Getting extra info for {[name]}')
# #     time.sleep(0.1)
# #     more_info.update(get_additional_info(name))
#
# # print(more_info)
#
# # add_extra_info_to_data(output)
#
# #%%
# combine_data(output, extra_info)
# # print('Combining extra info to fully evolved data\n\n')
# # for name in output.keys():
# #     output[name].update(extra_info[name])
#
# print(f'{json.dumps(output, indent=4)}')
#
# #%%
# save_json_file(output, 'gen_1_data')
