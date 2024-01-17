from config import error_code, id_delimiter

class SourceGetterInterface:
    def __init__(self, sources_storage) -> None:
        self.sources_storage = sources_storage
        self.input_promt = 'Enter instance ID among given:\n'


    def get(self):
        available_instances = self.__get_available_instances()
        view_message = self.__create_view_mesage(available_instances)
        instance_id = self.__get_instance_id(available_instances, view_message)
        if instance_id == error_code:
            return error_code
        return self.sources_storage.get(instance_id)


    def __get_available_instances(self):
        return {key.split(id_delimiter)[1]: key.split(id_delimiter)[0] for key in self.sources_storage.data.keys()}
        

    def __create_view_mesage(self, instances):
        return '\n'.join(f'{key}: {value}' for key, value in instances.items())

    
    def __get_instance_id(self, instances, message):
        try:
            instance_id = str(input(f'{self.input_promt}{message}\n'))
            return id_delimiter.join([instances[instance_id], instance_id])
        except KeyError:
            print(f'{KeyError.__name__}: there is no such id. Try again.\n')
            return error_code
        except ValueError:
            print(f'{ValueError.__name__}: id should be numeric. Try again!')
            return error_code