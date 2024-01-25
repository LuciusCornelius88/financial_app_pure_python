import sys
import pickle
from pathlib import Path
from collections import UserDict
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent.parent))

from config import dumps_path, transactions_dump_file
from decorators import errors_handler


class Transactions(UserDict):
    __instance  = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    

    def __init__(self) -> None:
        super().__init__()
        self._dump_path = Path(dumps_path + transactions_dump_file)
        self._empty_storage_return = 'No transactions in the storage'
        self._change_log = []

        change_log = f'{self.__class__.__name__} was created.'
        self._update_change_log(change_log)
    

    def add(self, instance: object):
        if instance.id not in self.data:
            self.data[instance.id] = instance
            change_log = f'{instance.__class__.__name__} "{instance.id}" added to {self.__class__.__name__} storage.'
        else:
            change_log = f'{instance.__class__.__name__} "{instance.id}" is already in {self.__class__.__name__} storage.'

        self._update_change_log(change_log)
        return change_log


    @errors_handler
    def get(self, instance_id):
        instance = self.data[instance_id]
        change_log = f'{instance.__class__.__name__} "{instance.id}" got from the {self.__class__.__name__} storage.'
        self._update_change_log(change_log)
        return instance


    @errors_handler
    def delete(self, instance_id):
        instance = self.data.pop(instance_id)
        change_log = f'{instance.__class__.__name__} "{instance.id}" deleted from the {self.__class__.__name__} storage.'
        instance.delete()
        self._update_change_log(change_log)
        return change_log
    

    def show_all(self) -> str:
        return str(self) if self.data else self._empty_storage_return


    def save_to_file(self):
        with open(self._dump_path, 'wb') as file:
            pickle.dump(self, file)

        change_log = f'{self.__class__.__name__} storage saved to {self._dump_path}.\n'
        self._update_change_log(change_log)
        return change_log


    def restore_from_file(self):
        with open(self._dump_path, 'r+b') as file:
            change_log = f'{self.__class__.__name__} restored from {self._dump_path}.\n'
            self._update_change_log(change_log)
            return pickle.load(file)


    def view_change_log(self):
        return ('\n\n').join(self._change_log)


    def _update_change_log(self, change_log):
        log_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._change_log.append(log_date + '\n' + change_log)


    def __repr__(self) -> str:
        return_string = f''
        for item in self.data.values():
            return_string += (str(item) + '\n\n')
        return return_string


    def __str__(self):
        return self.__repr__()