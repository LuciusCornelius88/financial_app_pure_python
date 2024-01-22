import sys
import os

src_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(src_folder)

# Sources

sources_folder = os.path.abspath(os.path.join(src_folder, 'sources'))
sys.path.append(sources_folder)

source_interfaces_folder = os.path.abspath(os.path.join(sources_folder, 'interfaces'))
sys.path.append(source_interfaces_folder)

source_models_folder = os.path.abspath(os.path.join(sources_folder, 'models'))
sys.path.append(source_models_folder)

# Transactions

transactions_folder = os.path.abspath(os.path.join(src_folder, 'transactions'))
sys.path.append(transactions_folder)

transaction_interfaces_folder = os.path.abspath(os.path.join(transactions_folder, 'interfaces'))
sys.path.append(transaction_interfaces_folder)

transaction_models_folder = os.path.abspath(os.path.join(transactions_folder, 'models'))
sys.path.append(transaction_models_folder)
