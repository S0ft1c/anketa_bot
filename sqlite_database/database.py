import aiosqlite
from loguru import logger


class DB:
    def __init__(self):
        self.db_path = 'db.sqlite'
        self.orders_mask = ['id', 'customer_id', 'date', 'how_many_ppl', 'address', 'work_desc',
                            'payment', 'help_phone', 'FULL_address', 'FULL_work_desc', 'FULL_phones',
                            'FULL_additional_info', 'long_time', 'long_days']

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

    async def select_orders_where_customer(self, customer_id: int | str):
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
