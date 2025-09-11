import asyncio
import json
import os
import time
from io import BytesIO

import PIL
import aiohttp
import requests
from PIL import Image

from rembg import remove
from tqdm.auto import tqdm
from config import POKEMON_DATA_DIR, SPRITES_DIR, PAUSE_TIME
from data_ingestion.base_api import BaseApi
from utils import pokemon_data_file_exists


class SpriteApi(BaseApi):
    def __init__(self, filename: str = 'national'):
        super().__init__(filename)

    async def collect_sprites(self):
        """
        Check the pokemon_data folder for the 'national.json' file. If it doesn't exist, exit.
        If the data file exists, collect all the IDs from all Pokémon and store them in a list to use later.
        """
        if not pokemon_data_file_exists(self.filename):
            print(f'{self.filename} data was not found. '
                  f'Please download the data and try again.')
            return

        # add the file extension so it can be used properly later in the process
        self.filename += '.json'

        print('Starting sprite collection...')

        pokemon_data_urls: list[str] = []

        # list of tuples containing Pokémon name, sprite URL, and if it's shiny
        sprite_info_collection: list[tuple[str, str, bool]] = []
        file_path: str = os.path.join(POKEMON_DATA_DIR, self.filename)

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

        count: int = 0

        for sprite_info_tuple in tqdm(sprite_urls[1645:1660]):
            # Pause after collecting 1000 sprites to not time out
            if count % 250 == 0 and count != 0:
                print(f'Pausing for {PAUSE_TIME} seconds to not time out while collecting sprites...')
                time.sleep(PAUSE_TIME)
                print(f'Continuing to collect sprites...')

            try:
                response = requests.get(sprite_info_tuple[1], timeout=PAUSE_TIME)

                # make an Image object with the image URL
                input_image = Image.open(BytesIO(response.content)).convert('RGBA')

                # remove the background
                output_image = remove(input_image)

                is_shiny: bool = sprite_info_tuple[2]
                img_file_name: str = f'{sprite_info_tuple[0]}-sprite_shiny.png' \
                    if is_shiny else f'{sprite_info_tuple[0]}-sprite.png'

                tqdm.write(f'Downloading sprite: {img_file_name}')

                # save the new image with the removed background
                output_image.save(f'{SPRITES_DIR}/{img_file_name}')
            except PIL.UnidentifiedImageError:
                tqdm.write(f'\nUnidentified error downloading sprite for: {sprite_info_tuple[0]}'
                           f'\nImage link: {sprite_info_tuple[1]}\n')
            except requests.exceptions.MissingSchema:
                tqdm.write(f'\nMissing schema error downloading sprite for: {sprite_info_tuple[0]}\n')

            count += 1

            # write to a file the URLs that failed and script how to recover the lost sprites separately

        print('Sprite collection complete.')
