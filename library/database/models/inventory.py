from psycopg2.extras import execute_values

from library.database import AbstractDatabase
from datetime import datetime


class Inventory(AbstractDatabase):
    def __init__(self, pool):
        super().__init__(pool)

    def get_all(self):
        with self.get_db_cursor() as cur:
            cur.execute("""SELECT 
                             inventory.inventory_id,
                             inventory.isbn,
                             inventory.page_number,
                             inventory.edition,
                             to_char(inventory.year_published, 'YYYY') as year_published,
                             
                             json_build_object('book_id',book.book_id, 'title',book.title) as book,
                             json_build_object('author_id',author.author_id, 'first_name',author.first_name, 
                                               'last_name',author.last_name) as author,
                             json_build_object('publisher_id',publisher.publisher_id, 'title',publisher.title) 
                             as publisher                             
                           FROM 
                             inventory
                           LEFT JOIN book ON book.book_id = inventory.book
                           LEFT JOIN publisher ON publisher.publisher_id = inventory.publisher
                           LEFT JOIN author on book.author = author.author_id;
                           
                        """)
            return cur.fetchall()

    def get(self, inventory_id: int):
        with self.get_db_cursor() as cur:
            cur.execute("""SELECT 
                             inventory.inventory_id,
                             inventory.isbn,
                             inventory.page_number,
                             inventory.edition,
                             to_char(inventory.year_published, 'YYYY') as year_published,
                             
                             json_build_object('book_id',book.book_id, 'title',book.title) as book,
                             json_build_object('author_id',author.author_id, 'first_name',author.first_name, 
                                               'last_name',author.last_name) as author,
                             json_build_object('publisher_id',publisher.publisher_id, 'title',publisher.title) 
                             as publisher                             
                           FROM 
                             inventory
                           LEFT JOIN book ON book.book_id = inventory.book
                           LEFT JOIN publisher ON publisher.publisher_id = inventory.publisher
                           LEFT JOIN author on book.author = author.author_id
                           WHERE 
                           inventory_id = %s;
                        """, (inventory_id,))
            return cur.fetchone()

    def new(self, book_id: int, publisher_id: str, isbn: str, page_number: int, edition: str, year_published: datetime,
            amount: int):
        with self.get_db_cursor(commit=True) as cur:
            execute_values(cur,
                           """INSERT INTO inventory (book, publisher, isbn, page_number, edition, year_published) 
                           VALUES %s RETURNING inventory_id;""",
                           [(book_id, publisher_id, isbn, page_number, edition, year_published)] * amount)
            return cur.fetchall()

    def update(self, inventory_id: int, book_id: int, publisher_id: str, isbn: str, page_number: int, edition: str,
               year_published: datetime):
        with self.get_db_cursor(commit=True) as cur:
            cur.execute("""UPDATE inventory
                        SET book = %s, publisher = %s, isbn = %s, page_number = %s, edition = %s, year_published = %s
                        WHERE inventory_id = %s;""",
                        (book_id, publisher_id, isbn, page_number, edition, year_published, inventory_id))
            return cur.statusmessage == "UPDATE 1"

    def delete(self, inventory_id: int):
        with self.get_db_cursor(commit=True) as cur:
            cur.execute("""DELETE FROM inventory WHERE inventory_id = %s""", (inventory_id,))
            return cur.statusmessage == "DELETE 1"
