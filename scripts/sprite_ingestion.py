import asyncio

from backend.ml.sprite_ingestion.sprite_api import SpriteApi
from utils import input_generation, create_dirs

if __name__ == '__main__':
    # Sprites can be collected by running this file
    create_dirs()
    filename: str = input_generation('What generation of Pokemon would you like to collect sprites for?')[0]

    sprite_api = SpriteApi(filename)
    asyncio.run(sprite_api.collect_sprites())
