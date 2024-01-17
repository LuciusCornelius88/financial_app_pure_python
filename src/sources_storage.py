import pickle
from collections import UserDict
from pathlib import Path
from datetime import datetime

# from source_model import Source
from config import dumps_path, sources_dump_file


class Sources(UserDict):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    

    def __init__(self):
        super().__init__()
        self.dump_path = Path(dumps_path + sources_dump_file)
        self.empty_storage_return = 'No sources in the storage'
        self.change_log = []

        change_log = f'{self.__class__.__name__} was created.'
        self.__update_change_log(change_log)
    

    def add(self, instance: object):
        if not instance.id in self.data:
            self.data[instance.id] = instance
            change_log = f'{instance.__class__.__name__} "{instance.id}: {instance.name}" added to {self.__class__.__name__} storage.'
        else:
            change_log = f'{instance.__class__.__name__} "{instance.id}: {instance.name}" is already in {self.__class__.__name__} storage.'

        self.__update_change_log(change_log)
        return change_log


    def get(self, instance_id):
        try:
            instance = self.data[instance_id]
            change_log = f'{instance.__class__.__name__} "{instance.id}: {instance.name}" got from the {self.__class__.__name__} storage.'
            self.__update_change_log(change_log)
            return instance
        except KeyError:
            change_log = f'There is no instance with name "{instance_id}" in {self.__class__.__name__} storage.'
            self.__update_change_log(change_log)
            return change_log
        

    def delete(self, instance_id):
        try:
            instance = self.data.pop(instance_id)
            change_log = f'{instance.__class__.__name__} "{instance.id}: {instance.name}" deleted from the {self.__class__.__name__} storage.'
            instance.delete()
            self.__update_change_log(change_log)
            return change_log
        except KeyError:
            change_log = f'There is no instance with name "{instance_id}" in {self.__class__.__name__} storage.'
            self.__update_change_log(change_log)
            return change_log


    def show_all(self) -> str:
        return str(self) if self.data else self.empty_storage_return
    

    def save_to_file(self):
        with open(self.dump_path, 'wb') as file:
            pickle.dump(self, file)

        change_log = f'{self.__class__.__name__} storage saved to {self.dump_path}.\n'
        self.__update_change_log(change_log)
        return change_log


    def restore_from_file(self):
        with open(self.dump_path, 'r+b') as file:
            change_log = f'{self.__class__.__name__} restored from {self.dump_path}.\n'
            self.__update_change_log(change_log)
            return pickle.load(file)
        

    def view_change_log(self):
        return ('\n\n').join(self.change_log)


    def __update_change_log(self, change_log):
        log_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.change_log.append(log_date + '\n' + change_log)


    def __repr__(self) -> str:
        return_string = f''
        for item in self.data.values():
            return_string += (str(item) + '\n\n')
        return return_string
    

    def __str__(self):
        return self.__repr__()



# def main():
#     source_data_1 = {
#         'name': 'source_1',
#         'init_balance': 1000
#     }

#     source_data_2 = {
#         'name': 'source_2',
#         'init_balance': 1000
#     }

#     source_data_3 = {
#         'name': 'source_3',
#         'init_balance': 1000
#     }

#     instance = Sources()

#     source_1 = Source(source_data_1)
#     source_2 = Source(source_data_2)
#     source_3 = Source(source_data_3)

#     instance.add(source_1)
#     instance.add(source_2)
#     instance.add(source_3)

#     target_source = instance.get(source_1.id)
#     print(target_source)
#     target_source.update_name('New name')
#     target_source.update_init_balance(100000)
#     print(target_source.view_change_log())
#     print(target_source)


# if __name__ == '__main__':
#     main()