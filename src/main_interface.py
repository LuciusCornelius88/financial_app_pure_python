import sys
from enum import Enum, unique
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'sources'))
sys.path.append(str(Path(__file__).parent / 'sources/models'))
sys.path.append(str(Path(__file__).parent / 'categories'))
sys.path.append(str(Path(__file__).parent / 'categories/models'))
sys.path.append(str(Path(__file__).parent / 'transactions'))

from sources_storage import Sources
from sources_interface import SourcesInterface
from categories_storage import Categories
from categories_interface import CategoriesInterface
from transactions_interface import TransactionsInterface
from config import stop_function_code, error_code, goodbye_message, key_error_message


def interface_loop(interface):
    while True:
        commands = interface.show_commands()
        print(commands)

        try:
            input_command = int(input('Enter command id: '))
        except ValueError:
            print(f'{ValueError.__name__}: id should be numeric. Try again!')
            continue
        except (KeyboardInterrupt, EOFError):
            input_command = MainInterfaceCommand.STOP.id

        trigger_function = interface.handle_commands(input_command)
        if trigger_function == error_code:
            continue
    
        result = trigger_function()
        if result == stop_function_code:
            break
        elif result == error_code or result == None:
            continue
        else:
            print(result)


@unique
class MainInterfaceCommand(Enum):
    SOURCES = {'id': 1, 'val': 'Operations with Sources'}
    CATEGORIES = {'id': 2, 'val': 'Operations with Categories'}
    TRANSACTIONS = {'id': 3, 'val': 'Operations with Transactions'}
    REPORT = {'id': 4, 'val': 'Operations with report'}
    STOP = {'id': -1, 'val': 'Stop the programm'}

    def __init__(self, vals):
        self.id = vals.get('id')
        self.val = vals.get('val')



class MainInterface:
    def __init__(self) -> None:
        try:
            sources_storage = Sources().restore_from_file()
            categories_storage = Categories().restore_from_file()
        except (FileNotFoundError, EOFError):
            sources_storage = Sources()
            categories_storage = Categories()
            
        self.commands = MainInterfaceCommand
        self.sources_interface = SourcesInterface(sources_storage)
        self.categories_interface = CategoriesInterface(categories_storage)
        self.transactions_interface = TransactionsInterface(sources_storage, categories_storage)


    def show_commands(self):
        commands = f''
        for command in self.commands:
            commands += f'Enter {command.id} to trigger {command.val}\n'

        return commands

    
    def handle_commands(self, command_id):
        commands = {
            self.commands.SOURCES.id: self.trigger_sources,
            self.commands.CATEGORIES.id: self.trigger_categories,
            self.commands.TRANSACTIONS.id: self.trigger_transactions,
            self.commands.REPORT.id: self.trigger_report,
            self.commands.STOP.id: self.trigger_stop,
        }

        try:
            command = commands[command_id]
            return command
        except KeyError:
            print(f'{KeyError.__name__}{key_error_message}')
            return error_code
    

    def trigger_stop(self):
        print(goodbye_message)
        return stop_function_code


    def trigger_sources(self):
        interface_loop(self.sources_interface)


    def trigger_categories(self):
        interface_loop(self.categories_interface)


    def trigger_transactions(self):
        interface_loop(self.transactions_interface)
    

    def trigger_report(self):
        return 'Report'
    