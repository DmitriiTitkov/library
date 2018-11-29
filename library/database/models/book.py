from library.database import AbstractDatabase
from psycopg2.extensions import cursor as Cur


# TODO: add many to many  books <-> authors
class Book(AbstractDatabase):
    def __init__(self, pool):
        super().__init__(pool)


    # TODO: Error handlers for ALL DB calls
    def get_all(self) -> list:
        with self.get_db_cursor() as cur:  # type: Cur
            cur.execute('''SELECT 
                             book.book_id, 
                             book.title, 
                             json_build_object('author_id', author_id, 'first_name',author.first_name, 
                                               'last_name',author.last_name) as book,
                             (SELECT count(*) FROM 
                                (SELECT 
                                  inventory_id, 
                                  book 
                                 FROM inventory
                                 WHERE book = book.book_id
                                 EXCEPT
                                 SELECT 
                                  orders.inventory, 
                                  book 
                                 FROM inventory
                                 INNER JOIN orders ON orders.inventory = inventory.inventory_id
                                 WHERE book = book.book_id 

                                ) as not_ordered_books
                             ) as available_book_count
                           FROM
                             book
                           LEFT JOIN author ON author.author_id = book.author
                           ''')
            return cur.fetchall()

    def get(self, book_id: int) -> dict:
        with self.get_db_cursor() as cur:  # type: Cur
            cur.execute('''SELECT 
                             book.book_id, 
                             book.title, 
                             json_build_object('author_id', author_id, 'first_name',author.first_name, 
                                               'last_name',author.last_name) as book,
                             (SELECT count(*) FROM 
                                (SELECT 
                                  inventory_id, 
                                  book 
                                 FROM inventory
                                 WHERE book = book.book_id
                                 EXCEPT
                                 SELECT 
                                  orders.inventory, 
                                  book 
                                 FROM inventory
                                 INNER JOIN orders ON orders.inventory = inventory.inventory_id
                                 WHERE book = book.book_id 

                                ) as not_ordered_books
                             ) as available_book_count
                           FROM
                             book
                           LEFT JOIN author ON author.author_id = book.author
                           WHERE book_id = %s;
                           ''', (book_id,))
            return cur.fetchone()

    def new(self, title: str, author_id: int) -> dict:
        with self.get_db_cursor(commit=True) as cur:  # type: Cur
            cur.execute("""INSERT INTO book(title, author) VALUES (%s, %s) 
                                RETURNING book_id;""", (title, author_id))
            return cur.fetchone()

    def update(self, book_id: int, title: str, author_id: int) -> str:
        with self.get_db_cursor(commit=True) as cur:  # type: Cur
            cur.execute("""UPDATE book
                        SET title = %s, author = %s
                        WHERE book_id = %s;""", (title, author_id, book_id))
            return cur.statusmessage == "UPDATE 1"

    def delete(self, book_id):
        with self.get_db_cursor(commit=True) as cur:  # type: Cur
            cur.execute("""DELETE FROM book
                           WHERE book_id = %s;""", (book_id,))
            return cur.statusmessage == "DELETE 1"


    # TODO: Already refactored. Do I need to move to inventory?
    # def create_book_full(self, title: str, page_number: int, author_first_name: str, author_last_name: str,
    #                      publisher_title: str):
    #     with self.get_db_cursor(commit=True) as cur:  # type: Cur
    #         return cur.execute(
    #             """WITH data(first_name, last_name, publisher_title, book_title, page_number) as (
    #                     VALUES(
    #                         text %s, text %s,, text %s,, text %s, int %s,
    #                     )
    #                 ),
    #                 ins1 AS(
    #                     INSERT INTO author (first_name, last_name)
    #                     SELECT first_name, last_name FROM data
    #                     ON CONFLICT DO NOTHING
    #                     RETURNING author_id, first_name, last_name
    #                 ),
    #                 ins2 AS(
    #                     INSERT INTO publisher (title)
    #                     SELECT publisher_title FROM data
    #                     RETURNING publisher_id, title
    #                 )
    #                 INSERT INTO book
    #                   (title, page_number, author, publisher)
    #                   SELECT book_title, page_number, author_id, publisher_id FROM data
    #                   JOIN ins1 USING(first_name, last_name)
    #                   JOIN ins2
    #                   ON data.publisher_title = ins2.title;
    #       """, (author_first_name, author_last_name, publisher_title, title, page_number))
