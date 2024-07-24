from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .send_order_to_workers import send_order_to_workers

scheduler = AsyncIOScheduler()
