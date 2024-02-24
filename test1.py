import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from nprc import RayCast

with open('highpolyjet.json') as f:
    dataLoad = json.load(f)
    triangles = np.array(dataLoad['triangles'])

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.add_collection(Poly3DCollection(triangles, alpha=0.2))
ax.set_xlim(-50, 50)
ax.set_ylim(-50, 50)
ax.set_zlim(-50, 50)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

rayOrigin = np.array([40, 5, 80])
direction = np.array([-1, 0, -2])

rv = RayCast()
rv.set(direction[0], direction[1], direction[2], rayOrigin[0], rayOrigin[1], rayOrigin[2])
interescts = rv.cast(triangles)
point = interescts['points']
distance = interescts['distances']
reflection = interescts['reflections']
faces = interescts['faces']

#  plot hit triangles
ax.add_collection(Poly3DCollection(interescts['faces'], alpha=.25, facecolor='#800000'))

for i in range(interescts['size']):
    #  plot rays that hit with their distance
    ax.plot([rayOrigin[0], (rayOrigin[0] + distance[i] * direction[0])[0]],
            [rayOrigin[1], (rayOrigin[1] + distance[i] * direction[1])[0]],
            [rayOrigin[2], (rayOrigin[2] + distance[i] * direction[2])[0]], color='dodgerblue')

    #  plot rays reflections
    ax.plot([point[i][0], (point[i][0] + .5 * distance[i] * reflection[i][0])[0]],
            [point[i][1], (point[i][1] + .5 * distance[i] * reflection[i][1])[0]],
            [point[i][2], (point[i][2] + .5 * distance[i] * reflection[i][2])[0]], color='crimson')

    #  plot hits
    ax.scatter([point[i][0]], [point[i][1]], [point[i][2]], color='crimson')
print(f"checked {len(triangles)} triangles")
