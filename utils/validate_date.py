from datetime import datetime


def is_valid_datetime(date_str):
    try:
        # Attempt to parse the date string with the given format
        datetime.strptime(date_str, '%H:%M %d.%m.%Y')
        return True
    except ValueError:
        # If parsing fails, the format is incorrect
        return False
