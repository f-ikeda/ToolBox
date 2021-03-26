# purpose: to get a list of filenames in a directory

import sys

import os

argument = sys.argv
if (len(argument) != 2):
    print('USEAGE: $ python3 get_filenames.py path_to_dir')
    sys.exit()
else:
    path_to_dir = argument[1]

file_and_dir_names = os.listdir(path_to_dir)
files_names = [f for f in file_and_dir_names
               if os.path.isfile(os.path.join(path_to_dir, f))]
print('files_names:', files_names)

# add a condition
files_names_py = [f for f in file_and_dir_names
                  if (os.path.isfile(os.path.join(path_to_dir, f)) and ('.py' in f))]
print('files_names_py:', files_names_py)
