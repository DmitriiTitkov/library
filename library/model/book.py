from library.model import AbstractDatabase
from psycopg2.extensions import cursor as Cur


class Book(AbstractDatabase):
    def __init__(self, pool):
        super().__init__(pool)
        self.author_fields = ["author_id", "first_name", "last_name"]
        self.publisher_fields = ["publisher_id", "publisher_name"]

    def _transform_full_book_data(self, sql_book_list) -> list:
        result = []
        for row in sql_book_list:
            new_row = {k: v for k, v in row.items() if k not in self.author_fields and k not in self.publisher_fields}
            new_row["author"] = {k: row[k] for k in self.author_fields}
            new_row["publisher"] = {k: row[k] for k in self.publisher_fields}
            result.append(new_row)
        return result
    # TODO: Error handlers for ALL DB calls
    def get_all_books(self) -> list:
        with self.get_db_cursor() as cur:  # type: Cur
            cur.execute('''SELECT 
                             book.book_id, 
                             book.title, 
                             book.page_number,
                             author_id,
                             author.first_name,
                             author.last_name,
                             publisher_id,
                             publisher.title publisher_name 
                           FROM
                             book
                           LEFT JOIN author ON author.author_id = book.author
                           LEFT JOIN publisher ON publisher.publisher_id = book.publisher;
                           ''')
            return self._transform_full_book_data(cur.fetchall())

    def get_book(self, book_id: int) -> dict:
        with self.get_db_cursor() as cur:  # type: Cur
            cur.execute('''SELECT 
                             book.book_id, 
                             book.title, 
                             book.page_number,
                             author_id,
                             author.first_name,
                             author.last_name,
                             publisher_id,
                             publisher.title publisher_name 
                           FROM
                             book
                           LEFT JOIN author ON author.author_id = book.author
                           LEFT JOIN publisher ON publisher.publisher_id = book.publisher
                           WHERE book_id = %s;
                           ''', (book_id,))
            return self._transform_full_book_data(cur.fetchall())[0]

    def create_book(self, title: str, page_number: int, author_id: int, publisher_id: int) -> dict:
        with self.get_db_cursor(commit=True) as cur:  # type: Cur
            cur.execute("""INSERT INTO book(title, page_number, author, publisher) VALUES (%s, %s, %s, %s) 
                                RETURNING book_id;""", (title, page_number, author_id, publisher_id))
            return cur.fetchone()

    def update_book(self, book_id: int, title: str, page_number: int, author_id: int, publisher_id: int) -> str:
        with self.get_db_cursor(commit=True) as cur:  # type: Cur
            cur.execute("""UPDATE book
                        SET title = %s, page_number = %s, author = %s, publisher = %s
                        WHERE book_id = %s;""", (title, page_number, author_id, publisher_id, book_id))
            return cur.statusmessage

    def delete_book(self, book_id):
        with self.get_db_cursor(commit=True) as cur:  # type: Cur
            cur.execute("""DELETE FROM book
                           WHERE book_id = %s;""", (book_id,))
            return cur.statusmessage

    def create_book_full(self, title: str, page_number: int, author_first_name: str, author_last_name: str,
                         publisher_title: str):
        with self.get_db_cursor(commit=True) as cur:  # type: Cur
            return cur.execute(
                """WITH data(first_name, last_name, publisher_title, book_title, page_number) as (
                        VALUES(
                            text %s, text %s,, text %s,, text %s, int %s,
                        )
                    ),
                    ins1 AS(
                        INSERT INTO author (first_name, last_name)
                        SELECT first_name, last_name FROM data
                        ON CONFLICT DO NOTHING
                        RETURNING author_id, first_name, last_name
                    ),
                    ins2 AS(
                        INSERT INTO publisher (title)
                        SELECT publisher_title FROM data
                        RETURNING publisher_id, title
                    )
                    INSERT INTO book 
                      (title, page_number, author, publisher) 
                      SELECT book_title, page_number, author_id, publisher_id FROM data
                      JOIN ins1 USING(first_name, last_name)
                      JOIN ins2 
                      ON data.publisher_title = ins2.title;
          """, (author_first_name, author_last_name, publisher_title, title, page_number))
