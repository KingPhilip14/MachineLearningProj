import os
import sqlite3
from dotenv import load_dotenv


def create_conn():
    """
    Creates the database connection and returns it. The database parameters are read from the .env file.
    """
    print('Creating the database...')
    # load_dotenv()

    # db_params = {
    #     'database': os.getenv('DB_NAME'),
    #     'user': os.getenv('DB_USER'),
    #     'password': os.getenv('DB_PASSWORD'),
    #     'host': os.getenv('DB_HOST'),
    #     'port': os.getenv('DB_PORT'),
    # }
    #
    # print('Database parameters loaded successfully.')

    # creates the database if it doesn't exist already
    conn: sqlite3.Connection = sqlite3.connect('paige_server.db')

    print('Database created successfully.')

    return conn


def print_error_msg(class_name: str, method_name: str, error: sqlite3.Error) -> None:
    """
    Prints multiple statements to provide further details on may have gone wrong for a method. By using the given
    class name and method name, additional details will be given to know which method caused the issue.
    """
    print(f'An error occurred in {class_name}.{method_name}:')
    print('Error code:', error.sqlite_errorcode)
    print('Error name:', error.sqlite_errorname)
