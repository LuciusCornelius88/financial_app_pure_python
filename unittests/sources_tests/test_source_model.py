import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent / 'src/sources/models'))

from source_model import Source


class TestSource(unittest.TestCase):
    def setUp(self):
        # Initialize a sample source for testing
        fields = {'name': 'TestSource', 'init_balance': 100}
        self.source = Source(fields)

    def test_id_property(self):
        # Test the id property
        self.assertEqual(self.source.id, 'TestSource')

    def test_name_property(self):
        # Test the name property
        self.assertEqual(self.source.name, 'TestSource')

        # Change the name
        self.source.name = 'NewTestSource'
        self.assertEqual(self.source.name, 'NewTestSource')

    def test_init_balance_property(self):
        # Test the init_balance property
        self.assertEqual(self.source.init_balance, 100)

        # Change the init_balance
        self.source.init_balance = 150
        self.assertEqual(self.source.init_balance, 150)

    def test_current_balance_property(self):
        # Test the current_balance property
        self.assertEqual(self.source.current_balance, 100)

        # Change the current_balance
        self.source.current_balance = 120
        self.assertEqual(self.source.current_balance, 120)

    def test_current_transaction_property(self):
        # Test the current_transaction property
        self.assertIsNone(self.source.current_transaction)

        # Change the current_transaction
        self.source.current_transaction = 'Transaction123'
        self.assertEqual(self.source.current_transaction, 'Transaction123')

    def test_delete_method(self):
        # Test the delete method
        log_message = self.source.delete()

        # Check if the source attributes are set to None after deletion
        self.assertIsNone(self.source.id)
        self.assertIsNone(self.source.name)
        self.assertIsNone(self.source.init_balance)
        self.assertIsNone(self.source.current_balance)
        self.assertIsNone(self.source.current_transaction)
        self.assertIsNone(self.source._transactions)

        # Check if the log message contains the expected deletion message
        self.assertIn('Source None:', log_message)
        self.assertIn('was deleted', log_message)

    def test_view_change_log_method(self):
        # Test the view_change_log method
        self.source._change_log = ['Log Entry 1', 'Log Entry 2']

        # Check if the returned log string contains the expected log entries
        log_string = self.source.view_change_log()
        self.assertIn('Log Entry 1', log_string)
        self.assertIn('Log Entry 2', log_string)

    def test_update_method(self):
        # Test the update method
        params = {'name': 'UpdatedSource', 'init_balance': 120}
        log_message = self.source.update(params)

        # Check if the log message contains the expected update messages
        self.assertIn('Source name changed from NewTestSource to UpdatedSource.', log_message)
        self.assertIn('New init balance: 120', log_message)
        self.assertIn('Current balance: 120', log_message)
        self.assertIn('Difference: 20', log_message)


if __name__ == '__main__':
    unittest.main()
