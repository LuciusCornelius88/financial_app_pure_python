import sys
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from config import id_delimiter 


class Source:
    _instances = 0

    def __new__(cls, *args, **kwargs):
        cls._instances += 1
        instance = super().__new__(cls)
        instance.instance_id = cls._instances
        return instance

    def __init__(self, fields: dict) -> None:
        self._id_suffix = f'{id_delimiter}{self.instance_id}'
        self._id = None
        self._name = None
        self._init_balance = None
        self._current_balance = None
        self._transactions = {}
        self._change_log = []

        self.id = fields['name']
        self.name = fields['name']
        self.init_balance = fields['init_balance']
        self.current_balance = fields['init_balance']

        change_log = f'{self.__class__.__name__} {self.id} was created.'
        self._update_change_log(change_log)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, name):
        if name is None:
            self._id = None
        else:
            self._id = name + self._id_suffix

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def init_balance(self):
        return self._init_balance

    @init_balance.setter
    def init_balance(self, new_balance):
        self._init_balance = new_balance

    @property
    def current_balance(self):
        return self._current_balance

    @current_balance.setter
    def current_balance(self, new_balance):
        self._current_balance = new_balance


    def delete(self) -> str:
        change_log = f'Source {self.id}: {self.name} was deleted.\n'

        self.id = None
        self.name = None
        self.init_balance = None
        self.current_balance = None
        self.current_transaction = None
        self._transactions = None

        self._update_change_log(change_log)
        return change_log


    def view_transactions(self) -> str:
        return '\n\n'.join(self._transactions)


    def view_change_log(self) -> str:
        return '\n\n'.join(self._change_log)


    def revert_transaction(self, transaction_id, target=False):
        transaction = self._transactions[transaction_id]
        self._update_current_balance(transaction, target=target, revert=True)
        del self._transactions[transaction_id]
        change_log = f'Transaction {transaction_id} was deleted.\n'
        self._update_change_log(change_log)

    
    def fake_revert(self, transaction_id, target):
        transaction = self._transactions[transaction_id]
        amount = transaction.target_amount if target else transaction.source_amount
        return self.current_balance - amount

    
    def update_transaction(self, transaction, target=False):
        self._update_current_balance(transaction, target=target)
        self._update_transactions(transaction)


    def update(self, params) -> str:
        ch_name_log = self._update_name(params['name'])
        ch_balance_log = self._update_init_balance(params['init_balance'])

        return ch_name_log + ch_balance_log


    def _update_current_balance(self, transaction, target, revert=False):
        amount = transaction.target_amount if target else transaction.source_amount
        difference = (amount * -1) if revert else amount 
        self.current_balance += difference
        change_log = (f'New current balance: {self.current_balance}\n' +
                      f'Initial balance: {self.init_balance}\n' +
                      f'Difference: {difference}.\n\n')
        self._update_change_log(change_log)

    
    def _update_transactions(self, transaction):
        self._transactions[transaction.id] = transaction
        change_log = f'Transaction {transaction.id} was added.'
        self._update_change_log(change_log)


    def _update_name(self, new_name: str) -> str:
        change_log = f'Source name changed from {self.name} to {new_name}.\n'
        self.id = new_name
        self.name = new_name
        self._update_change_log(change_log)

        return change_log


    def _update_init_balance(self, new_balance: float) -> str:
        difference = new_balance - self.init_balance
        self.init_balance = new_balance
        self.current_balance += difference

        change_log = (f'New init balance: {self.init_balance}\n' +
                      f'Current balance: {self.current_balance}\n' +
                      f'Difference: {difference}.\n\n')
        self._update_change_log(change_log)

        return change_log


    def _update_change_log(self, change_log):
        log_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._change_log.append(log_date + '\n' + change_log)


    def __repr__(self) -> str:
        return (f'Source id: {self.id} \n' +
                f'Source name: {self.name}\n' +
                f'Source init balance: {self.init_balance}\n' +
                f'Source current balance: {self.current_balance}')


    def __str__(self) -> str:
        return self.__repr__()
