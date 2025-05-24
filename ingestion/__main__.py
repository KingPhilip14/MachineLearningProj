import asyncio

from ingestion.api_functions import ApiFunctions
from ingestion.data_processing import clean_and_update_pokemon_data_files
from utils import input_generation


if __name__ == '__main__':
    # Data can be collected by running this file
    filename, pokedex_ids = input_generation('What generation of Pokemon would you like to collect data for?')

    api: ApiFunctions = ApiFunctions(filename, pokedex_ids)
    asyncio.run(api.collect_data())
    clean_and_update_pokemon_data_files(f'{filename}.json')
