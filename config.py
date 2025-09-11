import os

# get the project root directory
ROOT_DIR: str = os.path.dirname(os.path.abspath(__file__))
DATA_DIR: str = os.path.join(ROOT_DIR, 'data')
POKEMON_DATA_DIR: str = os.path.join(DATA_DIR, 'pokemon_data')
EXTRA_DATA_DIR: str = os.path.join(DATA_DIR, 'extra_data')
SPRITES_DIR: str = os.path.join(DATA_DIR, 'sprites')

PAUSE_TIME: int = 5

# the minimum BST for a Pokémon to be considered when creating a team
BST_BARRIER: int = 350

# this is a dict that maps a string representation of a generation to the int(s) used for the API for Pokédex calls
GEN_TO_POKEDEX_MAP: dict[str, list[int]] = {
    'national': [1],
    'gen 1': [2],
    'gen 2': [7, 2],
    'gen 3': [15, 7, 2],
    'gen 4': [6, 15, 7, 2],
    'gen 5': [9, 6, 15, 7, 2],  # the newest Pokédex data for gen 5
    'gen 6': [12, 13, 14, 15, 9, 6, 15, 7, 2],  # includes all 3 Kalos Pokédexes and updated Hoenn
    'gen 7': [21],
    'gen 8': [27, 28, 29, 30],  # Galar, its DLCs, and Hisui
    'gen 9': [31, 32, 33, 30],  # Paldea, its DLCs, and Hisui
}

# if a Pokémon's name contains or is any of the following, it will be removed from the data files
NAMES_TO_FILTER: list[str] = ['pikachu-starter', 'eevee-starter', 'castform-sunny', 'castform-rainy', 'castform-snowy',
                              'keldeo-resolute', 'minior-red', 'minior-orange', 'minior-yellow', 'minior-green',
                              'minior-blue', 'minior-indigo', 'minior-violet', 'terapagos-stellar',
                              'meloetta-pirouette', 'aegislash-blade', 'wishiwashi-solo', 'magearna-original',
                              'cramorant-gulping', 'cramorant-gorging', 'eiscue-noice', 'morpeko-hangry',
                              'zarude-dada', 'maushold-family-of-three', 'palafin-zero', 'tatsugiri-droopy',
                              'tatsugiri-stretchy', 'dudunsparce-three-segment', 'gimmighoul-roaming']

WORDS_TO_FILTER: list[str] = ['busted', '-cap', 'totem']
