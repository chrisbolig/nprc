import numpy as np

"""
a ray casting class made from three stack overflows
expects triangles 

searching went like:
    1) see if triangle gets hit by a ray
    2) see if point is in triangle
    3) get reflection

next step would be to see if a class can be made to (numpy) vectorize many rays origins and directions
instead of looping through them
"""


class RayCast:
    def __init__(self):
        self.faces = None
        self.t = None
        self.nhat = None
        self.reflection = None
        self.pt = None
        self.direction = None
        self.dhat = None
        self.pOffset = None
        self.intersects = None

    def set(self, d1, d2, d3, o1=0., o2=0., o3=0.):
        self.direction = np.array([d1, d2, d3])
        self.dhat = self.direction / np.sqrt((np.sum(self.direction ** 2)))
        self.pOffset = np.array([o1, o2, o3])

    def cast(self, triangle):
        triangle = np.array(triangle)
        if triangle.shape[1] != 3 and triangle.shape[2] != 3:
            print('bad')
        #  https://math.stackexchange.com/questions/1979876/ray-casting-algorithm-in-ray-triangle-intersection
        #  something i figured out, subtract triangle by ray_origin if the ray_origin in not at (0,0,0)
        triangle = triangle - self.pOffset
        A = triangle[:, 0]
        B = triangle[:, 1]
        C = triangle[:, 2]
        u = B - A
        v = C - A
        nverts = triangle.shape[0]
        n = np.cross(u, v)
        nhat = n / np.sqrt((np.sum(n ** 2, axis=1)).reshape(nverts, 1))
        nd = np.sum(A * nhat, axis=1)
        denom = np.sum(self.dhat * nhat, axis=1)
        dmask = denom == 0
        # dmask contains edge cases, where a ray hits the exact edge
        denom[dmask] += 1
        t = nd / denom
        tmask = ~dmask * t > 0
        tN = np.sum(tmask)
        A = A[tmask]
        t = t[tmask]
        nhat = nhat[tmask]
        n = n[tmask]
        u = u[tmask]
        v = v[tmask]
        t = t.reshape(tN, 1)
        pt = self.pOffset + t * self.dhat
        #  https://math.stackexchange.com/questions/544946/determine-if-projection-of-3d-point-onto-plane-is-within-a-triangle/544947
        w = (t * self.dhat) - A
        oneOver4ASquared = 1.0 / np.sum(n * n, axis=1)
        gamma = np.sum(np.cross(u, w) * n, axis=1) * oneOver4ASquared
        beta = np.sum(np.cross(w, v) * n, axis=1) * oneOver4ASquared
        alpha = 1 - gamma - beta
        state = (0 <= alpha) * (alpha <= 1) * (0 <= beta) * (beta <= 1) * (0 <= gamma) * (gamma <= 1)
        sN = np.sum(state)
        nhat = nhat[state]
        t = t[state]
        srted = np.argsort(t, axis=0).flatten()
        self.t = t[srted]
        self.pt = pt[state][srted]
        #  https://math.stackexchange.com/questions/13261/how-to-get-a-reflection-vector
        reflection = self.dhat - 2 * (np.sum(self.dhat * nhat, axis=1)).reshape(sN, 1) * nhat
        self.reflection = (reflection / np.sqrt((np.sum(reflection ** 2, axis=1)).reshape(sN, 1)))[srted]
        A = A[state] + self.pOffset
        B = B[tmask][state] + self.pOffset
        C = C[tmask][state] + self.pOffset
        faces = np.array([A, B, C])
        self.faces = faces.swapaxes(0, 1)[srted]
        self.intersects = {
            'faces': self.faces,
            'reflections': self.reflection,
            'points': self.pt,
            'distances': self.t,
            'size': np.sum(state)
        }
        return self.intersects
