import functools

from config import stop_function_code, error_code, key_error_message, value_error_message, interruption_message


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
        except KeyboardInterrupt:
            print(f'{KeyboardInterrupt.__name__}: {interruption_message}')
            return stop_function_code
    return inner 