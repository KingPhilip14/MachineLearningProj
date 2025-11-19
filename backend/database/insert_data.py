import json
import sqlite3
from config import ABILITY_FILE_DIR


def insert_abilities(conn) -> None:
    data: dict

    # read in the JSON file
    with open(ABILITY_FILE_DIR, 'r') as f:
        data: dict = json.load(f)
        f.close()

    print(f'Inserting {len(data)} abilities from {ABILITY_FILE_DIR}...')

    success_inserts: int = 0

    for ability in data:
        ability_data: dict = data[ability]

        ability_id: int = ability_data['id']
        name: str = ability_data['name']
        short_desc: str = ability_data['short_desc']
        effect_desc: str = ability_data['effect_desc']
        flavor_text: str = ability_data['flavor_text']

        insert: str = """
        INSERT INTO ability VALUES (?, ?, ?, ?, ?);
        """

        try:
            cursor = conn.cursor()
            cursor.execute(insert, (ability_id, name, short_desc, effect_desc, flavor_text))
            conn.commit()
            success_inserts += 1
        except sqlite3.Error as e:
            print(e)

    print(f'Successfully inserted {success_inserts}/{len(data)} ({(success_inserts / len(data)) * 100}%) '
          f'abilities from {ABILITY_FILE_DIR} into the database.')
