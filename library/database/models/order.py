from library.database import AbstractDatabase
from datetime import datetime


class Order(AbstractDatabase):
    def __init__(self, pool):
        super().__init__(pool)

    def get_all(self):
        with self.get_db_cursor() as cur:
            cur.execute("""SELECT
                           order_id,
                           user_id,
                           inventory,  
                           to_char(return_date, 'YYYY-MM-DD') as return_date
                           FROM orders""")
            return cur.fetchall()

    def get(self, order_id: int):
        with self.get_db_cursor() as cur:
            cur.execute("""SELECT
                           order_id,
                           user_id,
                           inventory,  
                           to_char(return_date, 'YYYY-MM-DD') as return_date
                           FROM orders
                           WHERE order_id = %s""", (order_id,))
            return cur.fetchone()

    def new(self, user_id: str, inventory: str, return_date: datetime):
        with self.get_db_cursor(commit=True) as cur:
            cur.execute("""INSERT INTO orders (user_id, inventory, return_date) VALUES (%s, %s, %s) 
                           RETURNING order_id;""",
                        (user_id, inventory, return_date))
            return cur.fetchone()

    def update(self, order_id: int, user_id: str, inventory: str, return_date: str):
        with self.get_db_cursor(commit=True) as cur:
            cur.execute("""UPDATE orders
                        SET user_id = %s, inventory = %s, return_date = %s
                        WHERE order_id = %s;""", (user_id, inventory, return_date, order_id))
            return cur.statusmessage == "UPDATE 1"

    def delete(self, order_id: int):
        with self.get_db_cursor(commit=True) as cur:
            cur.execute("""DELETE FROM orders WHERE order_id = %s""", (order_id,))
            return cur.statusmessage == "DELETE 1"
