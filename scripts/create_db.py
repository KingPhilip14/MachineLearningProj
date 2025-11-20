from backend.database.db_utils import create_conn
from backend.database.create_tables import create_all_tables
from backend.database.insert_data import *

if __name__ == '__main__':
    conn = create_conn()
    create_all_tables(conn)
    insert_abilities(conn)
    insert_moves(conn)
    insert_pokemon(conn)
    insert_movepools(conn)
