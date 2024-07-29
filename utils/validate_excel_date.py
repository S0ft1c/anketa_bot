from datetime import datetime

from loguru import logger


def validate_excel_date(date: str):
    try:

        date = datetime.strptime(date, '%d.%m.%Y')
        return True
    except Exception as e:
        logger.warning(f'Error in validate_excel_date: {e}')
        return False
