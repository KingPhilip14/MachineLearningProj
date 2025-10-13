import aiohttp
import asyncio
import async_timeout

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
