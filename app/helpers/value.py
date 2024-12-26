from typing import Any
import json
import random
import re

def is_empty(value) -> bool:
    return (
        value is None or
        (isinstance(value, list) and len(value) == 0) or
        (isinstance(value, dict) and len(value.keys()) == 0) or
        (isinstance(value, str) and len(value.strip()) == 0) or
        (isinstance(value, (int, float)) and value < 1)
    )

def is_numeric(value) -> bool:
    return isinstance(value, (int, float))

def is_json(value):
    try:
        result = json.dumps(value) if not isinstance(value, str) else value
        parsed = json.loads(result)

        if isinstance(parsed, dict) and not is_empty(parsed):
            return parsed

        raise ValueError("Not JSON data")
    except Exception:
        return False

def is_domain_address(value: str) -> bool:
    # regex for validating ip address
    ip_regex = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
               r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
               r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
               r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

    return not (re.match(ip_regex, value) or 'localhost' in value)

def random_string(size: int = 32, numeric: bool = False, specialchar: bool = False) -> str:
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    if numeric:
        characters += '1234567890'

    if specialchar:
        characters += '!@#$&'

    return ''.join(random.choice(characters) for _ in range(size))

def mask_sensitive_data(data: dict) -> dict:
    sensitive_keys = ['secret', 'password']

    for key in data:
        if key.lower() in sensitive_keys and isinstance(data[key], str):
            data[key] = '*' * len(data[key])  # Replace with asterisks

    return data

def excel_column_name(value: int) -> str:
    column_name = ''

    while value > 0:
        value -= 1
        column_name = chr((value % 26) + 65) + column_name
        value //= 26

    return column_name

def escape(value) -> str:
    return f"'{value}'" if isinstance(value, str) else str(value)

def format_snakecase(value: str) -> str:
    # cleans the header string by replacing unwanted characters and formatting
    return re.sub(r'[^0-9a-z ]', '', value.lower()).replace('  ', ' ').replace(' ', '_')