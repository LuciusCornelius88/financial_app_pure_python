from config import invalid_deletion_message

class InvalidDeletion(Exception):
    def __init__(self) -> None:
        self.message = invalid_deletion_message
        super().__init__(self.message)