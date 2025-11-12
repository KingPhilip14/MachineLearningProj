import os
import psycopg2 as pg2
from dotenv import load_dotenv
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, declarative_base

# define the sqlalchemy engine for the database connection
engine = db.create_engine('sqlite:///test.db', echo=True)

# create the metadata object
metadata = db.MetaData()
Session = sessionmaker(bind=engine)
Base = declarative_base()


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
