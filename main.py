from ingestion.api_functions import collect_data
from ingestion.data_processing import clean_and_update_data_files
from utils import input_generation


if __name__ == '__main__':
    # ask for and collect data using API calls
    print('Welcome to the ML Pokémon Team Generator!')
    user_input_collection: tuple[str, list[int]] = input_generation()
    collect_data(user_input_collection[0], user_input_collection[1])

    clean_and_update_data_files()
