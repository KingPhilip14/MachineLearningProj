import os
import psycopg2 as pg2
from dotenv import load_dotenv


def create_conn():
    """
    Creates the database connection and returns it. The database parameters are read from the .env file.
    """
    load_dotenv()

    db_params = {
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
    }

    conn = pg2.connect(**db_params)

    return conn
