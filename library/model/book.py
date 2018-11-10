from library.model import AbstractDatabase


class Book(AbstractDatabase):
    def __init__(self, pool):
        super().__init__(pool)

    def get_all_books(self):
        with self.get_db_cursor() as cur:
            cur.execute("SELECT * FROM books")
            return cur.fetchone()
