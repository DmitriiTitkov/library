from library.model import AbstractDatabase
from psycopg2.extensions import cursor as Cur


class User(AbstractDatabase):
    def __init__(self, pool):
        super().__init__(pool)

    def get_all_users(self):
        with self.get_db_cursor() as cur:  # type: Cur
            cur.execute('''SELECT 
                             user_id, 
                             first_name, 
                             last_name 
                           FROM
                             users
                           ''')
            return cur.fetchall()

    def get_user(self):
        pass

    def add_user(self, first_name: str, last_name: str):
        with self.get_db_cursor(commit=True) as cur:  # type: Cur
            cur.execute("""INSERT INTO users (first_name, last_name) VALUES (%s, %s);""", (first_name, last_name))
            return cur.statusmessage
