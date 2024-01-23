class TransactionUpdateInterface:

    def __init__(self, transaction_storage) -> None:
        self.transaction_storage = transaction_storage


    def update(self):
        ...