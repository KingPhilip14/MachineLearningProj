import asyncio
import os

import aiohttp
from tqdm import tqdm

from backend.ml.data_ingestion.base_api import BaseApi
from config import ABILITY_DATA_DIR
from utils import save_json_file


class AbilityApi(BaseApi):
    def __init__(self):
        super().__init__()
        self.filename: str = 'ability'

    async def download_ability_data(self) -> None:
        """
        Using the ability endpoint, the JSON that returns a list of basic ability dictionaries entries is collected.
        The URL from each entry is extracted to be used later
        :return:
        """
        async with aiohttp.ClientSession() as session:
            ability_url: str = f'{self.base_url}/ability?limit=1000000&offset=0'
            url_collection: dict = await self.fetch_json(session, ability_url)
            results: list[dict] = url_collection['results']
            urls: list[str] = list()

            for result in tqdm(results):
                urls.append(result['url'])

            collected_data: dict = await self.__get_ability_data(session, urls)
            save_json_file(collected_data, self.filename, ABILITY_DATA_DIR)

    async def __get_ability_data(self, session: aiohttp.ClientSession, urls: list[str]) -> dict[dict]:
        ability_data: list[dict] = await asyncio.gather(*[self.fetch_json(session, url) for url in urls])
        collected_data: dict[dict] = dict()
        to_add: dict

        for ability in ability_data:

            if not ability['is_main_series']:
                continue

            try:
                to_add = {
                    'id': ability['id'],
                    'name': ability['name'],
                    'short_desc': [entry['short_effect'] for entry in ability['effect_entries']
                                   if entry['language']['name'] == 'en'][0],
                    'effect_desc': [entry['effect'] for entry in ability['effect_entries']
                                    if entry['language']['name'] == 'en'][0],
                    'flavor_text': [entry['flavor_text'] for entry in ability['flavor_text_entries']
                                    if entry['language']['name'] == 'en'][0],
                }

            except IndexError:
                print(f'Cannot add ability effect description or short description for ability "{ability["name"]}" because getting its English effect description failed\n'
                      f'Adding empty strings for descriptions instead.instead.')

                to_add = {
                    'id': ability['id'],
                    'name': ability['name'],
                    'short_desc': '',
                    'effect_desc': '',
                    'flavor_text': [entry['flavor_text'] for entry in ability['flavor_text_entries']
                                    if entry['language']['name'] == 'en'][0],
                }

            collected_data.update({ability['name']: to_add})

        return collected_data
