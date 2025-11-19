import os
import psycopg2 as pg2
from backend.database.db_utils import print_error_msg

def create_all_tables(conn):
    """
    Creates all the tables for the database.
    """
    try:
        cursor = conn.cursor()

        # create the tables
        cursor.execute(create_account_table())
        cursor.execute(create_team_table())
        cursor.execute(create_pokemon_table())
        cursor.execute(create_movepool_table())
        cursor.execute(create_move_table())
        cursor.execute(create_movepool_collection_table())
        cursor.execute(create_pokemon_in_team_table())
        cursor.execute(create_ability_table())
        cursor.execute(create_moveset_table())
        cursor.execute(create_pokemon_ability_table())
        conn.commit()

        print('All tables were created successfully.')
    except pg2.Error as e:
        filename: str = os.path.basename(__file__)
        print_error_msg(filename, create_all_tables.__name__, e)


def create_account_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS account (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(30) NOT NULL UNIQUE,
        password VARCHAR(30) NOT NULL);
    """

def create_team_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS team(
        team_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER NOT NULL REFERENCES account(account_id) ON DELETE CASCADE,
        team_name VARCHAR(30) NOT NULL,
        generation varchar(20) NOT NULL,
        time_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        last_time_used TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        overlapping_weaknesses JSONB NOT NULL);
    """

def create_pokemon_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS pokemon(
        pokemon_id INTEGER PRIMARY KEY,
        movepool_id INTEGER NOT NULL REFERENCES movepool(movepool_id),
        pokemon_name VARCHAR(30) NOT NULL,
        pokemon_role VARCHAR(30) NOT NULL,
        type_1 VARCHAR(10) NOT NULL,
        type_2 VARCHAR(10) NOT NULL,
        bst INTEGER NOT NULL,
        hp INTEGER NOT NULL,
        attack INTEGER NOT NULL,
        defense INTEGER NOT NULL,
        special_attack INTEGER NOT NULL,
        special_defense INTEGER NOT NULL,
        speed INTEGER NOT NULL,
        is_legend_or_mythical BOOLEAN NOT NULL,
        weaknesses JSONB,
        resistances JSONB);
    """

def create_movepool_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS movepool(
        movepool_id INTEGER NOT NULL,
        pokemon_id INTEGER NOT NULL REFERENCES pokemon(pokemon_id),
        PRIMARY KEY (movepool_id, pokemon_id));
    """

def create_move_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS move(
        move_id INTEGER PRIMARY KEY,
        move_name VARCHAR(30) NOT NULL,
        damage_class VARCHAR(30) NOT NULL,
        power INTEGER,
        accuracy INTEGER NOT NULL,
        pp INTEGER NOT NULL,
        priority INTEGER NOT NULL);
    """

def create_movepool_collection_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS movepool_collection(
        movepool_id INTEGER NOT NULL REFERENCES movepool(movepool_id),
        move_id INTEGER NOT NULL REFERENCES move(move_id),
        PRIMARY KEY(movepool_id, move_id)); 
    """

def create_ability_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS ability(
        ability_id INTEGER PRIMARY KEY,
        ability_name VARCHAR(30) NOT NULL UNIQUE,
        effect_desc VARCHAR(500) NOT NULL,
        short_desc VARCHAR(500) NOT NULL,
        flavor_text VARCHAR(500) NOT NULL);
    """

def create_moveset_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS moveset(
        moveset_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pit_id INTEGER NOT NULL REFERENCES pokemon_in_team(pit_id),
        move_id INTEGER NOT NULL REFERENCES move(move_id));
    """

def create_pokemon_in_team_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS pokemon_in_team(
        pit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_id INTEGER NOT NULL REFERENCES team(team_id) ON DELETE CASCADE,
        pokemon_id INTEGER NOT NULL REFERENCES pokemon(pokemon_id),
        chosen_ability_id INTEGER NOT NULL REFERENCES ability(ability_id),
        moveset_id INTEGER NOT NULL REFERENCES moveset(move_id),
        nickname VARCHAR(30) NOT NULL);
    """


def create_pokemon_ability_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS pokemon_abilities(
        pokemon_id INTEGER NOT NULL REFERENCES pokemon(pokemon_id),
        ability_id INTEGER NOT NULL REFERENCES ability(ability_id),
        PRIMARY KEY (pokemon_id, ability_id));
    """
