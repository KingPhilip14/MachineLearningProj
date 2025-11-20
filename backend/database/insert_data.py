import json
import psycopg2 as pg2
from tqdm import tqdm
from config import ABILITY_FILE_DIR, MOVE_FILE_DIR, NATIONAL_FILE_DIR

prepared_var: str = 'statement'
prepared_statement: str = f'PREPARE {prepared_var} AS'


def insert_abilities(conn, cursor) -> None:
    """
    Inserts the data from the ability.json file into the database.
    """
    data: dict

    # read in the JSON file
    with open(ABILITY_FILE_DIR, 'r') as f:
        data: dict = json.load(f)
        f.close()

    print(f'Inserting {len(data)} abilities from {ABILITY_FILE_DIR}...')

    success_inserts: int = 0

    for ability in tqdm(data):
        ability_data: dict = data[ability]

        ability_id: int = ability_data['id']
        name: str = ability_data['name']
        short_desc: str = ability_data['short_desc']
        effect_desc: str = ability_data['effect_desc']
        flavor_text: str = ability_data['flavor_text']

        insert: str = """
                      INSERT INTO ability
                      VALUES (%s, %s, %s, %s, %s); \
                      """

        try:
            cursor.execute(insert, (ability_id, name, short_desc, effect_desc, flavor_text))
            conn.commit()
            success_inserts += 1
        except pg2.Error as e:
            print(e)

    print(f'Successfully inserted {success_inserts}/{len(data)} ({(success_inserts / len(data)) * 100}%) '
          f'abilities from {ABILITY_FILE_DIR} into the database.\n')


def insert_moves(conn, cursor) -> None:
    """
    Inserts the data from the move.json file into the database.
    """
    data: dict

    # read in the JSON file
    with open(MOVE_FILE_DIR, 'r') as f:
        data: dict = json.load(f)
        f.close()

    print(f'Inserting {len(data)} moves from {MOVE_FILE_DIR}...')

    success_inserts: int = 0

    for move in tqdm(data):
        move_data: dict = data[move]

        move_id: int = move_data['id']
        move_name: str = move_data['name']
        damage_class: str = move_data['damage_class']
        move_type: str = move_data['type']
        power: int = move_data['power']
        accuracy: int = move_data['accuracy']
        pp: int = move_data['pp']
        priority: int = move_data['priority']

        insert: str = """
                      INSERT INTO move
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                      """

        try:
            cursor.execute(insert, (move_id, move_name, damage_class, move_type, power, accuracy, pp, priority))
            conn.commit()
            success_inserts += 1
        except pg2.Error as e:
            print(e)

    print(f'Successfully inserted {success_inserts}/{len(data)} ({(success_inserts / len(data)) * 100}%) '
          f'moves from {MOVE_FILE_DIR} into the database.\n')


def insert_pokemon(conn, cursor) -> None:
    data: dict

    # read in the JSON file
    with open(NATIONAL_FILE_DIR, 'r') as f:
        data: dict = json.load(f)
        f.close()

    print(f'Inserting {len(data)} moves from {NATIONAL_FILE_DIR}...')

    success_inserts: int = 0

    for pokemon in tqdm(data):
        pokemon_data: dict = data[pokemon]

        pokemon_id: int = pokemon_data['id']
        pokemon_name: str = pokemon
        pokemon_role: str = pokemon_data['role']
        type_1: str = pokemon_data['type_1']
        type_2: str = pokemon_data['type_2']
        bst: int = pokemon_data['bst']
        hp: int = pokemon_data['hp']
        attack: int = pokemon_data['attack']
        defense: int = pokemon_data['defense']
        sp_attack: int = pokemon_data['special-attack']
        sp_defense: int = pokemon_data['special-defense']
        speed: int = pokemon_data['speed']
        is_legend_or_mythical: bool = pokemon_data['is_legend_or_mythical']
        weaknesses: dict = pokemon_data['weaknesses']
        resistances: dict = pokemon_data['resistances']

        insert: str = """
                      INSERT INTO pokemon
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                      """

        try:
            cursor = conn.cursor()
            cursor.execute(insert, (pokemon_id, pokemon_name, pokemon_role,
                                    type_1, type_2, bst, hp, attack, defense, sp_attack,
                                    sp_defense, speed, is_legend_or_mythical, weaknesses, resistances))
        except pg2.Error as e:
            print(e)

    print(f'Successfully inserted {success_inserts}/{len(data)} ({(success_inserts / len(data)) * 100}%) '
          f'Pokemon from {NATIONAL_FILE_DIR} into the database.\n')


def insert_movepools(conn, cursor) -> None:
    """
    Inserts the movepools from every Pokemon into the database by using the national_data.json file.
    """
    data: dict

    # read in the JSON file
    with open(NATIONAL_FILE_DIR, 'r') as f:
        data: dict = json.load(f)
        f.close()

    print(f'Inserting movepools from every Pokemon in the database...')

    # stores tuples of the Pokemon ID with a move ID
    pkmn_move_pairs: list[tuple[int, int]] = []

    # iterate over every Pokemon
    for pokemon in tqdm(data):
        pokemon_id: int = data[pokemon]['id']

        # iterate over every move in the current Pokemon's movepool
        for move_data in data[pokemon]['movepool']:
            print(move_data)
            input('>')

            key: str = move_data.keys()[0]
            subdata: dict = move_data[key]
            move_id: int = data[subdata]['id']

            pkmn_move_pairs.append((pokemon_id, move_id))

    for pair in pkmn_move_pairs:
        insert: str = """
                      INSERT INTO movepool
                      VALUES (%s, %s);
                      """

        try:
            cursor = conn.cursor()
            cursor.execute(insert, (pair[0], pair[1]))
        except pg2.Error as e:
            print(e)

    print('Successfully inserted movepools from every Pokemon in the database.\n')
