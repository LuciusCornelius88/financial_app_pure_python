import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from config import error_code, stop_function_code, exit_code, interruption_message, \
    id_delimiter
from decorators import errors_handler


class GetterPattern:
    def __init__(self, categories_storage) -> None:
        self.categories_storage = categories_storage
        self.exit_code = exit_code
        self.input_prompt = f'Enter instance ID among given or enter {self.exit_code} to exit the input:\n'
        self.target_method = None

    def target(self):
        available_keys = self._get_available_keys()
        view_message = self._create_view_message()

        while True:
            instance_id = self._get_instance_id(available_keys, view_message)
            if instance_id == error_code:
                continue
            elif instance_id == stop_function_code:
                return error_code
            else:
                return self.target_method(instance_id)

    def _get_available_keys(self):
        return {key.split(id_delimiter)[1]: key for key in self.categories_storage.data.keys()}

    def _create_view_message(self):
        return '\n'.join(f'{key.split(id_delimiter)[1]}: {value.id.split(id_delimiter)[0]}' for key, value in self.categories_storage.items())

    @errors_handler
    def _get_instance_id(self, keys, message):
        instance_id = input(f'{self.input_prompt}{message}\n')
        if instance_id == self.exit_code:
            print(interruption_message)
            return stop_function_code
        return keys[instance_id]


class CategoryGetterInterface(GetterPattern):
    def __init__(self, categories_storage) -> None:
        super().__init__(categories_storage)
        self.target_method = self.categories_storage.get

    def get(self):
        """Get method for category."""
        return self.target()


class CategoryDeletionInterface(GetterPattern):
    def __init__(self, categories_storage) -> None:
        super().__init__(categories_storage)
        self.target_method = self.categories_storage.delete

    def delete(self):
        """Delete method for category."""
        return self.target()