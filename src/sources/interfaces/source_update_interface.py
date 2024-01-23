from source_creation_interface import SourceCreationInterface
from source_get_delete_interface import SourceGetterInterface
from config import error_code


class SourceUpdateInterface:
    def __init__(self, sources_storage) -> None:
        self.getter_interface = SourceGetterInterface(sources_storage)
        self.creation_interface = SourceCreationInterface


    def update(self):
        instance = self._get_instance()
        if instance == error_code:
            return error_code

        creation_interface = self.creation_interface(default_name=instance.name, default_balance=instance.init_balance)
        print(str(instance) + '\n')

        new_params = creation_interface.create()
        if new_params == error_code:
            return error_code
        return instance.update(new_params)


    def _get_instance(self):
        return self.getter_interface.get()