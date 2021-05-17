# -*- coding: utf-8 -*-
"""
@author: fatih
"""
import numpy as np
from numpy.random import default_rng
import matplotlib.pyplot as plt
import PyQt5.QtCore as Qtc


class FHP_Model(Qtc.QObject):

    time_step = Qtc.pyqtSignal(np.ndarray)

    vectors = {'4':[np.array([1,1,0,1,1,0]),
                    np.array([1,0,1,1,0,1]),
                    np.array([0,1,1,0,1,1])],
               '3':[np.array([1,0,1,0,1,0]),
                    np.array([0,1,0,1,0,1])],
               '2':[np.array([1,0,0,1,0,0]),
                    np.array([0,1,0,0,1,0]),
                    np.array([0,0,1,0,0,1])]}

    def __init__(self, height=250, width=750, randomized=True):
        super().__init__()
        self.__h = height
        self.__w = width
        self.__field_randomized = randomized
        self.__coordinates = []
        self.field = self.__init_field()
        if self.__field_randomized:
            self.__randomize_field()
            self.__field_square()

    def __init_field(self):
        field = np.zeros((8, self.__h, self.__w), dtype=np.long)
        # Apply upper and lower wall
        field[6,:3,:]=1
        field[6,-3:,:]=1
        # List of __coordinates at which to find the nodes
        for i in range(int(self.__h / 2)):
            for j in range(self.__w):
                if (i%2) == 0:
                    if j%2 == 0:
                        field[7, 2*i, j] = 1
                        self.__coordinates.append((2 * i, j))
                if (i%2) != 0:
                    if j%2 != 0:
                        field[7, 2*i, j] = 1
                        self.__coordinates.append((2 * i, j))
        return field

    def __randomize_field(self):
        rng = default_rng()
        for c in self.__coordinates:
            if self.field[6, c[0], c[1]] != 1:
                d = rng.integers(low=0, high=2, size=6)
                d = d.astype(np.long)
                self.field[:6, c[0], c[1]] = d

    def __field_square(self):
        square = [c for c in self.__coordinates if 100<c[0]<150 and 300<c[1]<350]
        for s in square:
            if self.field[6,s[0],s[1]] != 1:
                d = np.ones((1,6))
                d = d.astype(np.long)
                self.field[:6,s[0],s[1]] = d

    def __flux(self):
        # Create new field fo the next time step t+1
        field_t1 = np.zeros_like(self.field)
        # Copy control bits from previous time step
        field_t1[7,:,:] = self.field[7,:,:]
        # Copy walls from previous time step
        field_t1[6,:,:] = self.field[6,:,:]

        # These sub-arrays contain the desired particles
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
        for c in self.__coordinates:
            if c[1]<4:
                # field_t1[:3,c[0],c[1]] = np.time_step([1,1,1], dtype=np.long)
                field_t1[:6,c[0],c[1]] = np.array([1, 1, 1, 0, 0, 0], dtype=np.long)

        # Clean nodes from particles if nodes are walls
        for c in self.__coordinates:
            if field_t1[6,c[0],c[1]] == 1:
                d = np.zeros((1,6))
                d = d.astype(np.long)
                field_t1[:6,c[0],c[1]] = d
        self.field = field_t1

    def __scatter(self):
        rng = default_rng()
        for c in self.__coordinates:
            initial_vector = self.field[:6,c[0],c[1]]
            particles = str(sum(initial_vector))
            if particles in ('2', '3', '4'):
                for i, v in enumerate(self.vectors[particles],0):
                    if all(v == initial_vector):
                        # Create a list of all possible indices
                        choice_list = list(range(len(self.vectors[particles])))
                        # Delete the index number which is the current vector
                        choice_list.remove(i)
                        choice = rng.choice(choice_list)
                        self.field[:6,c[0],c[1]] = self.vectors[particles][choice]
                        break

    def do_step(self):
        self.__flux()
        self.__scatter()
        array = np.sum(self.field[:6, :, :], axis=0)
        self.time_step.emit(array)

    def get_array(self):
        return np.sum(self.field[:6, :, :], axis=0)

    def run(self, t_steps=100):
        for t in range(t_steps):
            self.do_step()


if __name__ == "__main__":
    model = FHP_Model(250, 750)
    model.run()
