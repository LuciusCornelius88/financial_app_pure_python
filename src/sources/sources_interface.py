import sys
from enum import Enum, unique
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'interfaces'))
sys.path.append(str(Path(__file__).parent / 'models'))
sys.path.append(str(Path(__file__).parent.parent))

from source_creation_interface import SourceCreationInterface
from source_get_delete_interface import SourceGetterInterface, SourceDeletionInterface
from source_update_interface import SourceUpdateInterface
from source_model import Source
from sources_storage import Sources
from config import error_code, stop_function_code, key_error_message, \
    loop_exit_message, create_obj_message, create_instance_message


@unique
class SourcesInterfaceCommand(Enum):
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
            self.sources_storage = Sources().restore_from_file()
        except (FileNotFoundError, EOFError):
            self.sources_storage = Sources()

        self.commands = SourcesInterfaceCommand
        self.source_creation_interface = SourceCreationInterface()
        self.source_getter_interface = SourceGetterInterface(self.sources_storage)
        self.source_deletion_interface = SourceDeletionInterface(self.sources_storage)
        self.source_update_interface = SourceUpdateInterface(self.sources_storage)
        self.new_sources_cache = []


    def show_commands(self):
        commands = ''
        for command in self.commands:
            commands += f'Enter {command.id} to trigger {command.val}\n'
        return commands


    def handle_commands(self, command_id):
        commands = {
            self.commands.CREATE.id: self.trigger_create,
            self.commands.MASS_INSERT.id: self.trigger_mass_insert,
            self.commands.GET.id: self.trigger_get,
            self.commands.GET_ALL.id: self.trigger_get_all,
            self.commands.UPDATE.id: self.trigger_update,
            self.commands.DELETE.id: self.trigger_delete,
            self.commands.STOP.id: self.trigger_stop,
        }

        try:
            command = commands[command_id]
            return command
        except KeyError:
            print(f'{KeyError.__name__}{key_error_message}')
            return error_code


    def trigger_stop(self):
        self.sources_storage.save_to_file()
        print(f'{loop_exit_message} {self.__class__.__name__}.\n')
        return stop_function_code


    def trigger_create(self):
        source_data = self.source_creation_interface.create()
        if source_data == error_code:
            return error_code
        self.new_sources_cache.append(source_data)
        log_message = f'{create_obj_message}{source_data}'
        return log_message


    def trigger_mass_insert(self):
        for source_data in self.new_sources_cache:
            source_instance = Source(source_data)
            self.sources_storage.add(source_instance)
        log_message = (f'{create_instance_message}' +
                       '; '.join(f'{source.get("name")}: {source.get("init_balance")}' for source in self.new_sources_cache))
        self.new_sources_cache.clear()
        return log_message


    def trigger_get(self):
        return self.source_getter_interface.get()


    def trigger_get_all(self):
        return self.sources_storage.show_all()


    def trigger_update(self):
        return self.source_update_interface.update()


    def trigger_delete(self):
        return self.source_deletion_interface.delete()
