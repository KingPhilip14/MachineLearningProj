import asyncio

from backend.ml.data_ingestion.ability_api import AbilityApi
from utils import create_dirs

if __name__ == '__main__':
    # ability data can be collected by running this file
    create_dirs()
    ability_api: AbilityApi = AbilityApi()

    asyncio.run(ability_api.download_ability_data())
