# purpose: to reads binary file and packs it into array, separating them by specific bytes, with some ways

import os
import sys
import random
import time

import numpy as np


def make_binaryfile(data_unit):
    # make data_unit Bytes * 10M test_data
    if (os.path.isfile('test_data')):
        print('test_data is already exist!')
    else:
        print('start to make test_data')
        with open('test_data', 'ab') as f:
            for i in range(int(1e+7)):
                bytearray_temp = bytearray(
                    [random.randint(0, 255) for i in range(data_unit)])

                f.write(bytearray_temp)
        print('finish to make test_data')


def way1(data_unit, data_type):
    # use for-statement
    array_size = int(os.path.getsize('test_data') / data_unit)
    data = np.zeros(array_size, dtype=data_type)
    with open('test_data', 'rb') as f:
        for i in range(array_size):
            data[i] = f.read(data_unit)
    return data


def way2(data_unit, data_type):
    # use list-comprehension
    array_size = int(os.path.getsize('test_data') / data_unit)
    with open('test_data', 'rb') as f:
        data = np.array([f.read(data_unit)
                         for i in range(array_size)],
                        dtype=data_type)
    return data


def way3(data_unit, data_type):
    # use np.frombuffer()
    array_size = int(os.path.getsize('test_data') / data_unit)
    data = np.zeros(array_size, dtype=data_type)
    with open('test_data', 'rb') as f:
        data = f.read(data_unit * array_size)
    data = np.frombuffer(data, data_type)
    return data


DATA_UNIT = 13
DATA_TYPE = np.dtype((np.void, DATA_UNIT))

# make test data
make_binaryfile(DATA_UNIT)

TIME_S = time.time()
data = way1(DATA_UNIT, DATA_TYPE)
TIME_F = time.time()
print('way1, time:', TIME_F - TIME_S)
print('data:', data)

TIME_S = time.time()
data = way2(DATA_UNIT, DATA_TYPE)
TIME_F = time.time()
print('way2, time:', TIME_F - TIME_S)
print('data:', data)

TIME_S = time.time()
data = way3(DATA_UNIT, DATA_TYPE)
TIME_F = time.time()
print('way3, time:', TIME_F - TIME_S)
print('data:', data)
