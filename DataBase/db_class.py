import sqlite3 as sql

class DataBase:

    '''class for data base managements'''


    file = "DataBase\pizza.db"


    def __init__(self) -> None:
        self.con = sql.connect(database=self.file)
        self.cur = self.con.cursor()
    

    def check_user_exists(self, user_id) -> bool:
        result = self.cur.execute("""SELECT * FROM `users` WHERE user_id = (?)""", (user_id,))
        return result.fetchall()

    
    def add_user(self, user_id, email, lat, lon, date) -> None:
        self.cur.execute("""INSERT INTO `users` (user_id, email, lat, lon, registr_date) VALUES (?, ?, ?, ?, ?)""", (user_id, email, lat, lon, date))
        self.close_db()


    def edit_user_email(self, email, user_id) -> None:
        self.cur.execute("""UPDATE `users` SET `email` = ? WHERE `user_id` = ?""", (email, user_id))
        self.close_db()
    

    def edit_user_address(self, user_id, lat, lon) -> None:
        self.cur.execute("""UPDATE `users` SET `lat` = ?, `lon` = ?WHERE `user_id` = ?""", (lat, lon, user_id))
        self.close_db()
    

    def get_user_address(self, user_id) -> tuple:
        self.cur.execute("""SELECT `lat`, `lon` FROM `users` WHERE user_id = ?""", (user_id,))
        return self.cur.fetchone()
    

    def get_user_email(self, user_id) -> str:
        self.cur.execute("""SELECT `email` FROM `users` WHERE user_id = ?""", (user_id,))
        return self.cur.fetchone()[0]
    

    def get_menu(self) -> list:
        pizzas = self.cur.execute("""SELECT `name`, `descr`, `image`, `price`, `id` FROM `pizzas`""")
        return pizzas.fetchall()

    
    def get_basket(self, user_id) -> str:
        self.cur.execute("""SELECT `basket` FROM `users` WHERE user_id = ?""", (user_id,))
        return self.cur.fetchone()[0][0 : -1] # delete last ',' in string


    def get_pizza_name(self, pizza_id) -> str:
        self.cur.execute("""SELECT `name` FROM `pizzas` WHERE `id` = ?""", (pizza_id,))
        return self.cur.fetchone()[0]
    

    def get_pizza_price(self, pizza_id) -> float:
        self.cur.execute("""SELECT `price` FROM `pizzas` WHERE `id` = ?""", (pizza_id,))
        return self.cur.fetchone()[0]


    def add_to_basket(self, pizza, user_id) -> None:
        basket = self.get_basket(user_id)
        if basket: basket += ','
        self.cur.execute("""UPDATE `users` SET `basket` = ? WHERE `user_id` = ?""",  (f"{basket}{pizza},", user_id))
        self.close_db()


    def delete_from_basket(self, pizza, user_id) -> None:
        
        '''delete one pizza from basket with such name and size'''
        
        basket = f"{self.get_basket(user_id)}".split(',')
        basket.remove(pizza)
        self.cur.execute("""UPDATE `users` SET `basket` = ? WHERE `user_id` = ?""", (f"{','.join(basket)},", user_id))
        self.close_db()


    def kill_pizza_basket(self, pizza, user_id) -> None:

        ''' deleting all pizzas from basket with such name and size'''

        basket = f"{self.get_basket(user_id)}".split(',')
        n = basket.count(pizza)
        for i in range(n):
            basket.remove(pizza)
        self.cur.execute("""UPDATE `users` SET `basket` = ? WHERE `user_id` = ?""", (f"{','.join(basket)},", user_id))
        self.close_db()


    def clear_basket(self, user_id: int) -> None:

        '''making user basket empty after making order'''

        self.cur.execute("UPDATE `users` SET `basket` = '' WHERE `user_id` = ?", (user_id,))
        self.close_db()


    def make_order(self, user_id, date_time, lat, lon, total, shop_adress, order_type) -> None:
        self.cur.execute("""INSERT INTO `orders` 
        (`user_id`, `date_time`, `lat`, `lon`, `total`, `shop_address`, `basket`, `order_type`) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (user_id, date_time, lat, lon, total, shop_adress, self.get_basket(user_id), order_type))
        self.clear_basket(user_id)
        self.close_db()

    
    def add_pizza_in_db(self, name: str, descr: str, price: float, image: str) -> None:
        self.cur.execute(
            """INSERT INTO `pizzas` (name, descr, price, image)
                VALUES (?, ?, ?, ?)
            """,
            (name, descr, price, image)
        )
        self.close_db()
    

    def redact_pizza(self, pizza_id, key, value) -> None:
        
        '''setting new value of some parametr of pizza'''
        
        self.cur.execute(
            f"""UPDATE `pizzas` SET {key} = ? WHERE id = ?""",
            (value, pizza_id)
        )
        self.close_db()

    
    def get_user_id_list(self) -> list:
        
        '''list of users id for mailing'''

        self.cur.execute(
            "SELECT `user_id` FROM `users`"
        )
        return self.cur.fetchall()


    def get_pizza_names(self) -> dict:
        self.cur.execute(
            """SELECT `id`, `name` FROM `pizzas`"""
        )
        return self.cur.fetchall()


    def get_order_id(self) -> int:

        '''geting order_id for buyer'''

        self.cur.execute('SELECT max(`id`) FROM `orders`')
        return self.cur.fetchone()[0]
    

    def close_db(self) -> None: # saving changes in DB
        self.con.commit()