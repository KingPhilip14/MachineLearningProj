import os
import psycopg2 as pg2
from dotenv import load_dotenv


def create_conn():
    """
    Creates the database connection and returns it. The database parameters are read from the .env file.
    """
    print('Connecting to the database...')
    load_dotenv()

    db_params = {
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
    }

    print(f'{db_params}')
    print('Database parameters loaded successfully.')

    input('>')

    conn = pg2.connect(**db_params)

    print('Database connection established.')

    return conn


def print_error_msg(class_name: str, method_name: str, error: pg2.Error) -> None:
    """
    Prints multiple statements to provide further details on may have gone wrong for a method. By using the given
    class name and method name, additional details will be given to know which method caused the issue.
    """
    print(f'An error occurred in {class_name}.{method_name}:')
    print('PG Error message:', error)
    print('PG Error details:', error.pgerror)
    print('PG Error code:', error.pgcode)
    print('Diagnostics:', getattr(error, 'diag', None))
