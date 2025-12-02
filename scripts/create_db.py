from backend.database.db_utils import create_conn, create_database
from backend.database.create_tables import create_all_tables
from backend.database.insert_data import *

if __name__ == '__main__':
    conn = create_conn()
    cursor = conn.cursor()

    create_database(conn)
    create_all_tables(conn, cursor)

    insert_abilities(conn, cursor)
    insert_moves(conn, cursor)
    insert_pokemon(conn, cursor)
    insert_movepools(conn, cursor)
    insert_pokemon_abilities(conn, cursor)
