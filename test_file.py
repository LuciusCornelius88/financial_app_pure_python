import re
from datetime import datetime

# pattern = re.compile(r'^\d{2}-\d{2}-\d{4}$')
date_str = 1000
# print(pattern.match(date_str))

new_date = datetime.strptime(date_str, '%d-%m-%Y').date()
print(new_date)