def validate_how_many_ppl(text):
    try:
        nn = int(text)
        return True if nn > 0 else False
    except Exception as e:
        return False
