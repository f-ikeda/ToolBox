# purpose: to save and load numpy's array

import sys

import numpy as np


argument = sys.argv
if (len(argument) != 3):
    print('USEAGE: $ python3 saveload_array.py path_to_dir file_name')
    sys.exit()
else:
    path_to_dir = argument[1]
    file_name = argument[2]

array_foo = np.array([0, 1, 2, 3, 4])
print('before, array_foo:', array_foo)
array_bar = np.array([10, 20, 30, 40, 50])
print('before, array_bar:', array_bar)

# save
np.savez(path_to_dir + file_name + '.npz',
         array_1st=array_foo, array_2nd=array_bar)
print('array_foo and array_bar are saved as array_1st and array_2nd in',
      path_to_dir + file_name + '.npz')

# load
npz = np.load(path_to_dir + file_name + '.npz')
array_foo = npz['array_1st']
print('after, array_foo:', array_foo)
array_bar = npz['array_2nd']
print('after, array_bar:', array_bar)
