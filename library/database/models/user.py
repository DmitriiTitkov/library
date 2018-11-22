from library.database import AbstractDatabase
from psycopg2.extensions import cursor as Cur


class User(AbstractDatabase):
    def __init__(self, pool):
        super().__init__(pool)

    def get_all(self):
        with self.get_db_cursor() as cur:  # type: Cur
            cur.execute('''SELECT 
                             user_id, 
                             first_name, 
                             last_name 
                           FROM
                             users
                           ''')
            return cur.fetchall()

    def get(self, user_id: int):
        with self.get_db_cursor() as cur:  # type: Cur
            cur.execute('''SELECT 
                             user_id, 
                             first_name, 
                             last_name 
                           FROM
                             users
                        WHERE user_id = %s
                           ''', (user_id,))
            return cur.fetchall()

    def new(self, first_name: str, last_name: str):
        with self.get_db_cursor(commit=True) as cur:  # type: Cur
            cur.execute("""INSERT INTO users (first_name, last_name) VALUES (%s, %s);""", (first_name, last_name))
            return cur.statusmessage

    def update(self, user_id: int, first_name: str, last_name: str):
        with self.get_db_cursor() as cur:
            cur.execute("""UPDATE users
                            SET first_name = %s, last_name = %s
                            WHERE publisher_id = %s;""", (first_name, last_name, user_id))
            return cur.statusmessage

    def delete(self, user_id: int):
        with self.get_db_cursor() as cur:
            cur.execute("""DELETE FROM users WHERE user_id = %s""", (user_id,))
            return cur.statusmessage
