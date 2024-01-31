import sys
from enum import Enum, unique
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'interfaces'))
sys.path.append(str(Path(__file__).parent / 'models'))
sys.path.append(str(Path(__file__).parent.parent))

from category_creation_interface import CategoryCreationInterface
from category_get_delete_interface import CategoryGetterInterface, CategoryDeletionInterface
from category_update_interface import CategoryUpdateInterface
from category_model import Category
from config import error_code, stop_function_code, key_error_message, \
    loop_exit_message, create_obj_message, create_instance_message


@unique
class CategoriesInterfaceCommand(Enum):
    CREATE = {'id': 1, 'val': 'Create new Category'}
    MASS_INSERT = {'id': 2, 'val': 'Insert new categories into database'}
    GET = {'id': 3, 'val': 'View category'}
    GET_ALL = {'id': 4, 'val': 'View all categories'}
    UPDATE = {'id': 5, 'val': 'Update category'}
    DELETE = {'id': 6, 'val': 'Delete category'}
    GET_TRANSACTIONS = {'id': 7, 'val': 'View related transactions'}
    GET_CHANGE_LOG = {'id': 8, 'val': 'View change log'}
    STOP = {'id': -1, 'val': 'Stop the programm'}
    

    def __init__(self, vals) -> None:
        self.id = vals['id']
        self.val = vals['val']



class CategoriesInterface:
    def __init__(self, categories_storage) -> None:
        self.categories_storage = categories_storage
        self.commands = CategoriesInterfaceCommand
        self.category_creation_interface = CategoryCreationInterface()
        self.category_getter_interface = CategoryGetterInterface(categories_storage)
        self.category_deletion_interface = CategoryDeletionInterface(categories_storage)
        self.category_update_interface = CategoryUpdateInterface(categories_storage)
        self.new_categories_cache = []


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
            self.commands.GET_TRANSACTIONS.id: self.trigger_get_transactions,
            self.commands.GET_CHANGE_LOG.id: self.trigger_get_change_log,
            self.commands.STOP.id: self.trigger_stop,
        }

        try:
            command = commands[command_id]
            return command
        except KeyError:
            print(f'{KeyError.__name__}{key_error_message}')
            return error_code


    def trigger_stop(self):
        self.categories_storage.save_to_file()
        print(f'{loop_exit_message} {self.__class__.__name__}.\n')
        return stop_function_code


    def trigger_create(self):
        source_data = self.category_creation_interface.create()
        if source_data == error_code:
            return error_code
        self.new_categories_cache.append(source_data)
        log_message = f'{create_obj_message}{source_data}'
        return log_message


    def trigger_mass_insert(self):
        for source_data in self.new_categories_cache:
            source_instance = Category(source_data)
            self.categories_storage.add(source_instance)
        log_message = (f'{create_instance_message}' +
                       '; '.join(f'{source.get("name")}: {source.get("init_balance")}' for source in self.new_categories_cache))
        self.new_categories_cache.clear()
        return log_message


    def trigger_get(self):
        return self.category_getter_interface.get()


    def trigger_get_all(self):
        return self.categories_storage.show_all()


    def trigger_update(self):
        return self.category_update_interface.update()


    def trigger_delete(self):
        return self.category_deletion_interface.delete()


    def trigger_get_transactions(self):
        instance = self.category_getter_interface.get()
        return instance.view_transactions()

    def trigger_get_change_log(self):
        instance = self.category_getter_interface.get()
        return instance.view_change_log()