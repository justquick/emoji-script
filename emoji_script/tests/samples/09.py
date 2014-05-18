# indent your Python code to put into an email
import glob
# glob supports Unix style pathname extensions
python_files = glob.glob('*.py')
for file_name in sorted(python_files):
    print('    ------' + file_name)

    for line in open(file_name).readlines():
        print('    ' + line.rstrip())

    print()
