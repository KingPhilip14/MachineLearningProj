import asyncio
import aiohttp
from backend.ml.data_ingestion.base_api import BaseApi
from config import MOVE_DATA_DIR
from utils import save_json_file


class MoveApi(BaseApi):
    def __init__(self):
        super().__init__()
        self.filename: str = 'moves'

    async def download_move_data(self) -> None:
        """
        The move endpoint from PokeAPI is called to collect the data for all moves. The URL for each
        move entry is used.
        :return:
        """
        async with aiohttp.ClientSession() as session:
            urls: list[str] = await self.collect_data_urls('move', session)
            collected_data: dict = await self.__get_move_data(session, urls)
            save_json_file(collected_data, self.filename, MOVE_DATA_DIR)

    async def __get_move_data(self, session: aiohttp.ClientSession, urls: list[str]) -> dict:
        move_data: list[dict] = await asyncio.gather(*[self.fetch_json(session, url) for url in urls])
        collected_data: dict[dict] = dict()

        for move in move_data:
            to_add: dict[str, dict] = {
                'id': move['id'],
                'name': move['name'],
                'damage_class': move['damage_class']['name'],
                'type': move['type']['name'],
                'power': move['power'],
                'accuracy': move['accuracy'],
                'pp': move['pp'],
                'priority': move['priority']
            }

            collected_data.update({move['name']: to_add})

        return collected_data
