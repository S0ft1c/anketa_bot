from datetime import datetime


async def create_now_time_text():
    now = datetime.now()
    return now.strftime('%H:%M %d.%m.%Y')
