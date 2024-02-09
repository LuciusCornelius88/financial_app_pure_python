import functools

from config import stop_function_code, error_code, key_error_message, value_error_message, interruption_message
from custom_exceptions import InvalidDeletion


def errors_handler(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            print(f'{KeyError.__name__}{key_error_message}')
            return error_code
        except ValueError:
            print(f'{ValueError.__name__}{value_error_message}')
            return error_code
        except (KeyboardInterrupt, EOFError):
            print(f'{KeyboardInterrupt.__name__}: {interruption_message}')
            return stop_function_code
        except InvalidDeletion as inv_del_ex:
            print(f'{InvalidDeletion.__name__}: {inv_del_ex.message}')
            return error_code
    return inner 


def while_loop(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        while True:
            result = func(*args, **kwargs)
            if result == stop_function_code:
                return stop_function_code
            elif result == error_code:
                continue
            else: 
                return result
    return inner