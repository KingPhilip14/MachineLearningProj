from backend.database.db_utils import create_conn
from backend.database.delete_tables import delete_tables

if __name__ == '__main__':
    conn = create_conn()
    cursor = conn.cursor()

    delete_tables(conn, cursor)
