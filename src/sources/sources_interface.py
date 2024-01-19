from enum import Enum, unique

from source_creation_interface import SourceCreationInterface
from source_deletion_interface import SourceDeletionInterface
from source_getter_interface import SourceGetterInterface
from source_model import Source
from source_update_interface import SourceUpdateInterface
from sources_storage import Sources
from config import error_code, stop_function_code

@unique
class SourcesInterfaceCommands(Enum):
    CREATE = {'id': 1, 'val': 'Create new Source'}
    MASS_INSERT = {'id': 2, 'val': 'Insert new sources into database'}
    GET = {'id': 3, 'val': 'View source'}
    GET_ALL = {'id': 4, 'val': 'View all Sources'}
    UPDATE = {'id': 5, 'val': 'Update Source'}
    DELETE = {'id': 6, 'val': 'Delete Source'}
    STOP = {'id': -1, 'val': 'Stop the programm'}
    

    def __init__(self, vals) -> None:
        self.id = vals['id']
        self.val = vals['val']



class SourcesInterface:
    def __init__(self) -> None:
        try:
            self.__sources_storage = Sources().restore_from_file()
        except (FileNotFoundError, EOFError):
            self.__sources_storage = Sources()

        self.__commands = SourcesInterfaceCommands
        self.__source_creation_interface = SourceCreationInterface()
        self.__source_getter_interface = SourceGetterInterface(self.__sources_storage)
        self.__source_update_interface = SourceUpdateInterface(self.__sources_storage)
        self.__source_deletion_interface = SourceDeletionInterface(self.__sources_storage)
        self.__new_sources_cache = []


    def show_commands(self):
        commands = f''
        for command in self.__commands:
            commands += f'Enter {command.id} to trigger {command.val}\n'

        return commands

    
    def handle_commands(self, command_id):
        commands = {
            self.__commands.CREATE.id: self.trigger_create,
            self.__commands.MASS_INSERT.id: self.trigger_mass_insert,
            self.__commands.GET.id: self.trigger_get,
            self.__commands.GET_ALL.id: self.trigger_get_all,
            self.__commands.UPDATE.id: self.trigger_update,
            self.__commands.DELETE.id: self.trigger_delete,
            self.__commands.STOP.id: self.trigger_stop,
        }

        try:
            command = commands[command_id]
            return command
        except KeyError:
            print(f'{KeyError.__name__}: there is no such id. Try again.\n')
            return error_code
        

    def trigger_stop(self):
        self.__sources_storage.save_to_file()
        print(f'Stop working with {self.__class__.__name__}.\n')
        return stop_function_code
    

    def trigger_create(self):
        source_data = self.__source_creation_interface.create()
        if source_data == error_code:
            return error_code
        self.__new_sources_cache.append(source_data)
        log_message = (f'Created object with data:\n' + 
                       f'{source_data}')
        return log_message
    

    def trigger_mass_insert(self):
        for source_data in self.__new_sources_cache:
            source_instance = Source(source_data)
            self.__sources_storage.add(source_instance)
        log_message = (f'Created instances:\n' + 
                       '; '.join(f'{source["name"]}: {source["init_balance"]}' for source in self.__new_sources_cache))
        self.__new_sources_cache.clear()
        return log_message


    def trigger_get(self):
        return self.__source_getter_interface.get()


    def trigger_get_all(self):
        return self.__sources_storage.show_all()
    

    def trigger_update(self):
        return self.__source_update_interface.update()


    def trigger_delete(self):
        return self.__source_deletion_interface.delete()
