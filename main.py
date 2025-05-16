import os

import utils
from ingestion.api_functions import collect_data
from ingestion.data_processing import clean_and_update_data_files
from utils import input_generation, ask_if_using_legends, ask_if_only_using_babies, ask_for_team_preferences
from learning.team_builder import TeamBuilder

if __name__ == '__main__':
    utils.clear_screen()

    # ask for and collect data using API calls
    print('Welcome to the ML Pokémon Team Generator!\n')
    filename, pokedex_ids = input_generation()

    collect_data(filename, pokedex_ids)

    clean_and_update_data_files()

    print('\n\nAll data files have been cleaned/updated.')
    input('Press "Enter" to continue > ')

    utils.clear_screen()

    using_babies: bool = ask_if_only_using_babies()
    using_legends: bool = False

    if not using_babies:
        using_legends = ask_if_using_legends()

    preferences: dict[str, bool] = ask_for_team_preferences()

    data_path: str = os.path.join(os.getcwd(), 'data', 'pokemon_data')
    file_path: str = os.path.join(data_path, filename + '.json')

    tb: TeamBuilder = TeamBuilder(using_babies, using_legends, file_path, preferences)

    input('\nPress "Enter" to continue > ')
    utils.clear_screen()

    print('Generating a team...\n')

    tb.generate_team()
