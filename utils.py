# %%
import json
import os

from config import (EXTRA_DATA_DIR, POKEMON_DATA_DIR, ERR_SPRITES_DIR, POKEMON_SPRITES_DIR, TYPE_SPRITES_DIR,
                    GEN_TO_POKEDEX_MAP, EXTRA_DATA_DIR)


def gen_roman_converter(filename: str) -> str:
    """
    Takes the filename of the generation to use converts it to a string with roman numeral representation. If
    "everything" was selected, return an empty string.
    :param filename:
    :return:
    """
    if filename.__contains__('everything'):
        return ''

    gen_num: int = int(filename.split('_')[1])

    roman_map: dict[int, str] = {1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v', 6: 'vi', 7: 'vii', 8: 'viii', 9: 'ix',
                                 10: 'x'}

    return f'generation-{roman_map[gen_num]}'


def roman_to_int(roman: str) -> int:
    """
    Given a roman numeral, it is converted to a standard integer. If the given roman numeral is not in the dictionary,
    -1 is returned.
    :param roman:
    """
    roman_map: dict[str, int] = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5, 'vi': 6, 'vii': 7, 'viii': 8, 'ix': 9,
                                 'x': 10}

    return roman_map.get(roman, -1)


def input_generation(prompt: str) -> tuple[str, list[int]]:
    menu: str = make_menu(GEN_TO_POKEDEX_MAP)

    user_input: str = input(f'{prompt}\n{menu}').lower()

    selected_gens: list[int] = GEN_TO_POKEDEX_MAP.get(user_input, None)

    # if the user's input is invalid, loop until it is valid
    while selected_gens is None:
        user_input = input('\nPlease enter the generation you want as you see it appear in the list (e.g., "Gen 1" or '
                           '"National")\n> ')

        selected_gens = GEN_TO_POKEDEX_MAP.get(user_input, None)

    print(f'\nYou selected "{user_input}."\n')

    # create the filename based on the user's input; used later when creating files
    file_name: str = user_input.replace(' ', '_') + '_data'
    result: tuple[str, list[int]] = (file_name, selected_gens)

    return result


def get_generation_num(filename: str) -> int:
    """
    Returns the generation number from the given filename. If the filename contains "everything," -1 is returned
    instead.
    :param filename:
    """
    if filename.__contains__('national'):
        return -1

    return int(filename.split('_')[1])


def make_menu(options: dict[str, list[int]]) -> str:
    output: str = ''

    for key in options:
        output += f'- {key[0].upper() + key[1:]}\n'

    output += '\n> '

    return output


def save_json_file(data: dict[str, dict], filename: str) -> None:
    """
    Uses the given dictionary to save the data in a JSON file.
    :param data:
    :param filename:
    """
    filename = filename + '.json'

    exists: bool = pokemon_data_file_exists(filename)

    file_path: str = os.path.join(POKEMON_DATA_DIR, filename)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

        print(f'Saved new file "{filename}" to "{file_path}".') if exists else \
            print(f'Replaced data in file {filename}')


def pokemon_data_file_exists(filename: str) -> bool:
    file_path: str = os.path.join(POKEMON_DATA_DIR, filename + '.json')

    return os.path.exists(file_path)

def create_dirs() -> None:
    dirs: list[str] = [EXTRA_DATA_DIR, POKEMON_DATA_DIR, ERR_SPRITES_DIR, POKEMON_SPRITES_DIR, TYPE_SPRITES_DIR]

    print(f'Attempting to make data directories...')
    created: bool = False

    for directory in dirs:
        if os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            created = True
            print(f'Created directory "{directory}"')

    input('Directories created. Press enter to continue >' if created
          else print('Directories were already created. Press enter to continue >'))
    clear_screen()


def ask_if_using_legends() -> bool:
    user_input: str = input('\nWould you like to potentially use legendaries in your team composition?\n(y/n) > ')

    return user_input.lower() in ['y', 'yes']


def ask_if_only_using_babies() -> bool:
    user_input: str = input('Would you like to generate a team for the Little Cup format '
                            '(only unevolved Pokémon are used; legendaries will not be used)\n(y/n) > ')

    return user_input.lower() in ['y', 'yes']


def ask_for_team_preferences() -> dict[str, bool]:
    """
    Asks the user for how they want their team composition. They can choose between a more offensive, defensive, or
    balanced composition.

    When asking the user, each question will be asked until they say yes to one of the compositions. If they say no
    to all three, the default composition will be the balanced composition.
    """
    preferences: dict[str, bool] = {
        'more_offensive': False,
        'more_defensive': False,
        'more_balanced': False
    }

    user_input: str = input('\nWould you like a more offensive team composition?\n(y/n) > ')

    if user_input.lower() in ['y', 'yes']:
        preferences['more_offensive'] = True
        return preferences

    user_input = input('\nWould you like a more defense team composition instead?\n(y/n) > ')

    if user_input.lower() in ['y', 'yes']:
        preferences['more_defensive'] = True
        return preferences

    print('\nThe balanced composition will be used by default.')
    preferences['more_balanced'] = True

    return preferences


def get_role_description(role: str) -> str:
    """
    Returns a description for the given role of a Pokémon. If an invalid role is given, a default description is
    returned.
    :param role:
    """
    descriptions: dict[str, str] = {
        'Physical Sweeper': 'A fast, hard-hitting attacker that uses their astounding physical damage.',
        'Special Sweeper': 'An attacker excelling in special damage and speed to overwhelm the opponent.',
        'Physical Attacker': 'An attacker that uses their reliable physical damage.',
        'Special Attacker': 'Focuses on dealing special damage.',
        'Mixed Attacker': 'Provides flexibility by being capable of attacking both physically and specially.',
        'Physical Wall': 'Eats physical hits without taking much of a scratch. Both HP and Defense are notably high.',
        'Special Wall': 'Absorbs special attacks, walling out special attackers. Both HP and Special Defense are '
                        'notably high.',
        'Bulky Wall': 'Can take both physical and damage well. Both Defense and Special Defense are notably high, '
                      'but HP may not be.',
        'Speedster': 'Focuses on speed, providing a variety of uses like maintaining momentum, revenge kills, or '
                     'occasional utility and setup.',
        'Utility/Support': 'Excels at using status moves, setup, or field control moves to aid the rest of the team.',
        'Bulky': 'Provides a general form of tankiness without having high defenses thanks to its high HP.',
        'Versatile': 'A flexible role that provides relatively balanced stats and can have unpredictable usage.',
        'Eviolite User': 'While not fully evolved, an Eviolite will make this Pokémon as bulky as another Wall '
                         'archetype, providing unique usage.',
    }

    return descriptions.get(role, 'A Pokémon with a lot of potential to fit on different teams.')


def calculate_type_effectiveness(primary_type: str, secondary_type: str) -> dict[str, float]:
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


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
