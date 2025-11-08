import json
import os

from config import ABILITY_FILE_DIR


def insert_abilities() -> None:
    data: dict

    with open(ABILITY_FILE_DIR, 'r') as f:
        data = json.load(f)
        f.close()

    for ability in data:

