from config import error_code, stop_function_code, exit_code, interruption_message
from decorators import errors_handler


class SourceCreationInterface:
    def __init__(self, default_name=None, default_balance=None) -> None:
        self.exit_code = exit_code
        self.default_input = ""
        self.default_name = default_name if default_name else 'Source'
        self.default_balance = default_balance if default_balance else 0
        self.create_name_prompt = (f'Enter name of the source or enter {self.default_input} to set to default '
                                   f'or enter {self.exit_code} to exit the input: \n')
        self.create_balance_prompt = (f'Enter initial balance or enter {self.default_input} to set to default '
                                      f'or enter {self.exit_code} to exit the input: \n')


    def create(self):
        name = self._create_name()
        if name == stop_function_code:
            return error_code

        while True:
            balance = self._create_initial_balance()
            if balance == stop_function_code:
                return error_code
            elif balance == error_code:
                continue
            else:
                return {'name': name, 'init_balance': balance}


    @errors_handler
    def _create_name(self):
        name = input(self.create_name_prompt)
        if name == self.default_input:
            return self.default_name
        elif name == self.exit_code:
            print(interruption_message)
            return stop_function_code
        else:
            return name


    @errors_handler
    def _create_initial_balance(self):
        balance = input(self.create_balance_prompt)
        if balance == self.default_input:
            return self.default_balance
        if balance == self.exit_code:
            print(interruption_message)
            return stop_function_code
        else:
            return float(balance)
