#%%
import json
import os


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


def save_json_file(data: dict[str, dict], filename: str, exists: bool) -> None:
    """
    Uses the given dictionary to save the data in a JSON file.
    :param data:
    :param filename:
    """
    data_path: str = os.path.join(os.getcwd(), 'data', 'pokemon_data')

    filename = filename + '.json' if not exists else filename

    file_path: str = os.path.join(data_path, filename)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

        print(f'Saved new file "{filename}" to "{file_path}".') if exists else \
            print(f'Replaced data in file {filename}')


def file_exists(filename: str) -> bool:
    data_path: str = os.path.join(os.getcwd(), 'data', 'pokemon_data')
    file_path: str = os.path.join(data_path, filename + '.json')

    print(f'Filepath: "{file_path}"')

    return os.path.exists(file_path)
