import os
from fileinput import filename

import psycopg2 as pg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_conn():
    """
    Creates the database connection and returns it. The database parameters are read from the .env file.
    """
    print('Creating the database...')
    load_dotenv()

    db_params: dict = {
        'host': os.getenv('DB_HOST'),
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT'),
    }

    print('Database parameters loaded successfully.')

    conn = pg2.connect(**db_params)

    print('Database connection established.\n')

    return conn


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
