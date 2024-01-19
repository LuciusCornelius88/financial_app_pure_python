from enum import Enum, unique

from sources_interface import SourcesInterface
from config import stop_function_code, error_code


def interface_loop(interface):
    while True:
        commands = interface.show_commands()
        print(commands)

        try:
            input_command = int(input('Enter command id: '))
        except ValueError:
            print(f'{ValueError.__name__}: id should be numeric. Try again!')
            continue
        except KeyboardInterrupt:
            input_command = MainInterfaceCommands.STOP.id

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
class MainInterfaceCommands(Enum):
    SOURCES = {'id': 1, 'val': 'Operations with Sources'}
    CATEGORIES = {'id': 2, 'val': 'Operations with Categories'}
    TRANSACTIONS = {'id': 3, 'val': 'Operations with Transactions'}
    REPORT = {'id': 4, 'val': 'Operations with report'}
    STOP = {'id': -1, 'val': 'Stop the programm'}

    def __init__(self, vals):
        self.id = vals['id']
        self.val = vals['val']



class MainInterface:
    def __init__(self) -> None:
        self.commands = MainInterfaceCommands
        self.sources_interface = SourcesInterface()


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
            self.commands.REPORT.id: self.trigger_transactions,
            self.commands.STOP.id: self.trigger_stop,
        }

        try:
            command = commands[command_id]
            return command
        except KeyError:
            print(f'{KeyError.__name__}: there is no such id. Try again.\n')
            return error_code
    

    def trigger_stop(self):
        print('Good bye!\n')
        return stop_function_code


    def trigger_sources(self):
        interface_loop(self.sources_interface)


    def trigger_categories(self):
        return 'Categories'


    def trigger_transactions(self):
        return 'Transsactions'
    

    def trigger_transactions(self):
        return 'Report'
    