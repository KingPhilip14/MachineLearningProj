import os

# get the project root directory
ROOT_DIR: str = os.path.dirname(os.path.abspath(__file__))
DATA_DIR: str = os.path.join(ROOT_DIR, 'data')
POKEMON_DATA_DIR: str = os.path.join(DATA_DIR, 'pokemon_data')

PAUSE_TIME: int = 10


