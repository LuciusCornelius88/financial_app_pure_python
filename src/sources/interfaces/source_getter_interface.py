from config import error_code, stop_function_code, exit_code, interruption_message, id_delimiter


class SourceGetterInterface:
    def __init__(self, sources_storage) -> None:
        self.__exit_code = exit_code
        self.__sources_storage = sources_storage
        self.__input_promt = f'Enter instance ID among given or enter {self.__exit_code} to exit the input:\n'


    def get(self):
        available_instances = self.__get_available_instances()
        view_message = self.__create_view_mesage(available_instances)

        while True:
            instance_id = self.__get_instance_id(available_instances, view_message)
            if instance_id == error_code:
                continue
            elif instance_id == stop_function_code:
                return error_code
            else:
                return self.__sources_storage.get(instance_id)


    def __get_available_instances(self):
        return {key.split(id_delimiter)[1]: key.split(id_delimiter)[0] for key in self.__sources_storage.data.keys()}
        

    def __create_view_mesage(self, instances):
        return '\n'.join(f'{key}: {value}' for key, value in instances.items())

    
    def __get_instance_id(self, instances, message):
        try:
            instance_id = str(input(f'{self.__input_promt}{message}\n'))
            if instance_id == self.__exit_code:
                print(interruption_message)
                return stop_function_code
            else:
                return id_delimiter.join([instances[instance_id], instance_id])
        except KeyError:
            print(f'{KeyError.__name__}: there is no such id. Try again.\n')
            return error_code
        except ValueError:
            print(f'{ValueError.__name__}: id should be numeric. Try again!')
            return error_code
        except KeyboardInterrupt:
            print(f'{KeyboardInterrupt.__name__}: {interruption_message}')
            return stop_function_code