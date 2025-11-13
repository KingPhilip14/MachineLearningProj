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
        cursor.execute(create_pokemon_ability_table())
        cursor.execute(create_moveset_table())
        conn.commit()

        print('All tables were created successfully.')
    except pg2.Error as e:
        filename: str = os.path.basename(__file__)
        print_error_msg(filename, create_all_tables.__name__, e)
    finally:
        conn.close()


def create_account_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS account (
        account_id INTEGER PRIMARY KEY SERIAL,
        username VARCHAR(30) NOT NULL UNIQUE,
        password VARCHAR(30) NOT NULL,
    );
    """

def create_team_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS team(
        team_id INTEGER PRIMARY KEY SERIAL,
        FOREIGN KEY (account_id) REFERENCES account(account_id) ON DELETE CASCADE,
        team_name VARCHAR(30) NOT NULL,
        generation varchar(20) NOT NULL,
        time_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        last_time_used TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        overlapping_weaknesses JSONB NOT NULL,
    );
    """

def create_pokemon_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS pokemon(
        pokemon_id INTEGER PRIMARY KEY,
        FOREIGN KEY (movepool_id) REFERENCES movepool(movepool_id),
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
        resistances JSONB,
    );
    """

def create_movepool_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS movepool(
        PRIMARY KEY (movepool_id, pokemon_id),
        FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokemon_id),
    );
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
        priority INTEGER NOT NULL,
    );
    """

def create_movepool_collection_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS movepool_collection(
        PRIMARY KEY(movepool_id, move_id),
        FOREIGN KEY (movepool_id) REFERENCES movepool(movepool_id),
        FOREIGN KEY (move_id) REFERENCES move(move_id),
    ); 
    """

def create_ability_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS ability(
        ability_id INTEGER PRIMARY KEY,
        ability_name VARCHAR(30) NOT NULL UNIQUE,
        effect_desc VARCHAR(150) NOT NULL,
    )
    """

def create_pokemon_in_team_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS pokemon_in_team(
        pit_id INTEGER PRIMARY KEY SERIAL,
        FOREIGN KEY (team_id) REFERENCES team(team_id) NOT NULL,
        FOREIGN KEY (pokemon_id) REFERENCES user(pokemon_id) NOT NULL,
        FOREIGN KEY (chosen_ability_id) REFERENCES ability(ability_id) NOT NULL,
        FOREIGN KEY (moveset_id) REFERENCES moveset(moveset_id) NOT NULL,
        nickname VARCHAR(30) NOT NULL,
    );
    """

def create_pokemon_ability_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS pokemon_abilities(
        PRIMARY KEY (pokemon_id, ability_id),
        FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokemon_id),
        FOREIGN KEY (ability_id) REFERENCES ability(ability_id)
    );
    """

def create_moveset_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS moveset_move(
        moveset_id INTEGER PRIMARY KEY SERIAL,
        FOREIGN KEY (pit_id) REFERENCES pokemon_in_team(pit_id),
        FOREIGN KEY (move_id) REFERENCES move(move_id),
    );
    """
