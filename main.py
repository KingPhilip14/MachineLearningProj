import os

import utils
from utils import input_generation, ask_if_using_legends, asking_if_using_little_cup, ask_for_team_composition
from backend.ml.learning.team_builder import TeamBuilder

if __name__ == '__main__':
    # utils.clear_screen()

    print('Welcome to the ML Pokémon Team Generator!\n')
    filename, pokedex_ids = input_generation('What generation of Pokemon would you like to generate a team for?')

    input('Press "Enter" to continue > ')

    utils.clear_screen()

    using_little_cup: bool = asking_if_using_little_cup()
    using_legends: bool = False

    if not using_little_cup:
        using_legends = ask_if_using_legends()

    composition: str = ask_for_team_composition()

    data_path: str = os.path.join(os.getcwd(), 'data', 'pokemon_data')
    file_path: str = os.path.join(data_path, filename + '.json')

    tb: TeamBuilder = TeamBuilder(using_little_cup, using_legends, file_path, composition)

    input('\nPress "Enter" to continue > ')
    utils.clear_screen()

    print('Generating a team...\n')

    tb.generate_team()
