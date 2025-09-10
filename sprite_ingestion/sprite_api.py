import asyncio
import json
import os

import aiohttp
import requests
from PIL import Image
from rembg import remove
from tqdm import tqdm

from config import POKEMON_DATA_DIR, SPRITES_DIR
from data_ingestion.base_api import BaseApi
from utils import pokemon_data_file_exists


class SpriteApi(BaseApi):
    def __init__(self):
        super().__init__()
        self.national_data: dict | None = None

    async def collect_sprites(self):
        """
        Check the pokemon_data folder for the 'national.json' file. If it doesn't exist, exit.
        If the data file exists, collect all the IDs from all Pokémon and store them in a list to use later.
        """
        if not pokemon_data_file_exists('national_data'):
            print('National data was not found. Please download the data to continue.')
            return

        print('Starting sprite collection...')

        pokemon_data_urls: list[str] = []

        # list of tuples containing Pokémon name, sprite URL, and if it's shiny
        sprite_info_collection: list[tuple[str, str, bool]] = []
        file_path: str = os.path.join(POKEMON_DATA_DIR, 'national_data.json')

        # open the data file
        with open(file_path, 'r') as f:
            file_data: dict = json.load(f)
            f.close()

        for pokemon_name in file_data.keys():
            pokemon_data_urls.append(f'{self.base_url}/pokemon/{pokemon_name}')

        async with aiohttp.ClientSession() as session:
            # collect the data from the endpoint for each Pokémon
            api_data: list[dict] = await asyncio.gather(*[self.fetch_json(session, url) for url in pokemon_data_urls])

        # store all the sprite URLs in the list; this includes the regular and shiny front sprites
        for pokemon_data in api_data:
            sprite_info_collection.append((pokemon_data['name'],
                                           pokemon_data['sprites']['front_default'],
                                           False))
            sprite_info_collection.append((pokemon_data['name'],
                                           pokemon_data['sprites']['front_shiny'],
                                           True))

        self.__download_sprites(sprite_info_collection)

    def __download_sprites(self, sprite_urls: list[tuple[str, str, bool]]):
        print('Downloading sprites and removing their backgrounds...')

        for sprite_info_tuple in tqdm(sprite_urls):
            # make an Image object with the image URL
            input_image: Image = Image.open(requests.get(sprite_info_tuple[1], stream=True).raw).convert('RGB')

            # remove the background
            output_image = remove(input_image)

            is_shiny: bool = sprite_info_tuple[2]
            img_file_name: str = f'{sprite_info_tuple[0]}_sprite_shiny.png' \
                if is_shiny else f'{sprite_info_tuple[0]}_sprite.png'

            # save the new image with the removed background
            output_image.save(f'{SPRITES_DIR}/{img_file_name}')

        print('Sprite collection complete.')
