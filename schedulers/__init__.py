from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .send_order_to_workers import send_order_to_workers
from .repeat_long_time_order import repeat_long_time_order

scheduler = AsyncIOScheduler()
