from datetime import datetime

from config import id_delimiter 


class Source:
    __instances = 0

    def __new__(cls, *args, **kwargs):
        cls.__instances += 1

        instance = super().__new__(cls)
        instance.id = cls.__instances
        return instance
    

    def __init__(self, fields: dict) -> None:
        self.id = fields['name'] + f'{id_delimiter}{self.id}'
        self.name = fields['name']
        self.init_balance = fields['init_balance']
        self.current_balance = fields['init_balance']
        self.current_transaction = None
        self.transactions = {}
        self.change_log = []

        change_log = f'{self.__class__.__name__} {self.id} was created.'
        self.__update_change_log(change_log)
    

    def update_name(self, name: str) -> str:
        change_log = f'Source name changed from {self.name} to {name}'
        self.name = name
        self.__update_change_log(change_log)

        return change_log


    def update_init_balance(self, new_balance: float) -> str:
        difference = new_balance - self.init_balance 
        self.init_balance = new_balance
        self.current_balance += difference

        change_log = (f'New init balance: {self.init_balance}\n' +
                      f'Current balance: {self.current_balance}\n' +
                      f'Difference: {difference}')
        self.__update_change_log(change_log)

        return change_log
 

    def delete(self) -> str:
        change_log = (f'Source {self.id}: {self.name} was deleted.\n')
        
        self.id = None
        self.name = None
        self.init_balance = None
        self.current_balance = None
        self.current_transaction = None
        self.transactions = None

        self.__update_change_log(change_log)
        return change_log


    def view_change_log(self):
        return ('\n\n').join(self.change_log)


    def __update_change_log(self, change_log):
        log_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.change_log.append(log_date + '\n' + change_log)

    
    def __repr__(self) -> str:
        return (f'Source id: {self.id} \n' + 
                f'Source name: {self.name}\n' + 
                f'Source init balance: {self.init_balance}\n' + 
                f'Source current balance: {self.current_balance}')
    
    
    def __str__(self) -> str:
        return self.__repr__()

    

# def main():
#     source_data_1 = {
#         'name': 'source_1',
#         'init_balance': 1000
#     }

#     source_data_2 = {
#         'name': 'source_2',
#         'init_balance': 10000
#     }

    # source_1 = Source(source_data_1)
    # source_2 = Source(source_data_2).restore_from_file()
    # print(source_2._Source__instances)
    # source_3 = Source(source_data_1)

    # source_1.update_name('New name')
    # source_1.update_init_balance(100000)
    # source_1.save_to_file()
    # print(source_2)
    # print(source_3)
    # print(source_2.view_change_log())


# if __name__ == '__main__':
#     main()