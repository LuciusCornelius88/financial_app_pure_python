from pathlib import Path

dumps_path = str(Path(__file__).parent.parent / 'dumps/')
sources_dump_file = '/sources_copy.bin'
categories_dump_file = '/categories_copy.bin'
transactions_dump_file = '/transactions_copy.bin'

stop_function_code = '0xFF'
error_code = '0xff'
exit_code = '000'
default_input = ''
date_format = '%d-%m-%Y'

goodbye_message = 'Good bye!\n'
interruption_message = 'Input was interrupted.\n'
key_error_message = ': there is no such id. Try again.\n'
value_error_message = ': invaluid input value. Try again!\n'
invalid_deletion_message = 'Deletion is impossible as there are transactions related to the object. Delete transactions first.\n'
loop_exit_message = 'Stop working with'
create_obj_message = 'Created object with data:\n'
create_instance_message = 'Created instances:\n'

id_delimiter = ': '
