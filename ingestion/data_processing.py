import json
import os

from typing import Any

from config import POKEMON_DATA_DIR, EXTRA_DATA_DIR
from utils import save_json_file


def clean_and_update_pokemon_data_files(filename) -> None:
    """
    Calls the helper methods to add extra data as necessary.
    :return:
    """
    __define_pokemon_role(filename)
    __add_type_matchups(filename)

    print('\nAll data files have been cleaned/updated.')


def __clean_data(filename: str):
    """
    Looks at every Pokémon stored in a JSON file. If the entry is missing the 'hp' key, the data is identified as
    malformed as is removed.
    :return:
    """
    print('\n---------------------------------------------------------')
    file_path: str = os.path.join(POKEMON_DATA_DIR, filename)

    with open(file_path, 'w') as f:
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
            json.dump(data, f, indent=4)
            return

        print(f'No malformed/incomplete data was found in {filename}\n')

    return


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


def __define_pokemon_role(filename: str) -> None:
    """
    By calling another method to define a Pokémon's role, it's then saved in the JSON file for each Pokémon stored.
    """
    file_path: str = os.path.join(POKEMON_DATA_DIR, filename)

    data: dict[str, dict]

    print('Classifying roles...')

    with open(file_path, 'r') as f:
        data = json.load(f)
        f.close()

    with open(file_path, 'w') as f:
        for pokemon_name, pokemon_data in data.items():
            poke_data: dict[str, Any] = data[pokemon_name]
            role: str = __classify_role_by_dynamic_stats(poke_data)

            data[pokemon_name].update({'role': role})

        json.dump(data, f, indent=4)
        f.close()

    # save_json_file(data, filename)

    print(f'Pokemon roles have been saved to {filename}\n')


def __add_bst(filename: str) -> None:
    """
    Calculates a Pokémon's base stat total (BST) by finding the sum of all stats (HP, attack, defense, etc.).
    """
    file_path: str = os.path.join(POKEMON_DATA_DIR, filename)

    data: dict[str, dict]

    print('Calculating BSTs...')

    with open(file_path, 'r') as f:
        data = json.load(f)
        f.close()

    with open(file_path, 'w') as f:
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

        json.dump(data, f, indent=4)
        f.close()

    # save_json_file(data, filename)

    print(f'Base stat totals have been saved to {filename}\n')


def __add_type_matchups(filename: str) -> None:
    file_path: str = os.path.join(POKEMON_DATA_DIR, filename)

    data: dict[str, dict]

    print('Calculating type matchups...')

    with open(file_path, 'r') as f:
        data = json.load(f)
        f.close()

    with open(file_path, 'w') as f:
        for pokemon_name, pokemon_data in data.items():
            matchups: dict[str, float] = __calculate_type_effectiveness(pokemon_data['type_1'], pokemon_data['type_2'])
            weaknesses: dict[str, float] = {t: val for t, val in matchups.items() if val > 1.0}
            resistances: dict[str, float] = {t: val for t, val in matchups.items() if val < 1.0}

            data[pokemon_name].update({'weaknesses': weaknesses})
            data[pokemon_name].update({'resistances': resistances})

        json.dump(data, f, indent=4)
        f.close()

    # save_json_file(data, filename)

    print(f'Type effectiveness and weaknesses have been added to {filename}\n')


def __calculate_type_effectiveness(primary_type: str, secondary_type: str) -> dict[str, float]:
    """
    By using a given Pokémon's primary and potential secondary typing, a list is created to determine how many
    weaknesses the Pokémon has.
    :param primary_type:
    :param secondary_type:
    :return:
    """
    type_chart: dict[str, dict[str, float]]

    file_path: str = os.path.join(EXTRA_DATA_DIR, 'defensive_type_chart.json')

    # read in the type chart data
    with open(file_path, 'r') as f:
        type_chart = json.load(f)
        f.close()

    types: dict[str, float] = {t: 1.0 for t in type_chart.keys()}

    for current_type in [primary_type, secondary_type]:
        if current_type == '':
            continue

        for t in types.keys():
            # whatever the current type is, multiply it by the effectiveness found in the type_chart
            effectiveness: float = type_chart[current_type].get(t, 1.0)
            types[t] *= effectiveness

    return types
