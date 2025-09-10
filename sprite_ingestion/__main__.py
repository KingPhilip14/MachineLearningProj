import asyncio

from sprite_ingestion.sprite_api import SpriteApi

if __name__ == '__main__':
    # Sprites can be collected by running this file
    sprite_api = SpriteApi()
    asyncio.run(sprite_api.collect_sprites())
