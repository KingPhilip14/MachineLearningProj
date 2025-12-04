from sqlalchemy import text

from backend.api.db import engine

if __name__ == '__main__':
    with engine.connect() as conn:
        print(conn.execute(text("SELECT 1")).scalar())
