class SourceCreationInterface:
    def __init__(self) -> None:
        self.default_name = 'Source'
        self.default_balance = 0
        self.create_name_promt = 'Enter name of the source: '
        self.create_balance_promt = 'Enter initial balance: '


    def create(self):
        instance_data = {
            'name': self.__create_name(),
            'init_balance': self.__create_initial_balance()            
        }

        return instance_data
    
    def __create_name(self):
        name = input(self.create_name_promt)
        return name if name else self.default_name


    def __create_initial_balance(self):
        initial_balance = input(self.create_balance_promt)
        try:
            return float(initial_balance)
        except ValueError:
            return self.default_balance