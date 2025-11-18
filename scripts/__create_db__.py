from backend.database.db_utils import create_conn
from backend.database.create_tables import create_all_tables

if __name__ == '__main__':
    conn = create_conn()
    create_all_tables(conn)
