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
        self.inwork_mask = ['id', 'worker_id', 'order_id', 'start_date', 'end_date']
        self.admin_reviews_mask = ['id', 'customer_id', 'worker_id', 'date', 'how_many_ppl', 'address', 'work_desc',
                                   'payment', 'help_phone', 'FULL_address', 'FULL_work_desc', 'FULL_phones',
                                   'FULL_additional_info', 'long_time', 'long_days', 'report', 'start_date', 'end_date']
        self.admin_logs_mask = ['id', 'customer_id', 'worker_id', 'date', 'how_many_ppl', 'address', 'work_desc',
                                'payment', 'help_phone', 'FULL_address', 'FULL_work_desc', 'FULL_phones',
                                'FULL_additional_info', 'long_time', 'long_days', 'report', 'hours']
        self.admins_mask = ['id', 'telegram_id']

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
        await self.conn.execute('''
        CREATE TABLE IF NOT EXISTS inwork (
            id INTEGER PRIMARY KEY,
            worker_id STRING,
            order_id STRING, 
            start_date TEXT,
            end_date TEXT
        )
        ''')
        await self.conn.commit()
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS admin_reviews (
                id INTEGER PRIMARY KEY,
                customer_id STRING,
                worker_id STRING,
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
                long_days INTEGER,
                report TEXT,
                start_date TEXT,
                end_date TEXT
            )
        ''')
        await self.conn.commit()
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS admin_logs (
                id INTEGER PRIMARY KEY,
                customer_id STRING,
                worker_id STRING,
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
                long_days INTEGER,
                report TEXT,
                hours INTEGER
            )
        ''')
        await self.conn.commit()
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY,
                telegram_id STRING
            )
        ''')
        await self.conn.commit()

    async def delete_admin_by_telegram_id(self, telegram_id: int | str):
        try:
            cursor = await self.conn.execute('DELETE FROM admins WHERE telegram_id=?', (str(telegram_id),))
            await self.conn.commit()
            return True
        except Exception as e:
            logger.error(f'Error in delete_admin_by_telegram_id -> {e}')

    async def select_all_orders(self):
        try:
            cursor = await self.conn.execute('SELECT * FROM orders')
            orders_from_db = await cursor.fetchall()
            result = [
                {
                    el: ordr[idx]
                    for idx, el in enumerate(self.orders_mask)
                }
                for ordr in orders_from_db
            ]
            return result
        except Exception as e:
            logger.error(f'Error in select_all_inworks')

    async def select_all_inworks(self):
        try:
            cursor = await self.conn.execute('SELECT * FROM inwork')
            inwork_from_db = await cursor.fetchall()
            result = [
                {
                    el: inwork[idx]
                    for idx, el in enumerate(self.inwork_mask)
                }
                for inwork in inwork_from_db
            ]
            return result
        except Exception as e:
            logger.error(f'Error in select_all_inworks')

    async def select_all_admins(self):
        try:
            cursor = await self.conn.execute('SELECT * FROM admins')
            admins_from_database = await cursor.fetchall()

            result = [
                {
                    el: admin[idx]
                    for idx, el in enumerate(self.admins_mask)
                }
                for admin in admins_from_database
            ]
            return result
        except Exception as e:
            logger.error(f'Error in select_all_admins -> {e}')

    async def insert_admin(self, telegram_id: int | str):
        try:
            cursor = await self.conn.execute('INSERT INTO admins (telegram_id) VALUES (?)', (str(telegram_id),))
            await self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f'Error in insert_admin -> {e}')

    async def select_worker_by_username(self, username: str):
        try:
            cursor = await self.conn.execute('SELECT * FROM workers WHERE tg_nickname=?', (username,))
            worker_from_database = await cursor.fetchone()
            result = {
                el: worker_from_database[idx]
                for idx, el in enumerate(self.workers_mask)
            }
            return result

        except Exception as e:
            logger.error(f'Error in select_worker_by_username: {e}')

    async def select_all_admin_logs(self):
        try:
            cursor = await self.conn.execute('SELECT * FROM admin_logs')
            data = await cursor.fetchall()
            result = [
                {
                    el: ddd[idx]
                    for idx, el in enumerate(self.admin_logs_mask)
                }
                for ddd in data
            ]
            return result
        except Exception as e:
            logger.error(f'Error in select_all_admin_logs -> {e}')

    async def select_long_projects_from_orders(self):
        try:
            cursor = await self.conn.execute('SELECT * FROM orders WHERE long_time = True AND long_days = 0')
            orders_from_database = await cursor.fetchall()
            result = [
                {
                    el: order[idx]
                    for idx, el in enumerate(self.orders_mask)
                }
                for order in orders_from_database
            ]
            return result
        except Exception as e:
            logger.error(f'Error in select_long_projects_from_orders: {e}')

    async def decrease_worker_rating(self, worker_id: int | str):
        try:
            cursor = await self.conn.execute('''
                UPDATE workers SET rating = rating - 1 WHERE telegram_id = ? AND rating > 0
            ''', (str(worker_id),))
            await self.conn.commit()
            return True
        except Exception as e:
            logger.error(f'Error in update_worker_rating: {e}')

    async def delete_review_by_id(self, review_id: int | str):
        try:
            cursor = await self.conn.execute('DELETE FROM admin_reviews WHERE id=?', (review_id,))
            await self.conn.commit()
            return True
        except Exception as e:
            logger.error(f'Error in delete_review_by_id: {e}')

    async def update_worker_rating(self, worker_id: int | str):
        try:
            cursor = await self.conn.execute('''
                UPDATE workers SET rating = rating + 1 WHERE telegram_id = ? AND rating < 5
            ''', (str(worker_id),))
            await self.conn.commit()
            return True
        except Exception as e:
            logger.error(f'Error in update_worker_rating: {e}')

    async def select_admin_logs_by_worker_id(self, worker_id: int | str):
        try:
            cursor = await self.conn.execute('SELECT * FROM admin_logs WHERE worker_id = ?', (str(worker_id),))
            logs_from_db = await cursor.fetchall()
            result = [
                {
                    el: log[idx]
                    for idx, el in enumerate(self.admin_logs_mask)
                }
                for log in logs_from_db
            ]
            return result
        except Exception as e:
            logger.error(f'Error in select_admin_logs_by_worker_id({worker_id}): {e}')

    async def insert_admin_log(
            self,
            customer_id: str,
            worker_id: str,
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
            report: str = None,
            hours: int = 0
    ):
        try:
            cursor = await self.conn.execute('''
                INSERT INTO admin_logs (
                    customer_id, worker_id, date, how_many_ppl, address,
                    work_desc, payment, help_phone,
                    full_address, full_work_desc, full_phones, full_additional_info,
                    long_time, long_days, report, hours
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (
                customer_id, worker_id, date, how_many_ppl, address,
                work_desc, payment, help_phone,
                full_address, full_work_desc, full_phones, full_additional_info,
                long_time, long_days, report, hours
            ))
            await self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f'Error in insert_admin_log: {e}')

    async def select_review_by_id(self, review_id: int | str):
        try:
            cursor = await self.conn.execute('SELECT * FROM admin_reviews WHERE id=?', (int(review_id),))
            row = await cursor.fetchone()
            return row
        except Exception as e:
            logger.error(f'Error in select_review_by_id: {e}')

    async def select_all_admin_reviews(self):
        try:
            cursor = await self.conn.execute('SELECT * FROM admin_reviews')
            admin_reviews_from_database = await cursor.fetchall()
            result = [
                {
                    el: rev[idx]
                    for idx, el in enumerate(self.admin_reviews_mask)
                }
                for rev in admin_reviews_from_database
            ]
            return result
        except Exception as e:
            logger.error(f'Error in select_all_admin_reviews: {e}')

    async def insert_admin_review(
            self,
            customer_id: str,
            worker_id: str,
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
            report: str = None,
            start_date: str = None,
            end_date: str = None
    ):
        try:
            cursor = await self.conn.execute('''
                INSERT INTO admin_reviews (
                    customer_id, worker_id, date, how_many_ppl, address,
                    work_desc, payment, help_phone,
                    full_address, full_work_desc, full_phones, full_additional_info,
                    long_time, long_days, report, start_date, end_date
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (
                customer_id, worker_id, date, how_many_ppl, address,
                work_desc, payment, help_phone,
                full_address, full_work_desc, full_phones, full_additional_info,
                long_time, long_days, report, start_date, end_date
            ))
            await self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f'Error in insert_admin_review: {e}')

    async def delete_inwork_by_order_id(self, order_id: str | int):
        try:
            cursor = await self.conn.execute('DELETE FROM inwork WHERE order_id=?', (order_id,))
            await self.conn.commit()
            return True
        except Exception as e:
            logger.error(f'Error in delete_inwork_by_order_id: {e}')

    async def delete_order_by_order_id(self, order_id: str | int):
        try:
            cursor = await self.conn.execute('DELETE FROM orders WHERE id=?', (order_id,))
            await self.conn.commit()
            return True
        except Exception as e:
            logger.error(f'Error in delete_order_by_order_id: {e}')

    async def update_start_date_inwork(self, worker_id: int | str, order_id: str | int, start_time: str):
        try:
            cursor = await self.conn.execute('UPDATE inwork SET start_date = ? WHERE worker_id = ? AND order_id=?',
                                             (start_time, str(worker_id), str(order_id),))
            await self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f'Error in update_start_date_inwork: {e}')

    async def update_end_date_inwork(self, worker_id: int | str, order_id: str | int, end_time: str):
        try:
            cursor = await self.conn.execute('UPDATE inwork SET end_date = ? WHERE worker_id = ? AND order_id=?',
                                             (end_time, str(worker_id), str(order_id),))
            await self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f'Error in update_end_date_inwork: {e}')

    async def select_inwork_by_worker_n_order_id(self, worker_id: str | int, order_id: str | int):
        try:
            cursor = await self.conn.execute('SELECT * FROM inwork WHERE worker_id = ? AND order_id = ?',
                                             (str(worker_id), str(order_id),))
            inwork_from_database = await cursor.fetchone()
            if not inwork_from_database:
                return False

            result = {
                el: inwork_from_database[idx]
                for idx, el in enumerate(self.inwork_mask)
            }
            return result

        except Exception as e:
            logger.error(f'Error in select_inwork_by_worker_n_order_id: {e}')

    async def select_all_inwork_by_order_id(self, order_id: int | str):
        try:
            cursor = await self.conn.execute('SELECT * FROM inwork WHERE order_id = ?',
                                             (str(order_id),))
            inworks_from_db = await cursor.fetchall()
            result = [
                {
                    el: inwork[idx]
                    for idx, el in enumerate(self.inwork_mask)
                }
                for inwork in inworks_from_db
            ]
            return result
        except Exception as e:
            logger.error(f'Error in select_all_inwork_by_order_id : {e}')

    async def select_all_inwork_by_worker_id(self, worker_id: str | int):
        try:
            cursor = await self.conn.execute('SELECT * FROM inwork WHERE worker_id = ?', (str(worker_id),))
            result = [
                {
                    el: inwork[idx]
                    for idx, el in enumerate(self.inwork_mask)
                }
                for inwork in await cursor.fetchall()
            ]
            return result
        except Exception as e:
            logger.error(f'Error in select_all_inwork_by_worker_id: {e}')

    async def insert_inwork(self, worker_id: int | str, order_id: int | str):
        try:
            cursor = await self.conn.execute('INSERT INTO inwork (worker_id, order_id) VALUES (?, ?)',
                                             (str(worker_id), str(order_id),))
            await self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f'Error in insert_inwork: {e}')

    async def get_worker_by_tg_id(self, tg_id: int | str):
        try:
            cursor = await self.conn.execute('SELECT * FROM workers WHERE telegram_id=?', (str(tg_id),))
            worker_from_database = await cursor.fetchone()
            worker = {
                el: worker_from_database[idx]
                for idx, el in enumerate(self.workers_mask)
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

    async def get_all_workers(self, rated: bool = True):
        try:
            if rated:
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
            else:
                cursor = await self.conn.execute('SELECT * FROM workers')
                workers_from_db = await cursor.fetchall()
                result = [
                    {
                        el: worker[idx]
                        for idx, el in enumerate(self.workers_mask)
                    }
                    for worker in workers_from_db
                ]
                return result

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
