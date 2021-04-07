# purpose: to draw detector's hitmap

import random

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

# log scale colorbar with imshow
import matplotlib.colors as mcolors

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# make test data
data = np.array([[random.randint(0, 100) for row in range(66)]
                for column in range(4)])
for row in [0, 61]:
    for column in [0, 2]:
        data_tmp = random.randint(0, 100)
        data[column][row:row+5] = data_tmp
        data[column+1][row:row+5] = data_tmp
for row in range(5, 61, 7):
    for column in [0, 3]:
        data[column][row:row+7] = random.randint(0, 100)
print('data:', data)

# make log scale colorbar
norm = mcolors.SymLogNorm(linthresh=1, vmin=0, vmax=data.max()*10)
# plot imshow and colorbar
image_imshow = ax.imshow(data, cmap="viridis", aspect='auto', norm=norm)
fig.colorbar(image_imshow, orientation='horizontal')

# hide ticks and it's label
ax.set_xticks([])
ax.set_yticks([])
ax.xaxis.set_ticklabels([])
ax.yaxis.set_ticklabels([])

# overlay rectangular area on plot
for x in range(5, 61):
    for y in range(2):
        center_area = plt.Rectangle(
            # (x,y) of upper left corner, width, hight
            (-0.5 + x, 0.5 + y), 1, 1,
            edgecolor="Black", fill=False)
        ax.add_patch(center_area)

for x in [0 - 0.5, 61 - 0.5]:
    for y in [-0.5, 1.5]:
        leftright_area = plt.Rectangle(
            (x, y), 5, 2,
            edgecolor="Black", fill=False)
        ax.add_patch(leftright_area)

for x in range(5, 60, 7):
    for y in [-0.5, 2.5]:
        topbottom_area = plt.Rectangle(
            (-0.5 + x, y), 7, 1,
            edgecolor="Black", fill=False)
        ax.add_patch(topbottom_area)

plt.show()
