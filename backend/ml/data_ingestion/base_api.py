import aiohttp
import asyncio
import async_timeout
from typing import Callable, Awaitable
from tqdm import tqdm
from utils import pokemon_data_file_exists, save_json_file, roman_to_int, get_generation_num


class BaseApi:
    def __init__(self, filename: str = 'national'):
        self.base_url: str = 'https://pokeapi.co/api/v2/'
        self.filename: str = filename
        self.sem: asyncio.Semaphore = asyncio.Semaphore(10)

    async def fetch_json(self, session: aiohttp.ClientSession, url: str) -> dict:
        async with self.sem:
            try:
                async with async_timeout.timeout(10):
                    async with session.get(url) as response:
                        return await response.json(content_type='application/json')
            except Exception as e:
                print(f'Failed to fetch {url}: {e}')
                return dict()

    async def collect_data_urls(self, url_name: str, session: aiohttp.ClientSession) -> list[str]:
        data_url: str = f'{self.base_url}/{url_name}?limit=1000000&offset=0'
        url_collection: dict = await self.fetch_json(session, data_url)
        results: list[dict] = url_collection['results']
        urls: list[str] = list()

        for result in tqdm(results):
            urls.append(result['url'])

        return urls
