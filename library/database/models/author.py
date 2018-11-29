from library.database import AbstractDatabase


class Author(AbstractDatabase):
    def __init__(self, pool):
        super().__init__(pool)

    def get_all(self):
        with self.get_db_cursor() as cur:
            cur.execute("SELECT * FROM author")
            return cur.fetchall()

    def get(self, author_id):
        with self.get_db_cursor() as cur:
            cur.execute("""SELECT * FROM author WHERE author_id = %s""", (author_id,))
            return cur.fetchone()

    def new(self, first_name, last_name):
        with self.get_db_cursor(commit=True) as cur:
            cur.execute("""INSERT INTO author (first_name, last_name) VALUES (%s, %s) RETURNING author_id""", (first_name, last_name))
            return cur.fetchone()

    def update(self, author_id, first_name, last_name):
        with self.get_db_cursor(commit=True) as cur:
            cur.execute("""UPDATE author
                        SET first_name = %s, last_name = %s
                        WHERE author_id = %s;""", (first_name, last_name, author_id))
            if cur.statusmessage == "UPDATE 1":
                return True

    def delete(self, author_id):
        with self.get_db_cursor(commit=True) as cur:
            cur.execute("""DELETE FROM author WHERE author_id = %s""", (author_id,))
            if cur.statusmessage == "DELETE 1":
                return True

