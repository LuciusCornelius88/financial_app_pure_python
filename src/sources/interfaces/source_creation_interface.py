from config import error_code, stop_function_code, exit_code, interruption_message


class SourceCreationInterface:
    def __init__(self, default_name=None, default_balance=None) -> None:
        self.__exit_code = exit_code
        self.__default_input = ""
        self.__default_name = default_name if default_name else 'Source'
        self.__default_balance = default_balance if default_balance else 0
        self.__create_name_promt = (f'Enter name of the source or enter {self.__default_input} to set to default ' +
                                    f'or enter {self.__exit_code} to exit the input: ')
        self.__create_balance_promt = (f'Enter initial balance or enter {self.__default_input} to set to default ' +
                                       f'or enter {self.__exit_code} to exit the input: ')


    def create(self):
        name = self.__create_name()
        if name == stop_function_code:
            return error_code
        
        balance = self.__create_initial_balance()
        if balance == stop_function_code:
            return error_code
        
        return {'name': name, 'init_balance': balance}
    

    def __create_name(self):
        try:
            name = input(self.__create_name_promt)
            if name == self.__default_input:
                return self.__default_name
            elif name == self.__exit_code:
                print(interruption_message)
                return stop_function_code
            else:
                return name
        except KeyboardInterrupt:
            print(f'{KeyboardInterrupt.__name__}: {interruption_message}')
            return stop_function_code


    def __create_initial_balance(self):
        while True:
            try:
                balance = input(self.__create_balance_promt)
                if balance == self.__exit_code:
                    print(interruption_message)
                    return stop_function_code
                return float(balance)
            except ValueError:
                if balance == self.__default_input:
                    return self.__default_balance
                else:
                    print(f'{ValueError.__name__}: balance should be numeric. Try again!')
                    continue
            except KeyboardInterrupt:
                print(f'{KeyboardInterrupt.__name__}: {interruption_message}')
                return stop_function_code