import os

from utils import input_generation
from ingestion.data_collection import *


if __name__ == '__main__':
    filename: str = input('enter filename > ')

    data_path: str = os.path.join(os.getcwd(), 'data')
    file_path: str = os.path.join(data_path, filename + '.json')

    data: dict[str, dict]

    with open(file_path, 'r') as f:
        data = json.load(f)

        for pokemon_name, pokemon_data in data.items():
            print(f'Classifying role for {pokemon_name}')
            poke_data: dict[str, Any] = data[pokemon_name]
            role: str = classify_role_by_dynamic_stats(poke_data)

            print(f'{dict({'role': role})}')
            # input('> ')

            data[pokemon_name].update({'role': role})

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        print(f'Saved file "{filename}.json" to "{file_path}".')

    # print('Welcome to the ML Pokemon Team Generator!')
    # user_input_collection: tuple[str, list[int]] = input_generation()
    # collect_data(user_input_collection[0], user_input_collection[1])
