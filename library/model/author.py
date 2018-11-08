from library.model import AbstractDatabase


class Author(AbstractDatabase):
    def __init__(self, pool):
        super().__init__(pool)

    def get_all_authors(self):
        with self.get_db_cursor() as cur:
            cur.execute("SELECT * FROM author")
            return cur.fetchone()
