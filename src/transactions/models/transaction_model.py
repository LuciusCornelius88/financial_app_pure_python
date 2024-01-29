from hmac import new
import sys
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from config import id_delimiter 


class Transaction:
    _instances = 0


    def __new__(cls, *args, **kwargs):
        cls._instances += 1
        instance = super().__new__(cls)
        cls.instance_id = cls._instances
        return instance


    def __init__(self, fields: dict) -> None:
        self._id_suffix = f'{id_delimiter}{self.instance_id}'
        self._id = None
        self._source = None
        self._target = None

        self.id = fields['date']
        self.date = fields['date']
        self.description = fields['description']
        self.type = fields['type']
        self.source_amount = fields['source_amount']
        self.target_amount = fields['target_amount']
        self.source = fields['source']
        self.target = fields['target']
        self._change_log = []

        change_log = f'{self.__class__.__name__} {self.id} was created.'
        self._update_change_log(change_log)


    @property
    def id(self):
        return self._id
    

    @id.setter
    def id(self, date):
        if date is None:
            self._id = None
        else:
            self._id = date + self._id_suffix

    
    @property
    def source(self):
        return self._source
    

    @source.setter
    def source(self, source):
        if source is None:
            self._source = None
        else:
            source.update_transaction(self)
            self._source = source

    
    @property
    def target(self):
        return self._target
    

    @target.setter
    def target(self, target):
        if target is None:
            self._target = None
        else:
            target.update_transaction(self, target=True)
            self._target = target


    def delete(self) -> str:
        change_log = f'Transaction {self.id}: {self.description} {self.source_amount} was deleted.\n'

        self.id = None
        self.date = None
        self.description = None
        self.source = None
        self.target = None
        self.type = None
        self.source_amount = None
        self.target_amount = None

        self._update_change_log(change_log)
        return change_log


    def view_change_log(self):
        return '\n\n'.join(self._change_log)


    def update(self, params):
        ch_date_log = self._update_date(params['date'])
        ch_description_log = self._update_description(params['description'])
        ch_source_log = self._update_source(params['source'])
        ch_target_log = self._update_target(params['target'])
        ch_type_log = self._update_type(params['type'])
        ch_source_amount_log = self._update_source_amount(params['source_amount'])
        ch_target_amount_log = self._update_target_amount(params['target_amount'])

        return (ch_date_log + ch_description_log + ch_source_log + 
                ch_target_log + ch_type_log + ch_source_amount_log + ch_target_amount_log)


    def _update_date(self, new_date):
        change_log = f'Date changed from {self.date} to {new_date}.\n'
        self.id = new_date
        self.date = new_date
        self._update_change_log(change_log)

        return change_log


    def _update_description(self, new_description):
        change_log = f'Description changed from "{self.description}" to "{new_description}".\n'
        self.description = new_description
        self._update_change_log(change_log)

        return change_log

    
    def _update_source(self, new_source):
        change_log = f'Source changed from {self.source.id} to {new_source.id}.\n'
        self.source = new_source
        self._update_change_log(change_log)

        return change_log


    def _update_target(self, new_target):
        change_log = f'Target changed from {self.target.id} to {new_target.id}.\n'
        self.target = new_target
        self._update_change_log(change_log)

        return change_log


    def _update_type(self, new_type):
        change_log = f'Type changed from {self.type} to {new_type}.\n'
        self.type = new_type
        self._update_change_log(change_log)

        return change_log


    def _update_source_amount(self, new_source_amount):
        change_log = f'Source amount changed from {self.source_amount} to {new_source_amount}.\n'
        self.source_amount = new_source_amount
        self._update_change_log(change_log)

        return change_log
    

    def _update_target_amount(self, new_target_amount):
        change_log = f'Target amount changed from {self.target_amount} to {new_target_amount}.\n'
        self.target_amount = new_target_amount
        self._update_change_log(change_log)

        return change_log


    def _update_change_log(self, change_log):
        log_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._change_log.append(log_date + '\n' + change_log)


    def __repr__(self) -> str:
        return (f'Transaction id: {self.id} \n' +
                f'Transaction date: {self.date} \n' +
                f'Transaction description: {self.description}\n' +
                f'Transaction source: {self.source}\n' +
                # f'Transaction target: {self.target.id}\n' +
                f'Source amount: {self.source_amount}\n' + 
                f'Target amount: {self.target_amount}')


    def __str__(self):
        return self.__repr__()