from typing import Callable
from colorama import Fore, Back, Style
import inspect

def _debug_value(value):
    if isinstance(value, str):
        return Fore.LIGHTMAGENTA_EX + (f"'{value}'" if len(value) == 1 else f'"{value}"') + Fore.RESET
    elif isinstance(value, list):
        return Fore.YELLOW + '[' + ', '.join([_debug_value(item) for item in value]) + Fore.YELLOW + ']' + Fore.RESET
    elif callable(value):
        return Fore.LIGHTYELLOW_EX + '`' + '  '.join([line.strip() for line in inspect.getsourcelines(value)[0]]) + '`' + Fore.RESET
    else:
        return Fore.LIGHTCYAN_EX + str(value) + Fore.RESET

_debug_stack_depth = 0

def debug_stack_push():
    global _debug_stack_depth
    _debug_stack_depth += 1

def debug_stack_pop():
    global _debug_stack_depth
    _debug_stack_depth -= 1

def debug(ty: str, func: str, msg: str, *args: object, **kwargs: object):
    global _debug_stack_depth
    fmt_msg =  msg.format(*tuple([_debug_value(arg) for arg in args]), **dict([(key, _debug_value(val)) for (key, val) in kwargs]))
    print(('  ' * _debug_stack_depth) + Style.DIM + Fore.GREEN + ty + Fore.RESET + '.' + Fore.LIGHTYELLOW_EX + func + Fore.RESET + ": " + Style.RESET_ALL + fmt_msg)

def debug_surround(ret: Callable[[], object]) -> object:
    debug_stack_push()
    result = ret()
    debug_stack_pop()
    return result
