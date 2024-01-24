import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent.parent))

from config import error_code, stop_function_code, exit_code, interruption_message, \
    default_input, id_delimiter, date_format
from decorators import errors_handler, while_loop


class TransactionCreationInterface:

    def __init__(self, sources_storage, default_description=None, default_amount=None) -> None:
        self.exit_code = exit_code
        self.default_input = default_input
        self.sources_storage = sources_storage
        self.default_date = datetime.now().date().strftime(date_format)
        self.default_description = default_description if default_description else 'Transaction'
        self.default_amount = default_amount if default_amount else 0
        self.create_date_prompt = (f'Enter date of the transaction in a format "dd-mm-yyyy" or enter {self.default_input} to set to default '
                                   f'or enter {self.exit_code} to exit the input: \n')
        self.create_description_prompt = (f'Enter description of the transaction or enter {self.default_input} to set to default '
                                          f'or enter {self.exit_code} to exit the input: \n')
        self.create_amount_prompt = (f'Enter transaction amount or enter {self.default_input} to set to default '
                                     f'or enter {self.exit_code} to exit the input: \n')


    def create(self):
        date = self._create_date()
        if date == stop_function_code:
            return error_code
        
        description = self._create_description()
        if description == stop_function_code:
            return error_code
        
        amount = self._create_amount()
        if amount == stop_function_code:
            return error_code
        
        source = self._get_source(amount)
        if source == error_code:
            return error_code
        
        category = self._get_category(amount)
        if category == error_code:
            return error_code
        
        return {'date': date, 'description': description, 'source': source, 'category': category, 'amount': amount}


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


    def _get_source(self, amount):
        source = InstanceGetter(self.sources_storage, amount, 'source').get_instance()
        if source == error_code:
            return error_code
        return source


    def _get_category(self, amount):
        return 'Category'
        # category = InstanceGetter(self.categories_storage, 'category').get_instance()
        # if category == error_code:
        #     return error_code
        # return category



class InstanceGetter:
    def __init__(self, storage, amount, instance_name) -> None:
        self.storage = storage
        self.amount = amount
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
        available_keys = {key.split(id_delimiter)[1]: key for key in self.storage.data.keys()
                          if self.storage.data[key].current_balance >= self.amount}
        return available_keys if available_keys else self.no_available_keys_message


    def _create_view_message(self):
        return '\n'.join(f'{key.split(id_delimiter)[1]}: {value.id.split(id_delimiter)[0]}' for key, value in self.storage.items() 
                         if self.storage.data[key].current_balance >= self.amount)


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