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
        attempts: int = 0
        return await self.__fetch(session, url, attempts)

    async def collect_data_urls(self, url_name: str, session: aiohttp.ClientSession) -> list[str]:
        data_url: str = f'{self.base_url}/{url_name}?limit=1000000&offset=0'
        url_collection: dict = await self.fetch_json(session, data_url)
        results: list[dict] = url_collection['results']
        urls: list[str] = list()

        for result in tqdm(results):
            urls.append(result['url'])

        return urls

    async def __fetch(self, session: aiohttp.ClientSession, url: str, attempts: int) -> dict:
        """
        If the initial URL failed, try it again without the trailing slash. If that also doesn't work, return an empty
        dict with no data.

        The reason for this is that there's inconcsistency within the API for when
        """
        while attempts < 2:
            async with self.sem:
                try:
                    async with async_timeout.timeout(10):
                        async with session.get(url) as response:
                            attempts += 1
                            return await response.json(content_type='application/json')
                except Exception as e:
                    # if on another attempt and the last url character is a slash, try again
                    if attempts < 2 and (url[-1] == '/' or url[-1] == '\\'):
                        print(f'Attempting to fetch data from {url} again. Excluding trailing slash...')
                        return await self.__fetch(session, url[:-1], attempts)
                    elif attempts < 2 and (url[-1] != '/' and url[-1] != '\\'):
                        print(f'Attempting to fetch data from {url} again. Adding trailing slash...')
                        return await self.__fetch(session, url + '/', attempts)

                    print(f'Failed to fetch {url}: {e}')
                    return dict()

        print(f'Failed to fetch data from {url} and the URL without trailing slash. Returning empty dict.')
        return dict()
