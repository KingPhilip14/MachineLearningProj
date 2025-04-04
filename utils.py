import json
import os


def input_generation() -> list[int]:
    # this is a dict that maps a string representation of a generation to the int(s) used for the API for pokedex calls
    gen_to_pokedex_mapping: dict[str, list[int]] = {
        'everything': [1],
        'gen 1': [2],
        'gen 2': [7],
        'gen 3': [15],
        'gen 4': [6],
        'gen 5': [9],
        'gen 6': [12, 13, 14, 15],  # includes Kalos and updated Hoenn
        'gen 7': [21],
        'gen 8': [27, 28, 29],
        'gen 9': [31, 32, 33],
    }

    menu: str = make_menu(gen_to_pokedex_mapping)

    user_input: str = input(f'What generation of Pokemon would you like to generate a competitive team for?\n'
                            f'{menu}').lower()

    selected_gen: list[int] = gen_to_pokedex_mapping.get(user_input, None)

    # if the user's input is invalid, loop until it is valid
    while selected_gen is None:
        user_input = input('\nPlease enter the generation you want as you see it appear in the list (e.g., "Gen 1" or '
                           '"Everything")\n> ')

        selected_gen = gen_to_pokedex_mapping.get(user_input, None)

    print(f'You selected "{user_input}".')


def make_menu(options: dict[str, list[int]]) -> str:
    output: str = ''

    for index, key in enumerate(options, start=1):
        output += f'{index}) {key[0].upper() + key[1:]}\n'

    output += '\n> '

    return output


def save_json_file(data: dict[str, dict], filename: str) -> None:
    """
    Uses the given dictionary to save the data in a JSON file.
    :param data:
    :param filename:
    """
    data_path: str = os.path.join(os.getcwd(), 'data')
    file_path: str = os.path.join(data_path, filename + '.json')

    if os.path.exists(file_path):
        print(f'The file "{filename}" already exists. A new one will not be created.')
        return

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    data_dict: dict = {
        'First': 1,
        'Second': 2,
        'Third': 3,
        'Fourth': 4,
        'Fifth': 5,
    }

    new_data: dict = {
        'Sixth': 6,
        'Seventh': 7,
        'Eighth': 8,
        'Ninth': 9,
        'Tenth': 10,
    }
    save_json_file(data_dict, 'test')
