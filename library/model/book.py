from library.model import AbstractDatabase
from psycopg2.extensions import cursor as Cur


class Book(AbstractDatabase):
    def __init__(self, pool):
        super().__init__(pool)

    def get_all_books(self) -> list:
        with self.get_db_cursor() as cur:  # type: Cur
            cur.execute('''SELECT 
                             book.book_id, 
                             book.title, 
                             book.page_number,
                             author.first_name,
                             author.last_name,
                             publisher.title publisher_name 
                           FROM
                             book
                           LEFT JOIN author ON author.author_id = book.author
                           LEFT JOIN publisher ON publisher.publisher_id = book.publisher;
                           ''')
            return cur.fetchall()

    def create_book(self, title: str, page_number: int, author_first_name: str, author_last_name: str,
                    publisher_title: str):
        with self.get_db_cursor(commit=True) as cur:  # type: Cur
            return cur.execute("""INSERT INTO book(title, page_number) VALUES (%s, %s)""", (title, page_number))
