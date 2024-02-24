import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from nprc import RayCast
from tqdm import tqdm

with open('lowpolyjet.json') as f:
    dataLoad = json.load(f)
    triangles = np.array(dataLoad['triangles'])
    # import triangles

# generate a bunch of ray origins
gridSize = 20
xx, zz = np.meshgrid(np.linspace(-30, 30, gridSize), np.linspace(-30, 30, gridSize))
yy = np.ones(shape=(gridSize, gridSize)) * -20
xx = xx.flatten()
yy = yy.flatten()
zz = zz.flatten()

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.add_collection(Poly3DCollection(triangles, alpha=0.2))
rv = RayCast()

for idx in tqdm(range(gridSize ** 2)):

    a1, b1, c1 = xx[idx], yy[idx], zz[idx]
    a2, b2, c2 = 0, 1, 0
    #  set origin[a1, b1, c1], direction[a2, b2, c2]
    rv.set(a2, b2, c2, a1, b1, c1)
    #  cast into triangles
    interescts = rv.cast(triangles)
    rayOrigin = np.array([a1, b1, c1])
    direction = np.array([a2, b2, c2])
    point = interescts['points']
    distance = interescts['distances']
    reflection = interescts['reflections']
    faces = interescts['faces']

    ax.add_collection(Poly3DCollection(faces, alpha=.25, facecolor='#800000'))
    for i in range(len(reflection)):
        ax.plot([rayOrigin[0], (rayOrigin[0] + distance[i] * direction[0])[0]],
                [rayOrigin[1], (rayOrigin[1] + distance[i] * direction[1])[0]],
                [rayOrigin[2], (rayOrigin[2] + distance[i] * direction[2])[0]], color='dodgerblue')
        ax.plot([point[i][0], (point[i][0] + .5 * distance[i] * reflection[i][0])[0]],
                [point[i][1], (point[i][1] + .5 * distance[i] * reflection[i][1])[0]],
                [point[i][2], (point[i][2] + .5 * distance[i] * reflection[i][2])[0]], color='crimson')
        ax.scatter([point[i][0]], [point[i][1]], [point[i][2]], color='crimson')
        #  this break will plot only the closest hit
        break

ax.scatter(xx, yy, zz, color='dodgerblue', alpha=.25)
ax.set_xlim(-50, 50)
ax.set_ylim(-50, 50)
ax.set_zlim(-50, 50)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
print(f"checked {len(triangles) * gridSize ** 2} triangles")
