from ingestion.api_functions import collect_data
from ingestion.data_processing import clean_and_update_data_files
from utils import input_generation

if __name__ == '__main__':
    print('Data can be collected from here.')

    filename, pokedex_ids = input_generation()
    collect_data(filename, pokedex_ids)
    clean_and_update_data_files()
