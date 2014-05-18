# This program adds up integers in the command line
import sys
total = 0
for arg in sys.argv[1:]:
    total += int(arg)
print('sum = %s' % total)
