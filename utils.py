#%%
import json
import os

from config import POKEMON_DATA_DIR


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


def input_generation() -> tuple[str, list[int]]:
    # this is a dict that maps a string representation of a generation to the int(s) used for the API for Pokédex calls
    gen_to_pokedex_mapping: dict[str, list[int]] = {
        'everything': [1],
        'gen 1': [2],
        'gen 2': [7],
        'gen 3': [15],
        'gen 4': [6],
        'gen 5': [9],  # the newest Pokédex data for gen 5
        'gen 6': [12, 13, 14, 15],  # includes all 3 Kalos Pokédexes and updated Hoenn
        'gen 7': [21],
        'gen 8': [27, 28, 29],
        'gen 9': [31, 32, 33],
    }

    menu: str = make_menu(gen_to_pokedex_mapping)

    user_input: str = input(f'What generation of Pokemon would you like to generate a team for?\n'
                            f'{menu}').lower()

    selected_gens: list[int] = gen_to_pokedex_mapping.get(user_input, None)

    # if the user's input is invalid, loop until it is valid
    while selected_gens is None:
        user_input = input('\nPlease enter the generation you want as you see it appear in the list (e.g., "Gen 1" or '
                           '"Everything")\n> ')

        selected_gens = gen_to_pokedex_mapping.get(user_input, None)

    print(f'\nYou selected "{user_input}."\n')

    # create the filename based on the user's input; used later when creating files
    file_name: str = user_input.replace(' ', '_') + '_data'
    result: tuple[str, list[int]] = (file_name, selected_gens)

    return result


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


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
