import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from transaction_creation_interface import TransactionCreationInterface
from transaction_get_delete_interface import TransactionGetterInterface
from config import error_code


class TransactionUpdateInterface:
    def __init__(self, transaction_storage, sources_storage, categories_storage) -> None:
        self.sources_storage = sources_storage
        self.categories_storage = categories_storage
        self.getter_interface = TransactionGetterInterface(transaction_storage)
        self.creation_interface = TransactionCreationInterface


    def update(self):
        instance = self._get_instance()
        if instance == error_code:
            return error_code

        creation_interface = self.creation_interface(sources_storage=self.sources_storage, 
                                                     categories_storage=self.categories_storage, 
                                                     default_transaction=instance)
        print(str(instance) + '\n')

        new_params = creation_interface.create()
        if new_params == error_code:
            return error_code
        return instance.update(new_params)

    
    def _get_instance(self):
            return self.getter_interface.get()