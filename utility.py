def is_number(ch: str):
    return ch in "0123456789"

def is_lower(ch: str):
    return ch in "abcdefghijklmnopqrstuvwxyz"

def is_upper(ch: str):
    return ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def is_letter(ch: str):
    return is_lower(ch) or is_upper(ch)

def is_prime(n: int):
    if n <= 0 or n % 2 == 0:
        return False
    for m in range(3, n, 2):
        if n % m == 0:
            return False
    return True
