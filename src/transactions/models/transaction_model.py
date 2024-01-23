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
        self._category = None

        self.id = fields['date']
        self.date = fields['date']
        self.description = fields['description']
        self.source = fields['source']
        self.category = fields['category']
        self.amount = fields['amount']
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

    
    @property
    def category(self):
        return self._category
    

    @category.setter
    def category(self, category):
        if category is None:
            self._category = None


    def delete(self) -> str:
        change_log = f'Transaction {self.id}: {self.description} was deleted.\n'

        self.id = None
        self.date = None
        self.description = None
        self.source = None
        self.category = None
        self.amount = None

        self._update_change_log(change_log)
        return change_log


    def view_change_log(self):
        return '\n\n'.join(self._change_log)


    def update(self, params):
        ch_date_log = self._update_date(params['date'])
        ch_description_log = self._update_date(params['description'])
        ch_source_log = self._update_date(params['source'])
        ch_category_log = self._update_date(params['category'])
        ch_amount_log = self._update_date(params['amount'])

        return (ch_date_log + ch_description_log + ch_source_log + ch_category_log + ch_amount_log)


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


    def _update_category(self, new_category):
        change_log = f'Category changed from {self.category.id} to {new_category.id}.\n'
        self.category = new_category
        self._update_change_log(change_log)

        return change_log


    def _update_amount(self, new_amount):
        change_log = f'Amount changed from {self.amount} to {new_amount}.\n'
        self.amount = new_amount
        self._update_change_log(change_log)

        return change_log


    def _update_change_log(self, change_log):
        log_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._change_log.append(log_date + '\n' + change_log)


    def __repr__(self) -> str:
        return (f'Transaction id: {self.id} \n' +
                f'Transaction date: {self.date} \n' +
                f'Transaction description: {self.description}\n' +
                f'Transaction source: {self.source.id}\n' +
                f'Transaction category: {self.category.id}\n' +
                f'Transaction amount: {self.amount}\n')


    def __str__(self):
        return self.__repr__()