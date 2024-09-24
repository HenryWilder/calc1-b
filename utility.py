def is_number(ch: str):
    return ch in "0123456789"

def is_lower(ch: str):
    return ch in "abcdefghijklmnopqrstuvwxyz"

def is_upper(ch: str):
    return ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def is_letter(ch: str):
    return is_lower(ch) or is_upper(ch)
