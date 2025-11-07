import asyncio

from backend.ml.data_ingestion.data_api import DataApi
from backend.ml.data_ingestion.data_processing import update_data_file, clean_data_files
from utils import input_generation, create_dirs

if __name__ == '__main__':
    # Data can be collected by running this file
    create_dirs()
    filename, pokedex_ids = input_generation('What generation of Pokemon would you like to collect data for?')

    data_api: DataApi = DataApi(filename, pokedex_ids)
    asyncio.run(data_api.collect_data())
    update_data_file(f'{filename}.json')
    clean_data_files()

