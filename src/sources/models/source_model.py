from datetime import datetime

from config import id_delimiter 


class Source:
    __instances = 0

    def __new__(cls, *args, **kwargs):
        cls.__instances += 1

        instance = super().__new__(cls)
        instance.instance_id = cls.__instances
        return instance
    

    def __init__(self, fields: dict) -> None:
        self.__id_suffix = f'{id_delimiter}{self.instance_id}'
        self.__id = None
        self.__name = None
        self.__init_balance = None
        self.__current_balance = None
        self.__current_transaction = None
        self.__transactions = {}
        self.__change_log = []

        self.id = fields['name']
        self.name = fields['name']
        self.init_balance = fields['init_balance']
        self.current_balance = fields['init_balance']
        
        change_log = f'{self.__class__.__name__} {self.__id} was created.'
        self.__update_change_log(change_log)

    
    @property
    def id(self):
        return self.__id
    

    @id.setter
    def id(self, name):
        self.__id = name + self.__id_suffix


    @property
    def name(self):
        return self.__name
    

    @name.setter
    def name(self, new_name):
        self.__name = new_name
    

    @property
    def init_balance(self):
        return self.__init_balance
    

    @init_balance.setter
    def init_balance(self, new_balance):
        self.__init_balance = new_balance
    

    @property
    def current_balance(self):
        return self.__current_balance
    

    @current_balance.setter
    def current_balance(self, new_balance):
        self.__current_balance = new_balance


    @property
    def current_transaction(self):
        return self.__current_transaction
    

    @current_transaction.setter
    def current_transaction(self, new_transaction):
        self.__current_transaction = new_transaction


    def delete(self) -> str:
        change_log = (f'Source {self.__id}: {self.name} was deleted.\n')
        
        self.__id = None
        self.name = None
        self.init_balance = None
        self.current_balance = None
        self.current_transaction = None
        self.__transactions = None

        self.__update_change_log(change_log)
        return change_log


    def view_change_log(self):
        return ('\n\n').join(self.__change_log)


    def update(self, params):
        ch_name_log = self.__update_name(params['name'])
        ch_balance_log = self.__update_init_balance(params['init_balance'])

        return (ch_name_log + ch_balance_log)


    def __update_name(self, name: str) -> str:
        change_log = f'Source name changed from {self.name} to {name}.\n'
        self.id = name
        self.name = name
        self.__update_change_log(change_log)

        return change_log


    def __update_init_balance(self, new_balance: float) -> str:
        difference = new_balance - self.init_balance 
        self.init_balance = new_balance
        self.current_balance += difference

        change_log = (f'New init balance: {self.init_balance}\n' +
                      f'Current balance: {self.current_balance}\n' +
                      f'Difference: {difference}.\n\n')
        self.__update_change_log(change_log)

        return change_log
 

    def __update_change_log(self, change_log):
        log_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.__change_log.append(log_date + '\n' + change_log)

    
    def __repr__(self) -> str:
        return (f'Source id: {self.__id} \n' + 
                f'Source name: {self.name}\n' + 
                f'Source init balance: {self.init_balance}\n' + 
                f'Source current balance: {self.current_balance}')
    
    
    def __str__(self) -> str:
        return self.__repr__()
