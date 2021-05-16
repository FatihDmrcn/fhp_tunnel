# -*- coding: utf-8 -*-
"""
@author: fatih
"""
import numpy as np
from numpy.random import default_rng
import matplotlib.pyplot as plt
import copy


class FHP_Model():
    def __init__(self, height=250, width=750, randomized=True):
        self.h = height
        self.w = width
        self.field_randomized = randomized
        self.coordinates = []
        self.field = self.init_field()
        if self.field_randomized:
            self.randomize_field()

    def init_field(self):
        field = np.zeros((8, self.h, self.w), dtype=np.long)
        # Apply upper and lower wall
        field[6,:3,:]=1
        field[6,-3:,:]=1
        # List of coordinates at which to find the nodes
        for i in range(int(self.h/2)):
            for j in range(self.w):
                if (i%2) == 0:
                    if j%2 == 0:
                        field[7, 2*i, j] = 1
                        self.coordinates.append((2 * i, j))
                if (i%2) != 0:
                    if j%2 != 0:
                        field[7, 2*i, j] = 1
                        self.coordinates.append((2 * i, j))
        return field

    def randomize_field(self):
        rng = default_rng()
        for c in self.coordinates:
            if self.field[6, c[0], c[1]] != 1:
                d = rng.integers(low=0, high=2, size=6)
                d = d.astype(np.long)
                self.field[:6, c[0], c[1]] = d

    def flux(self):
        # Create new field fo the next time step t+1
        field_t1 = np.zeros_like(self.field)
        # Copy control bits from previous time step
        field_t1[7,:,:] = self.field[7,:,:]
        # Copy walls from previous time step
        field_t1[6,:,:] = self.field[6,:,:]

        # These subarrays contain the desired particles
        ur_t1 = self.field[0, 2:  ,  :-1] # from:down left  |to:upper right|for:t+1
        rr_t1 = self.field[1,  :  ,  :-2] # from:left       |to:right      |for:t+1
        dr_t1 = self.field[2,  :-2,  :-1] # from:upper left |to:down right |for:t+1
        dl_t1 = self.field[3,  :-2, 1:  ] # from:upper right|to:down left  |for:t+1
        ll_t1 = self.field[4,  :  , 2:  ] # from:right      |to:left       |for:t+1
        ul_t1 = self.field[5, 2:  , 1:  ] # from:down right |to:upper left |for:t+1

        # Move particles to the corresponding nodes
        field_t1[0,  :-2, 1:  ] = ur_t1
        field_t1[1,  :  , 2:  ] = rr_t1
        field_t1[2, 2:  , 1:  ] = dr_t1
        field_t1[3, 2:  ,  :-1] = dl_t1
        field_t1[4,  :  ,  :-2] = ll_t1
        field_t1[5,  :-2,  :-1] = ul_t1

        # Bounce back particles if hitting a wall
        field_t1[3, 2:  ,  :-1] += np.multiply(field_t1[6,  :-2, 1:  ], ur_t1)
        field_t1[4,  :  ,  :-2] += np.multiply(field_t1[6,  :  , 2:  ], rr_t1)
        field_t1[5,  :-2,  :-1] += np.multiply(field_t1[6, 2:  , 1:  ], dr_t1)
        field_t1[0,  :-2, 1:  ] += np.multiply(field_t1[6, 2:  ,  :-1], dl_t1)
        field_t1[1,  :  , 2:  ] += np.multiply(field_t1[6,  :  ,  :-2], ll_t1)
        field_t1[2, 2:  , 1:  ] += np.multiply(field_t1[6,  :-2,  :-1], ul_t1)

        # Influx condition
        for c in self.coordinates:
            if c[1]<4:
                # field_t1[:3,c[0],c[1]] = np.array([1,1,1], dtype=np.long)
                field_t1[:6,c[0],c[1]] = np.array([1, 1, 1, 0, 0, 0], dtype=np.long)

        # Clean nodes from particles if nodes are walls
        for c in self.coordinates:
            if field_t1[6,c[0],c[1]] == 1:
                d = np.zeros((1,6))
                d = d.astype(np.long)
                field_t1[:6,c[0],c[1]] = d
        return field_t1

    def scatter(self):
        field_t1 = self.field
        rng = default_rng()
        vectors = {'4':[np.array([1,1,0,1,1,0]),
                        np.array([1,0,1,1,0,1]),
                        np.array([0,1,1,0,1,1])],
                   '3':[np.array([1,0,1,0,1,0]),
                        np.array([0,1,0,1,0,1])],
                   '2':[np.array([1,0,0,1,0,0]),
                        np.array([0,1,0,0,1,0]),
                        np.array([0,0,1,0,0,1])]}
        for c in self.coordinates:
            initial_vector = field_t1[:6,c[0],c[1]]
            particles = str(sum(initial_vector))
            if particles in ('2', '3', '4'):
                for i, v in enumerate(vectors[particles],0):
                    if all(v == initial_vector):
                        v_array = copy.deepcopy(vectors[particles])
                        del v_array[i]
                        choice = rng.integers(low=0, high=len(v_array))
                        field_t1[:6,c[0],c[1]] = v_array[choice]
                        break
        return field_t1

    def run(self, t_steps=100):
        for t in range(t_steps):
            self.field = self.flux()
            self.field = self.scatter()
            print(t+1)
        a = np.sum(self.field[:6, :, :], axis=0)
        plt.imshow(a)
        plt.show()


def field_square(field, coords):
    field_square = field
    square = [c for c in coords if 180<c[0]<220 and 280<c[1]<320]
    for s in square:
        if field_square[6,s[0],s[1]] != 1:
            d = np.ones((1,6))
            d = d.astype(np.long)
            field_square[:6,s[0],s[1]] = d
    return field_square


model = FHP_Model(250, 750)
model.run()
