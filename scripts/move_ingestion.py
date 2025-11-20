import asyncio

import aiohttp

from backend.ml.data_ingestion.move_api import MoveApi
from utils import create_dirs

if __name__ == '__main__':
    # ability data can be collected by running this file
    create_dirs()
    ability_api: MoveApi = MoveApi()

    asyncio.run(ability_api.download_move_data())
