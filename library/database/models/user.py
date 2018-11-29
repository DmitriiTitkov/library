from library.database import AbstractDatabase
from psycopg2.extensions import cursor as Cur


class User(AbstractDatabase):
    def __init__(self, pool):
        super().__init__(pool)

    def get_all(self):
        with self.get_db_cursor() as cur:  # type: Cur
            cur.execute('''SELECT 
                             user_id, 
                             login,
                             first_name, 
                             last_name,
                             email 
                           FROM
                             users
                           ''')
            return cur.fetchall()

    def get(self, user_id: int):
        with self.get_db_cursor() as cur:  # type: Cur
            cur.execute('''SELECT 
                             user_id, 
                             login,
                             first_name, 
                             last_name,
                             email  
                           FROM
                             users
                        WHERE user_id = %s
                           ''', (user_id,))
            return cur.fetchall()

    def new(self, first_name: str, last_name: str, login: str, password: str, email: str):
        with self.get_db_cursor(commit=True) as cur:  # type: Cur
            cur.execute(
                """INSERT INTO users (first_name, last_name, login, password, email) 
                   VALUES (%s, %s, %s, %s, %s) RETURNING user_id;""",
                (first_name, last_name, login, password, email))
            return cur.fetchone()

    def update(self, user_id: int, first_name: str, last_name: str, login: str, password: str, email: str):
        with self.get_db_cursor(commit=True) as cur:
            cur.execute("""UPDATE users
                            SET first_name = %s, last_name = %s, login = %s, password = %s, email = %s
                            WHERE user_id = %s;""", (first_name, last_name, login, password, email, user_id))
            return cur.statusmessage == "UPDATE 1"

    def delete(self, user_id: int):
        with self.get_db_cursor(commit=True) as cur:
            cur.execute("""DELETE FROM users WHERE user_id = %s""", (user_id,))
            return cur.statusmessage == "DELETE 1"
