class GetterPattern:

    def __init__(self, transaction_storage) -> None:
        self.transaction_storage = transaction_storage

    
    def target(self):
        ...


class TransactionGetterInterface(GetterPattern):

    def __init__(self, transaction_storage) -> None:
        super().__init__(transaction_storage)


    def get(self):
        """Get method for source."""
        return self.target()
    

class TransactionDeletionInterface(GetterPattern):

    def __init__(self, transaction_storage) -> None:
        super().__init__(transaction_storage)


    def delete(self):
        """Get method for source."""
        return self.target()