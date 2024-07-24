import aiosqlite
from loguru import logger


class DB:
    def __init__(self):
        self.db_path = 'db.sqlite'
        self.orders_mask = ['id', 'customer_id', 'date', 'how_many_ppl', 'address', 'work_desc',
                            'payment', 'help_phone', 'FULL_address', 'FULL_work_desc', 'FULL_phones',
                            'FULL_additional_info', 'long_time', 'long_days']
        self.workers_mask = ['id', 'telegram_id', 'full_name', 'contact_number', 'tg_nickname', 'date_of_birth',
                             'area_of_residence', 'rating']

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(self.db_path)
        self.conn.row_factory = aiosqlite.Row
        await self.create_table()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.conn.close()

    async def create_table(self):
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_id STRING,
                date TEXT,
                how_many_ppl INTEGER,
                address TEXT,
                work_desc TEXT,
                payment REAL,
                help_phone TEXT,
                FULL_address TEXT,
                FULL_work_desc TEXT,
                FULL_phones TEXT,
                FULL_additional_info TEXT,
                long_time BOOLEAN,
                long_days INTEGER
            )
        ''')
        await self.conn.commit()
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS workers (
                id INTEGER PRIMARY KEY,
                telegram_id STRING,
                full_name TEXT,
                contact_number TEXT,
                tg_nickname TEXT,
                date_of_birth TEXT,
                area_of_residence TEXT,
                rating INTEGER
            )
        ''')
        await self.conn.commit()

    async def get_worker_by_tg_id(self, tg_id: int | str):
        try:
            cursor = await self.conn.execute('SELECT * FROM workers WHERE telegram_id=?', (str(tg_id),))
            worker_from_database = await cursor.fetchone()
            worker = {
                el: worker_from_database[idx]
                for idx, el in self.workers_mask
            }
            return worker
        except Exception as e:
            logger.error(f'Error in get_worker_by_tg_id -> {e}')

    async def insert_worker(
            self,
            telegram_id: int | str,
            full_name: str,
            contact_number: str,
            tg_nickname: str,
            date_of_birth: str,
            area_of_residence: str
    ):
        try:
            cursor = await self.conn.execute('''
            INSERT INTO workers (
                telegram_id, full_name, contact_number, tg_nickname, date_of_birth, area_of_residence, rating
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (str(telegram_id), full_name, contact_number, tg_nickname, date_of_birth, area_of_residence, 5,))
            await self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f'Error in insert_worker -> {e}')

    async def get_all_workers(self) -> dict:
        try:
            green_cursor = await self.conn.execute('SELECT * FROM workers WHERE rating >= 4')
            yellow_cursor = await self.conn.execute('SELECT * FROM workers WHERE rating >= 2 AND rating <= 3')
            red_cursor = await self.conn.execute('SELECT * FROM workers WHERE rating = 1')

            green_users = await green_cursor.fetchall()
            yellow_users = await yellow_cursor.fetchall()
            red_users = await red_cursor.fetchall()

            users = {
                'green': green_users,
                'yellow': yellow_users,
                'red': red_users
            }
            return users
        except Exception as e:
            logger.error(f'Error in get_all_workers -> {e}')

    async def insert_order(
            self,
            customer_id: str,
            date: str,
            how_many_ppl: int,
            address: str,
            work_desc: str,
            payment: int,
            help_phone: str,
            full_address: str,
            full_work_desc: str,
            full_phones: str,
            full_additional_info: str,
            long_time: bool = False,
            long_days: int = 0,
    ):
        try:
            async with self.conn.execute('''
            INSERT INTO orders (
                customer_id, date, how_many_ppl, address, work_desc, payment, help_phone,
                FULL_address, FULL_work_desc, FULL_phones, FULL_additional_info,
                long_time, long_days
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
                    customer_id, date, how_many_ppl, address,
                    work_desc, payment, help_phone,
                    full_address, full_work_desc, full_phones, full_additional_info,
                    long_time, long_days
            )) as cursor:
                await self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f'Error in sqlite_database: add_order_to_database -> {e}')

    async def select_orders_where_customer(self, customer_id: int | str) -> list[dict]:
        try:
            cursor = await self.conn.execute('SELECT * from orders WHERE customer_id = ?', (str(customer_id),))
            orders_from_database = await cursor.fetchall()
            orders = [{
                el: element_order[idx]
                for idx, el in enumerate(self.orders_mask)
            } for element_order in orders_from_database
            ]
            return orders
        except Exception as e:
            logger.error(f'Error in select_orders_where_customer -> {e}')

    async def select_order_by_id(self, order_id: int | str) -> dict:
        try:
            cursor = await self.conn.execute('SELECT * from orders WHERE id=?', (int(order_id),))
            order_from_database = await cursor.fetchone()
            orders = {
                el: order_from_database[idx]
                for idx, el in enumerate(self.orders_mask)
            }
            return orders
        except Exception as e:
            logger.error(f'Error in select_order_by_id -> {e}')

    async def update_long_days_in_order_by_id(self, order_id: int | str, days: int):
        try:
            cursor = await self.conn.execute('UPDATE orders SET long_days = ? WHERE id=?', (days, order_id,))
            await self.conn.commit()
        except Exception as e:
            logger.error(f'Error in update_long_days_in_order_by_id -> {e}')

    async def delete_order_by_id(self, order_id: int | str):
        try:
            cursor = await self.conn.execute('DELETE FROM orders WHERE id=?', (int(order_id),))
            await self.conn.commit()
        except Exception as e:
            logger.error(f'Error in delete_order_by_id -> {e}')
