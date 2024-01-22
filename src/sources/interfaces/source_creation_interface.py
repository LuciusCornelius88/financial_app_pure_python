from config import error_code, stop_function_code, exit_code, interruption_message, value_error_message
from decorators import errors_handler


class SourceCreationInterface:
    def __init__(self, default_name=None, default_balance=None) -> None:
        self.__exit_code = exit_code
        self.__default_input = ""
        self.__default_name = default_name if default_name else 'Source'
        self.__default_balance = default_balance if default_balance else 0
        self.__create_name_promt = (f'Enter name of the source or enter {self.__default_input} to set to default ' +
                                    f'or enter {self.__exit_code} to exit the input: \n')
        self.__create_balance_promt = (f'Enter initial balance or enter {self.__default_input} to set to default ' +
                                       f'or enter {self.__exit_code} to exit the input: \n')


    def create(self):
        name = self.__create_name()
        if name == stop_function_code:
            return error_code
        
        while True:
            balance = self.__create_initial_balance()
            if balance == stop_function_code:
                return error_code
            elif balance == error_code:
                continue
            else:
                return {'name': name, 'init_balance': balance}
    

    @errors_handler
    def __create_name(self):
        name = input(self.__create_name_promt)
        if name == self.__default_input:
            return self.__default_name
        elif name == self.__exit_code:
            print(interruption_message)
            return stop_function_code
        else:
            return name


    @errors_handler
    def __create_initial_balance(self):
        balance = input(self.__create_balance_promt)
        if balance == self.__default_input:
            return self.__default_balance
        if balance == self.__exit_code:
            print(interruption_message)
            return stop_function_code
        else:
            return float(balance)