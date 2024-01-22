from collections import UserDict


class Transactions(UserDict):
    __instance  = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    

    def restore_from_file(self):
        ...