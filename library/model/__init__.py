from contextlib import contextmanager
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import cursor as Cur


class AbstractDatabase:
    def __init__(self, pool):
        self.pool = pool

    @contextmanager
    def get_db_connection(self):
        try:
            connection = self.pool.getconn()
            yield connection
        finally:
            self.pool.putconn(connection)

    @contextmanager
    def get_db_cursor(self, commit=False) -> Cur:
        with self.get_db_connection() as conn:
            cursor: Cur = conn.cursor(cursor_factory=RealDictCursor)
            try:
                yield cursor
                if commit:
                    conn.commit()
            finally:
                cursor.close()
