# purpose: to save and load list and dictionary

import sys

import pickle


def pickle_save(something, path_to_file):
    # something may be list or dictionary
    with open(path_to_file, mode='wb') as f:
        pickle.dump(something, f)


def pickle_load(path_to_file):
    with open(path_to_file, mode='rb') as f:
        something = pickle.load(f)
        return something


argument = sys.argv
if (len(argument) != 2):
    print('USEAGE: $ python3 saveload_listdict.py path_to_dir')
    sys.exit()
else:
    path_to_dir = argument[1]

list_foo = [0, 1, 2, 3, 4, 5]
print('before, list_foo:', list_foo)
dictionary_bar = {0: 10, 1: 20, 2: 30, 3: 40, 4: 50}
print('before, dictionary_bar:', dictionary_bar)

# save
pickle_save(list_foo, path_to_dir + 'list_foo.pickle')
print('list_foo is saved as', path_to_dir + 'list_foo.pickle')
pickle_save(dictionary_bar, path_to_dir + 'dictionary_bar.pickle')
print('dictionary_bar is saved as', path_to_dir + 'dictionary_bar.pickle')


# load
list_foo = pickle_load(path_to_dir + 'list_foo.pickle')
print('after, list_foo: ', list_foo)
dictionary_bar = pickle_load(path_to_dir + 'dictionary_bar.pickle')
print('after, dictionary_bar: ', dictionary_bar)
