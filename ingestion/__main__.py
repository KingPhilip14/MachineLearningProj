import asyncio

from ingestion.api_functions import ApiFunctions
from ingestion.data_processing import update_data_file, clean_data_files
from utils import input_generation


if __name__ == '__main__':
    # Data can be collected by running this file
    filename, pokedex_ids = input_generation('What generation of Pokemon would you like to collect data for?')

    api: ApiFunctions = ApiFunctions(filename, pokedex_ids)
    asyncio.run(api.collect_data())
    update_data_file(f'{filename}.json')
    clean_data_files()

