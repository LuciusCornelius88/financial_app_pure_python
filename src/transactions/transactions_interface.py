import sys
from enum import Enum, unique
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'interfaces'))
sys.path.append(str(Path(__file__).parent / 'models'))
sys.path.append(str(Path(__file__).parent.parent))

from transaction_creation_interface import TransactionCreationInterface
from transaction_get_delete_interface import TransactionGetterInterface, TransactionDeletionInterface
from transaction_update_interface import TransactionUpdateInterface
from transaction_model import Transaction
from transactions_storage import Transactions
from config import error_code, stop_function_code, key_error_message, \
    loop_exit_message, create_obj_message, create_instance_message


@unique
class TransactionsInterfaceCommand(Enum):
    CREATE = {'id': 1, 'val': 'Create new Transaction'}
    GET = {'id': 3, 'val': 'View transaction'}
    GET_ALL = {'id': 4, 'val': 'View all Transactions'}
    UPDATE = {'id': 5, 'val': 'Update Transaction'}
    DELETE = {'id': 6, 'val': 'Delete Transaction'}
    STOP = {'id': -1, 'val': 'Stop the programm'}
    

    def __init__(self, vals) -> None:
        self.id = vals['id']
        self.val = vals['val']


class TransactionsInterface:
    def __init__(self, sources_storage) -> None:
        try:
            self.transactions_storage = Transactions().restore_from_file()
        except (FileNotFoundError, EOFError):
            self.transactions_storage = Transactions()

        self.commands = TransactionsInterfaceCommand
        self.transaction_creation_interface = TransactionCreationInterface(sources_storage)
        self.transaction_getter_interface = TransactionGetterInterface(self.transactions_storage)
        self.transaction_update_interface = TransactionUpdateInterface(transaction_storage=self.transactions_storage, 
                                                                       sources_storage=sources_storage)
        self.transaction_deletion_interface = TransactionDeletionInterface(self.transactions_storage)


    def show_commands(self):
        commands = f''
        for command in self.commands:
            commands += f'Enter {command.id} to trigger {command.val}\n'

        return commands

    
    def handle_commands(self, command_id):
        commands = {
            self.commands.CREATE.id: self.trigger_create,
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
        self.transactions_storage.save_to_file()
        print(f'{loop_exit_message} {self.__class__.__name__}.\n')
        return stop_function_code
    

    def trigger_create(self):
        transaction_data = self.transaction_creation_interface.create()
        if transaction_data == error_code:
            return error_code
        transaction_instance = Transaction(transaction_data)
        self.transactions_storage.add(transaction_instance)
        log_message = f'{create_instance_message}{transaction_instance}'
        return log_message


    def trigger_get(self):
        return self.transaction_getter_interface.get()


    def trigger_get_all(self):
        return self.transactions_storage.show_all()
    

    def trigger_update(self):
        return self.transaction_update_interface.update()


    def trigger_delete(self):
        return self.transaction_deletion_interface.delete()