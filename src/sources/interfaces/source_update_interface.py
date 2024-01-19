from source_creation_interface import SourceCreationInterface
from source_getter_interface import SourceGetterInterface
from config import error_code


class SourceUpdateInterface:
    def __init__(self, sources_storage) -> None:
        self.__getter_interface = SourceGetterInterface(sources_storage)
        self.__creation_interface = SourceCreationInterface


    def update(self):
        instance = self.__get_instance()
        if instance == error_code:
            return error_code
        creation_interface = self.__creation_interface(default_name=instance.name, default_balance=instance.init_balance)
        print(str(instance) + '\n')
        new_params = creation_interface.create()
        if new_params == error_code:
            return error_code
        return instance.update(new_params)


    def __get_instance(self):
        return self.__getter_interface.get()