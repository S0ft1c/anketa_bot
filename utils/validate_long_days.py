def validate_long_days(text: str):
    try:
        nn = int(text)
        if nn < 0:
            return False
        return True
    except Exception as e:
        return False
