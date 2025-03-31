def input_generation() -> list[int]:
    # this is a dict that maps a string representation of a generation to the int(s) used for the API for pokedex calls
    gen_to_pokedex_mapping: dict[str, list[int]] = {
        'Everything': [1],
        'Gen 1': [2],
        'Gen 2': [7],
        'Gen 3': [15],
        'Gen 4': [6],
        'Gen 5': [9],
        'Gen 6': [12, 13, 14, 15],  # includes kalos and then updated hoenn
        'Gen 7': [21],
        'Gen 8': [27, 28, 29],
        'Gen 9': [31, 32, 33],
    }

    menu: str = make_menu(gen_to_pokedex_mapping)

    user_input: str = input(f'What generation of Pokemon would you like to generate a competitive team for?\n'
                            'NOTE: inputs are case sensitive and must be entered as shown.\n'
                            f'{menu}')

    selected_gen: list[int] = gen_to_pokedex_mapping.get(user_input, None)

    # if the user's input is invalid, loop until it is valid
    while selected_gen is None:
        user_input = input('Please enter the generation you want as you see it appear in the list (e.g., "Gen 1" or '
                           '"Everything").')

        selected_gen = gen_to_pokedex_mapping.get(user_input, None)

    print(f'You selected "{user_input}".')


def make_menu(options: dict) -> str:
    output: str = ''

    for index, key in enumerate(options, start=1):
        output += f'{index}) {key}\n'

    output += '\n> '

    return output
