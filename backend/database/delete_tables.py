import os
import psycopg2 as pg2
from psycopg2 import sql
from backend.database.db_utils import print_error_msg


def delete_tables(conn, cursor):
    __delete_table(conn, cursor, 'account')
    __delete_table(conn, cursor, 'team')
    __delete_table(conn, cursor, 'pokemon')
    __delete_table(conn, cursor, 'movepool')
    __delete_table(conn, cursor, 'move')
    __delete_table(conn, cursor, 'moveset')
    __delete_table(conn, cursor, 'pokemon_in_team')
    __delete_table(conn, cursor, 'ability')
    __delete_table(conn, cursor, 'pokemon_abilities')


def __delete_table(conn, cursor, table_name: str) -> None:
    try:
        delete = sql.SQL('DROP TABLE IF EXISTS {} CASCADE').format(sql.Identifier(table_name))

        cursor.execute(delete)
        conn.commit()
        print(f'Successfully deleted {table_name} table.')
    except pg2.Error as e:
        filename: str = os.path.basename(__file__)
        print_error_msg(filename, delete_tables.__name__, e)
