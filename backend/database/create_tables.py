import os
import psycopg2 as pg2
from backend.database.db_utils import print_error_msg


def create_all_tables(conn, cursor):
    """
    Creates all the tables for the database.
    """
    # create the tables
    create_account_table(conn, cursor)
    create_team_table(conn, cursor)
    create_pokemon_table(conn, cursor)
    create_ability_table(conn, cursor)
    create_pokemon_ability_table(conn, cursor)
    create_move_table(conn, cursor)
    create_movepool_table(conn, cursor)
    create_moveset_table(conn, cursor)
    create_pokemon_in_team_table(conn, cursor)

    print('All tables were created successfully.\n')


def create_account_table(conn, cursor) -> None:
    try:
        insert: str = """
        CREATE TABLE IF NOT EXISTS account (
            account_id SERIAL PRIMARY KEY,
            username VARCHAR(30) NOT NULL UNIQUE,
            password VARCHAR(30) NOT NULL);
        """
        
        cursor.execute(insert)
        conn.commit()
    except pg2.Error as e:
        filename: str = os.path.basename(__file__)
        print_error_msg(filename, create_all_tables.__name__, e)
    

def create_team_table(conn, cursor) -> None:
    try:
        insert: str = """
        CREATE TABLE IF NOT EXISTS team(
            team_id SERIAL PRIMARY KEY,
            account_id INTEGER NOT NULL REFERENCES account(account_id) ON DELETE CASCADE,
            team_name VARCHAR(30) NOT NULL,
            generation varchar(20) NOT NULL,
            time_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            last_time_used TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            overlapping_weaknesses JSONB NOT NULL);
        """

        cursor.execute(insert)
        conn.commit()
    except pg2.Error as e:
        filename: str = os.path.basename(__file__)
        print_error_msg(filename, create_all_tables.__name__, e)


def create_pokemon_table(conn, cursor) -> None:
    try:
        insert: str = """
        CREATE TABLE IF NOT EXISTS pokemon(
            pokemon_id INTEGER PRIMARY KEY,
            pokemon_name VARCHAR(50) NOT NULL,
            pokemon_role VARCHAR(50) NOT NULL,
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

        cursor.execute(insert)
        conn.commit()
    except pg2.Error as e:
        filename: str = os.path.basename(__file__)
        print_error_msg(filename, create_all_tables.__name__, e)


def create_move_table(conn, cursor) -> None:
    try:
        insert: str = """
        CREATE TABLE IF NOT EXISTS move(
            move_id INTEGER PRIMARY KEY,
            move_name VARCHAR(50) NOT NULL,
            damage_class VARCHAR(30) NOT NULL,
            move_type VARCHAR(10) NOT NULL,
            power INTEGER,
            accuracy INTEGER,
            pp INTEGER,
            priority INTEGER NOT NULL);
        """

        cursor.execute(insert)
        conn.commit()
    except pg2.Error as e:
        filename: str = os.path.basename(__file__)
        print_error_msg(filename, create_all_tables.__name__, e)


def create_movepool_table(conn, cursor) -> None:
    try:
        insert: str = """
        CREATE TABLE IF NOT EXISTS movepool(
            pokemon_id INTEGER NOT NULL REFERENCES pokemon(pokemon_id),
            move_id INTEGER NOT NULL REFERENCES move(move_id),
            PRIMARY KEY (pokemon_id, move_id));
        """

        cursor.execute(insert)
        conn.commit()
    except pg2.Error as e:
        filename: str = os.path.basename(__file__)
        print_error_msg(filename, create_all_tables.__name__, e)


def create_ability_table(conn, cursor) -> None:
    try:
        insert: str = """
        CREATE TABLE IF NOT EXISTS ability(
            ability_id INTEGER PRIMARY KEY,
            ability_name VARCHAR(50) NOT NULL UNIQUE,
            effect_desc VARCHAR(3000) NOT NULL,
            short_desc VARCHAR(3000) NOT NULL,
            flavor_text VARCHAR(3000) NOT NULL);
        """

        cursor.execute(insert)
        conn.commit()
    except pg2.Error as e:
        filename: str = os.path.basename(__file__)
        print_error_msg(filename, create_all_tables.__name__, e)


def create_moveset_table(conn, cursor) -> None:
    try:
        insert: str = """
        CREATE TABLE IF NOT EXISTS moveset(
            moveset_id SERIAL PRIMARY KEY,
            move_id INTEGER NOT NULL REFERENCES move(move_id));
        """

        cursor.execute(insert)
        conn.commit()
    except pg2.Error as e:
        filename: str = os.path.basename(__file__)
        print_error_msg(filename, create_all_tables.__name__, e)


def create_pokemon_in_team_table(conn, cursor) -> None:
    try:
        insert: str = """
        CREATE TABLE IF NOT EXISTS pokemon_in_team(
            pit_id SERIAL PRIMARY KEY,
            team_id INTEGER NOT NULL REFERENCES team(team_id) ON DELETE CASCADE,
            pokemon_id INTEGER NOT NULL REFERENCES pokemon(pokemon_id),
            chosen_ability_id INTEGER NOT NULL REFERENCES ability(ability_id),
            moveset_id INTEGER NOT NULL REFERENCES moveset(moveset_id),
            nickname VARCHAR(30) NOT NULL,
            is_shiny BOOLEAN NOT NULL);
        """

        cursor.execute(insert)
        conn.commit()
    except pg2.Error as e:
        filename: str = os.path.basename(__file__)
        print_error_msg(filename, create_all_tables.__name__, e)


def create_pokemon_ability_table(conn, cursor) -> None:
    try:
        insert: str = """
        CREATE TABLE IF NOT EXISTS pokemon_abilities(
            pokemon_id INTEGER NOT NULL REFERENCES pokemon(pokemon_id),
            ability_id INTEGER NOT NULL REFERENCES ability(ability_id),
            is_hidden BOOLEAN NOT NULL DEFAULT FALSE,
            PRIMARY KEY (pokemon_id, ability_id));
        """

        cursor.execute(insert)
        conn.commit()
    except pg2.Error as e:
        filename: str = os.path.basename(__file__)
        print_error_msg(filename, create_all_tables.__name__, e)
