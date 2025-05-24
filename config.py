import os

# get the project root directory
ROOT_DIR: str = os.path.dirname(os.path.abspath(__file__))
DATA_DIR: str = os.path.join(ROOT_DIR, 'data')
POKEMON_DATA_DIR: str = os.path.join(DATA_DIR, 'pokemon_data')
EXTRA_DATA_DIR: str = os.path.join(DATA_DIR, 'extra_data')

PAUSE_TIME: int = 3

# this is a dict that maps a string representation of a generation to the int(s) used for the API for Pokédex calls
GEN_TO_POKEDEX_MAP: dict[str, list[int]] = {
        'everything': [1],
        'gen 1': [2],
        'gen 2': [7, 2],
        'gen 3': [15, 7, 2],
        'gen 4': [6, 15, 7, 2],
        'gen 5': [9, 6, 15, 7, 2],  # the newest Pokédex data for gen 5
        'gen 6': [12, 13, 14, 15, 9, 6, 15, 7, 2],  # includes all 3 Kalos Pokédexes and updated Hoenn
        'gen 7': [21],
        'gen 8': [27, 28, 29],
        'gen 9': [31, 32, 33],
    }
