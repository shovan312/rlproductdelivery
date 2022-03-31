from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import ast

raw_data = open("./output_sim.txt").read().split("\n")
raw_data = [[i.lstrip()] for i in raw_data]
raw_data = [i[0].split(" [") for i in raw_data]
raw_data = raw_data[:-1]

c = [float(i[0]) for i in raw_data]
arr = ["["+i[1] for i in raw_data]
arr = [list(map(int, ast.literal_eval(i))) for i in arr]
arr = np.array(arr)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = arr[:, 0]
y = arr[:, 1]
z = arr[:, 2]

ax.set_xlabel('move')
ax.set_ylabel('empty')
ax.set_zlabel('unload')


img = ax.scatter(x, y, z, c=c, cmap=plt.copper())
fig.colorbar(img)
plt.show()