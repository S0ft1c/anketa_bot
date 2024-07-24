from datetime import datetime


def validate_birth(text: str):
    try:
        date = datetime.strptime(text, '%d.%m.%Y')
        return True
    except Exception as e:
        return False
