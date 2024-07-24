import re


def is_valid_phone_number(phone_number):
    # Регулярное выражение для проверки телефонного номера
    phone_pattern = re.compile(r'^\+?\d{1,4}?[-.\s]?(\d{1,3}?[-.\s]?){1,4}$')

    # Проверяем, соответствует ли номер шаблону
    return bool(phone_pattern.match(phone_number))
