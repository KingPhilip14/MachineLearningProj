import json
import os
import psycopg2

from config import ABILITY_FILE_DIR


def insert_abilities(conn) -> None:
    data: dict

    # read in the JSON file
    with open(ABILITY_FILE_DIR, 'r') as f:
        data = json.load(f)
        f.close()

    ability_id: int
    name: str
    short_desc: str
    effect_desc: str
    flavor_text: str

    print(f'Inserting {len(data)} abilities from {ABILITY_FILE_DIR}...')

    for ability in data:
        ability_id = ability['id']
        name = ability['name']
        short_desc = ability['short_desc']
        effect_desc = ability['effect_desc']
        flavor_text = ability['flavor_text']

        insert: str = """
        INSERT INTO ability VALUES (?, ?, ?, ?, ?);
        """

        try:
            cursor = conn.cursor()
            cursor.execute(insert, (ability_id, name, short_desc, effect_desc, flavor_text))
            conn.commit()
        except pg2.Error as e:
            filename: str = os.path.basename(__file__)
            print_error_msg(filename, create_all_tables.__name__, e)
        finally:
            conn.close()

