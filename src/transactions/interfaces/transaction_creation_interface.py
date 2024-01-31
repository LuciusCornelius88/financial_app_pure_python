import sys
from pathlib import Path
from datetime import datetime
from enum import Enum, unique

sys.path.append(str(Path(__file__).parent.parent.parent))

from config import error_code, stop_function_code, exit_code, interruption_message, \
    default_input, id_delimiter, date_format
from decorators import errors_handler, while_loop


@unique
class TransactionType(Enum):
    INCOME = {'id': 1, 'val': 'income'}
    OUTCOME = {'id': 2, 'val': 'outcome'}

    def __init__(self, vals) -> None:
        self.id = vals['id']
        self.val = vals['val']

    @classmethod
    def get_values(cls) -> dict:
        dic = {}
        for item in cls:
            dic[item.id] = item.val
        return dic
    

@unique
class TargetType(Enum):
    SOURCE = {'id': 1, 'val': 'source'}
    CATEGORY = {'id': 2, 'val': 'category'}

    def __init__(self, vals) -> None:
        self.id = vals['id']
        self.val = vals['val']

    @classmethod
    def get_values(cls) -> dict:
        dic = {}
        for item in cls:
            dic[item.id] = item.val
        return dic



class TransactionCreationInterface:

    def __init__(self, sources_storage, categories_storage, default_transaction=None) -> None:
        self.exit_code = exit_code
        self.default_input = default_input

        self.sources_storage = sources_storage
        self.categories_storage = categories_storage

        self.transaction_types = TransactionType
        self.target_types = TargetType

        self.default_transaction = default_transaction
        self.default_date = default_transaction.date if default_transaction else datetime.now().date().strftime(date_format)
        self.default_description = default_transaction.description if default_transaction else 'Transaction'
        self.default_amount = default_transaction.source_amount if default_transaction else 0
        
        self.create_date_prompt = (f'Enter date of the transaction in a format "dd-mm-yyyy" or enter {self.default_input} to set to default '
                                   f'or enter {self.exit_code} to exit the input: \n')
        self.create_description_prompt = (f'Enter description of the transaction or enter {self.default_input} to set to default '
                                          f'or enter {self.exit_code} to exit the input: \n')
        self.create_amount_prompt = (f'Enter transaction amount or enter {self.default_input} to set to default '
                                     f'or enter {self.exit_code} to exit the input: \n')
        self.create_transaction_type_prompt = (f'Enter type of transaction or enter {self.exit_code} to exit the input.\n')
        self.create_target_type_prompt = (f'Enter type of target or enter {self.exit_code} to exit the input.\n')


    def create(self):
        date = self._create_date()
        if date == stop_function_code:
            return error_code
        
        description = self._create_description()
        if description == stop_function_code:
            return error_code
        
        transaction_type = self._create_transaction_type()
        if transaction_type == stop_function_code:
            return error_code
        
        source_amount = self._create_amount()
        if source_amount == stop_function_code:
            return error_code
        source_amount = source_amount if transaction_type == self.transaction_types.INCOME.val else (source_amount * -1)
        
        target_type = self._get_target_type(transaction_type)
        source_amount = source_amount if target_type == self.target_types.CATEGORY.val else (source_amount * -1)
        target_amount = source_amount if target_type == self.target_types.CATEGORY.val else (source_amount * -1)

        source = self._get_source(amount=source_amount)
        if source == error_code:
            return error_code
        
        target = (self._get_category(amount=target_amount) 
                  if target_type == self.target_types.CATEGORY.val 
                  else self._get_source())
        if target == error_code:
            return error_code
        
        return {'date': date, 
                'description': description, 
                'source': source, 
                'target': target, 
                'type': transaction_type, 
                'source_amount': source_amount, 
                'target_amount': target_amount}


    @while_loop
    @errors_handler
    def _create_date(self):
        date = input(self.create_date_prompt)
        if date == self.default_input:
            return self.default_date
        elif date == self.exit_code:
            print(interruption_message)
            return stop_function_code
        else:
            return datetime.strptime(date, date_format).date()


    @errors_handler
    def _create_description(self):
        description = input(self.create_description_prompt)
        if description == self.default_input:
            return self.default_description
        elif description == self.exit_code:
            print(interruption_message)
            return stop_function_code
        else:
            return description


    @while_loop
    @errors_handler
    def _create_amount(self):
        amount = input(self.create_amount_prompt)
        if amount == self.default_input:
            return self.default_amount
        elif amount == self.exit_code:
            print(interruption_message)
            return stop_function_code
        else:
            return float(amount)
        

    @while_loop
    @errors_handler
    def _create_transaction_type(self):
        type_id = input(f'{self.create_transaction_type_prompt}{self._show_transactions_types()}')
        if type_id == self.exit_code:
            print(interruption_message)
            return stop_function_code
        return self.transaction_types.get_values()[int(type_id)]
    

    def _show_transactions_types(self):
        types = f''
        for type in self.transaction_types:
            types += f'Enter {type.id} to trigger {type.val}\n'

        return types


    def _get_source(self, amount=None):
        source = InstanceGetter(amount=amount,
                                storage=self.sources_storage,
                                default_transaction=self.default_transaction, 
                                instance_name=self.target_types.SOURCE.val).get_instance()
        if source == error_code:
            return error_code
        return source


    def _get_target_type(self, transaction_type):
        if transaction_type == self.transaction_types.INCOME.val:
            return self.target_types.SOURCE.val
        elif transaction_type == self.transaction_types.OUTCOME.val:
            return self.target_types.CATEGORY.val


    def _get_category(self, amount):
        category = InstanceGetter(amount=amount,
                                  storage=self.categories_storage,
                                  default_transaction=self.default_transaction, 
                                  instance_name=self.target_types.CATEGORY.val).get_instance()
        if category == error_code:
            return error_code
        return category



class InstanceGetter:
    def __init__(self, amount, storage, default_transaction, instance_name) -> None:
        self.storage = storage
        self.amount = amount
        self.default_transaction = default_transaction
        self.exit_code = exit_code
        self.input_prompt = f'Enter {instance_name} ID among given or enter {self.exit_code} to exit the input:\n'
        self.no_available_keys_message = f'No {instance_name} with balance more or equal to {amount}\n'


    def get_instance(self):
        available_keys = self._get_available_keys()
        if available_keys == self.no_available_keys_message:
            print(self.no_available_keys_message)
            return error_code
        
        view_message = self._create_view_message()

        instance_id = self._get_instance_id(available_keys, view_message)
        if instance_id == stop_function_code:
            return error_code
        return self.storage.get(instance_id)


    def _get_available_keys(self):
        available_keys = {}
        for key in self.storage.data.keys():
            if self.amount:
                instance = self.storage.data[key]
                if self.default_transaction:
                    source = instance is self.default_transaction.source
                    target = instance is self.default_transaction.target
                    current_balance = (instance.fake_revert(self.default_transaction.id, target=target) 
                                       if source or target else instance.current_balance)
                else:
                    current_balance = instance.current_balance
                if self.amount >= 0 or current_balance >= abs(self.amount):
                    available_keys[key.split(id_delimiter)[1]] = key
            else:
                available_keys[key.split(id_delimiter)[1]] = key

        return available_keys if available_keys else self.no_available_keys_message


    def _create_view_message(self):
        message_items = []
        for key, value in self.storage.items():
            if self.amount:
                instance = self.storage.data[key]
                if self.default_transaction:
                    source = instance is self.default_transaction.source
                    target = instance is self.default_transaction.target
                    current_balance = (instance.fake_revert(self.default_transaction.id, target=target) 
                                       if source or target else instance.current_balance)
                else:
                    current_balance = self.storage.data[key].current_balance
                if self.amount >= 0 or current_balance >= abs(self.amount):
                    message_items.append(f'{key.split(id_delimiter)[1]}: {value.id.split(id_delimiter)[0]}')
            else:
                message_items.append(f'{key.split(id_delimiter)[1]}: {value.id.split(id_delimiter)[0]}')

        return '\n'.join(message_items)


    @while_loop
    @errors_handler
    def _get_instance_id(self, keys, message):
        instance_id = input(f'{self.input_prompt}{message}\n')
        if instance_id == self.exit_code:
            print(interruption_message)
            return stop_function_code
        return keys[instance_id]
    


# def main():
#     sys.path.append(str(Path(__file__).parent.parent.parent / 'sources/models'))
#     from sources_storage import Sources

#     sources = Sources().restore_from_file()
#     interface = TransactionCreationInterface(sources)

#     result = interface.create()
#     print(result)


# if __name__ == '__main__':
#     main()