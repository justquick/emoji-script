import re
for test_string in ['555-1212', 'ILL-EGAL']:
    if re.match(r'^\d{3}-\d{4}$', test_string):
        print('%s is a valid US local phone number' % test_string)
    else:
        print('%s rejected' % test_string)
