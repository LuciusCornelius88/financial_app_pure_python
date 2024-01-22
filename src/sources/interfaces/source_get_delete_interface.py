from config import error_code, stop_function_code, exit_code, interruption_message, \
    id_delimiter, key_error_message, value_error_message
from decorators import errors_handler


class GetterPattern:
    def __init__(self, sources_storage) -> None:
        self._sources_storage = sources_storage
        self._exit_code = exit_code
        self._input_promt = f'Enter instance ID among given or enter {self._exit_code} to exit the input:\n'
        self._target_method = None


    def target(self):
        available_keys = self._get_available_keys()
        view_message = self._create_view_mesage()

        while True:
            instance_id = self._get_instance_id(available_keys, view_message)
            if instance_id == error_code:
                continue
            elif instance_id == stop_function_code:
                return error_code
            else:
                return self._target_method(instance_id)


    def _get_available_keys(self):
        return {key.split(id_delimiter)[1]: key for key in self._sources_storage.data.keys()}
        

    def _create_view_mesage(self):
        return '\n'.join(f'{key.split(id_delimiter)[1]}: {value.id.split(id_delimiter)[0]}' for key, value in self._sources_storage.items())


    @errors_handler
    def _get_instance_id(self, keys, message):
        instance_id = input(f'{self._input_promt}{message}\n')
        if instance_id == self._exit_code:
            print(interruption_message)
            return stop_function_code
        return keys[instance_id]
 


class SourceGetterInterface(GetterPattern):
    def __init__(self, sources_storage) -> None:
        super().__init__(sources_storage)
        self._target_method = self._sources_storage.get



class SourceDeletionInterface(GetterPattern):
    def __init__(self, sources_storage) -> None:
        super().__init__(sources_storage)
        self._target_method = self._sources_storage.delete