import os
from fileinput import filename

import psycopg2 as pg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql


def create_conn():
    """
    Creates the database connection and returns it. The database parameters are read from the .env file.
    """
    print('Creating the database...')
    load_dotenv()

    try:
        db_params: dict = {
            'host': os.getenv('DB_HOST'),
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'port': os.getenv('DB_PORT'),
        }

        print('Database parameters loaded successfully.')

        conn = pg2.connect(**db_params)
        conn.autocommit = True
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        print('Database connection established.\n')

        __create_database(conn, db_params['dbname'])

        print('Database created successfully.\n')

        return conn
    except pg2.Error as err:
        print(f"An error occurred while connecting to PostgreSQL: {err}\nExiting the program...")
        exit(1)


def __create_database(conn, db_name: str):
    cursor = conn.cursor()
    create_query =  sql.SQL('CREATE DATABASE {}').format(sql.Identifier(db_name))

    try:
        cursor.execute(create_query, (db_name, ))
    except pg2.errors.DuplicateDatabase:
        print(f'Database "{db_name}" already exists. A new one will not be created.')
    except pg2.Error as err:
        print(f'An error occurred when creating the database: {err}. Aborting the program...')
        exit(1)


def print_error_msg(class_name: str, method_name: str, error: pg2.Error) -> None:
    """
    Prints multiple statements to provide further details on may have gone wrong for a method. By using the given
    class name and method name, additional details will be given to know which method caused the issue.
    """
    print(f'An error occurred in {class_name}.{method_name}:')
    print(f'PG Error message: {error}')
    print(f'PG Error details: {error.pgerror}')
    print(f'PG Error code: {error.pgcode}')
    print(f'Diagnostics: {getattr(error, 'diag', None)}\n')
