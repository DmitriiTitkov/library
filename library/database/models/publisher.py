from library.database import AbstractDatabase


class Publisher(AbstractDatabase):
    def __init__(self, pool):
        super().__init__(pool)

    def get_all(self):
        with self.get_db_cursor() as cur:
            cur.execute("SELECT * FROM publisher")
            return cur.fetchall()

    def get(self, publisher_id):
        with self.get_db_cursor() as cur:
            cur.execute("""SELECT * FROM publisher WHERE publisher_id = %s""", (publisher_id,))
            return cur.fetchone()

    def new(self, title: str):
        with self.get_db_cursor(commit=True) as cur:
            cur.execute("""INSERT INTO publisher (title) VALUES (%s) RETURNING publisher_id;""", (title,))
            return cur.fetchone()

    def update(self, publisher_id, title: str):
        with self.get_db_cursor(commit=True) as cur:
            cur.execute("""UPDATE publisher
                        SET title = %s
                        WHERE publisher_id = %s;""", (title, publisher_id))
            if cur.statusmessage == "UPDATE 1":
                return True

    def delete(self, publisher_id):
        with self.get_db_cursor(commit=True) as cur:
            cur.execute("""DELETE FROM publisher WHERE publisher_id = %s""", (publisher_id,))
            if cur.statusmessage == "DELETE 1":
                return True
