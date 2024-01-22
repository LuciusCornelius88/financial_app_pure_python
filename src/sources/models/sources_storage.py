import pickle
from collections import UserDict
from pathlib import Path
from datetime import datetime

from config import dumps_path, sources_dump_file
from decorators import errors_handler


class Sources(UserDict):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    

    def __init__(self):
        super().__init__()
        self.__dump_path = Path(dumps_path + sources_dump_file)
        self.__empty_storage_return = 'No sources in the storage'
        self.__change_log = []

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


    @errors_handler
    def get(self, instance_id):
        instance = self.data[instance_id]
        change_log = f'{instance.__class__.__name__} "{instance.id}: {instance.name}" got from the {self.__class__.__name__} storage.'
        self.__update_change_log(change_log)
        return instance
        

    @errors_handler
    def delete(self, instance_id):
        instance = self.data.pop(instance_id)
        change_log = f'{instance.__class__.__name__} "{instance.id}: {instance.name}" deleted from the {self.__class__.__name__} storage.'
        instance.delete()
        self.__update_change_log(change_log)
        return change_log


    def show_all(self) -> str:
        return str(self) if self.data else self.__empty_storage_return
    

    def save_to_file(self):
        with open(self.__dump_path, 'wb') as file:
            pickle.dump(self, file)

        change_log = f'{self.__class__.__name__} storage saved to {self.__dump_path}.\n'
        self.__update_change_log(change_log)
        return change_log


    def restore_from_file(self):
        with open(self.__dump_path, 'r+b') as file:
            change_log = f'{self.__class__.__name__} restored from {self.__dump_path}.\n'
            self.__update_change_log(change_log)
            return pickle.load(file)
        

    def view_change_log(self):
        return ('\n\n').join(self.__change_log)


    def __update_change_log(self, change_log):
        log_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.__change_log.append(log_date + '\n' + change_log)


    def __repr__(self) -> str:
        return_string = f''
        for item in self.data.values():
            return_string += (str(item) + '\n\n')
        return return_string
    

    def __str__(self):
        return self.__repr__()
