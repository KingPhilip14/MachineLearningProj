import asyncio
import json
import os
import time
from io import BytesIO
import PIL
import aiohttp
import requests

from PIL import Image
from tqdm.auto import tqdm
from config import (POKEMON_DATA_DIR, PAUSE_TIME, ERR_SPRITES_DIR, ERR_SPRITES_FILENAME,
                    ERR_NO_SPRITES_FILENAME, POKEMON_SPRITES_DIR)
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

        file_path: str = os.path.join(POKEMON_DATA_DIR, self.filename)
        pokemon_data_urls: list[str] = []

        # list of tuples containing Pokémon name, sprite URL, and if it's shiny
        sprite_info_collection: list[tuple[str, str, bool]] = []

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
        print('Downloading sprites...')

        count: int = 0

        for sprite_info_tuple in tqdm(sprite_urls):
            # Pause after collecting 1000 sprites to not time out
            if count % 250 == 0 and count != 0:
                tqdm.write(f'Pausing for {PAUSE_TIME} seconds to not time out while collecting sprites...')
                time.sleep(PAUSE_TIME)
                tqdm.write(f'Continuing to collect sprites...')

            try:
                # make an Image object with the image URL
                output_image = Image.open(requests.get(sprite_info_tuple[1], stream=True).raw).convert('RGBA')

                is_shiny: bool = sprite_info_tuple[2]
                img_file_name: str = f'{sprite_info_tuple[0]}-sprite_shiny.png' \
                    if is_shiny else f'{sprite_info_tuple[0]}-sprite.png'

                tqdm.write(f'Downloading sprite: {img_file_name}')

                # save the new image with the removed background
                output_image.save(f'{POKEMON_SPRITES_DIR}/{img_file_name}')
            except PIL.UnidentifiedImageError as e:
                tqdm.write(f'\nUnidentified error downloading sprite for: {sprite_info_tuple[0]}'
                           f'\nImage link: {sprite_info_tuple[1]}\n')
                self.__save_uncollected_sprite(sprite_info_tuple)
            except requests.exceptions.MissingSchema as e:
                tqdm.write(f'\nMissing schema error downloading sprite for: {sprite_info_tuple[0]}\n')
                self.__save_uncollected_sprite(sprite_info_tuple)

            count += 1

        print('Sprite collection complete.')

    def __save_uncollected_sprite(self, sprite_info_tuple: tuple[str, str, bool]) -> None:
        """
        If a sprite wasn't collected because:
        - No sprite was found (i.e., a None value was returned), write the name in the error_no_sprites.txt file
        - The Image object wasn't created successfully, write the URL of the sprite in the error_sprite_urls.txt file
        """
        sprite_url: str | None = sprite_info_tuple[1]
        file_path: str

        if sprite_url is None:
            file_path = os.path.join(ERR_SPRITES_DIR, ERR_NO_SPRITES_FILENAME)

            with open(file_path, 'a') as f:
                f.write(f'{sprite_info_tuple[0]}\n')

            tqdm.write(f'No sprite for {sprite_info_tuple[0]} and saved its name to {file_path}. '
                       f'Please recover a sprite for this in the clean up collection method')
            return

        file_path = os.path.join(ERR_SPRITES_DIR, ERR_SPRITES_FILENAME)

        with open(file_path, 'a') as f:
            f.write(sprite_url + '\n')
            tqdm.write(f'Wrote error sprite URL {sprite_url} to {file_path}. Please run the sprite clean up collection '
                  f'method')

    def __recover_lost_sprites(self):
        ...

    def __recover_no_sprite_err(self):
        no_sprite_file_path: str = os.path.join(ERR_SPRITES_DIR, ERR_NO_SPRITES_FILENAME)

        with open(no_sprite_file_path, 'r') as f:
            lines: list[str] = f.readlines()

        for pokemon_name in lines:
            # reverse the list of sprites in the folder since errors occur later in the collection
            for filename in os.listdir(POKEMON_SPRITES_DIR)[::-1]:
                # if the file name contains the Pokémon name and is not a shiny, save it as a new file for the Pokémon
                if filename.__contains__(pokemon_name) and not filename.__contains__('shiny'):

                    # make an Image object from a directory file with file name from pokemon_name
