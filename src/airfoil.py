import numpy as np
import matplotlib.pyplot as plt
import PyQt5.QtCore as Qtc


class Airfoil(Qtc.QObject):

    naca = Qtc.pyqtSignal(np.ndarray)

    def __init__(self, m=2, p=4, xx=12, pts=200):
        super().__init__()
        self.pts = pts
        self.x = 1 / pts
        self.m = m / 100
        self.p = p / 10
        self.xx = xx / 100
        self.xcgt = np.zeros((self.pts, 4))          # Contains x-Value, Camber, Gradient and Thickness
        self.upper_srf = np.zeros((self.pts, 2))     # Contains coordinates for upper surface
        self.lower_srf = np.zeros((self.pts, 2))     # Contains coordinates for lower surface
        self.calculate_airfoil()

    def __calculate_xcgt(self):
        for i in range(self.pts):
            # Calculate Thickness
            a = (0.2969, -0.126, -0.3516, 0.2843, -0.1015)
            yt = (self.xx / 0.2) * (a[0] * (self.x * i) ** 0.5 +
                                    a[1] * (self.x * i) +
                                    a[2] * (self.x * i) ** 2 +
                                    a[3] * (self.x * i) ** 3 +
                                    a[4] * (self.x * i) ** 4)
            # Calculate mean camber and gradient
            if 0 <= i*self.x < self.p:
                # Mean camber up to the max point
                yc = (self.m / self.p ** 2) *\
                     (2 * self.p * i * self.x - (i * self.x) ** 2)
                # Gradient up to the max point
                dyc_dx = ((2 * self.m) / self.p ** 2) *\
                         (self.p - i * self.x)

            if self.p <= i*self.x <= 1:
                # Mean camber from the max point on
                yc = (self.m / (1 - self.p) ** 2) *\
                     (1 - 2 * self.p + 2 * self.p * i * self.x - (i * self.x) ** 2)
                # Gradient from the max point on
                dyc_dx = ((2 * self.m) / (1 - self.p) ** 2) *\
                         (self.p - i * self.x)

            self.xcgt[i][0] = i*self.x              # xc - Coordinate
            self.xcgt[i][1] = yc                    # yc - Coordinate
            self.xcgt[i][2] = dyc_dx                # Gradient
            self.xcgt[i][3] = yt                    # Thickness

    def __calculate_surface(self):
        for i in range(self.pts):
            # Calculate normalised points
            theta = np.arctan(self.xcgt[i][2])
            xu = self.xcgt[i][0] - self.xcgt[i][3]*np.sin(theta)
            yu = self.xcgt[i][1] + self.xcgt[i][3]*np.cos(theta)
            xl = self.xcgt[i][0] + self.xcgt[i][3]*np.sin(theta)
            yl = self.xcgt[i][1] - self.xcgt[i][3]*np.cos(theta)

            # Scaling up to the desired length by multiplying with length
            self.upper_srf[i][0]= self.pts * xu
            self.upper_srf[i][1]= self.pts * yu
            self.lower_srf[i][0]= self.pts * xl
            self.lower_srf[i][1]= self.pts * yl

    def calculate_airfoil(self):
        self.__calculate_xcgt()
        self.__calculate_surface()

    def getMaxY(self):
        upper = np.transpose(self.upper_srf)
        return int(np.amax(upper[1]))+1

    def getMinY(self):
        lower = np.transpose(self.lower_srf)
        return int(np.amin(lower[1]))-1

    def getH(self):
        return self.getMaxY()-self.getMinY()

    def getW(self):
        return self.pts

    def getAirfoil(self):
        h = self.getH()
        w = self.pts
        airfoil = np.zeros((h, w), dtype=np.long)
        for i in range(h):
            for j in range(w):
                y_val = self.getMaxY()-i
                if self.lower_srf[j][1] <= y_val <= self.upper_srf[j][1]:
                    airfoil[i][j] = 1
        return airfoil

    @Qtc.pyqtSlot(str)
    def reset_params(self, string):
        values = string.split(sep='_')
        # print(values)
        # Reassign values
        self.pts = int(values[3])
        self.x = 1. / int(values[3])
        self.m = int(values[0]) / 100.
        self.p = int(values[1]) / 10.
        self.xx = int(values[2]) / 100.

        # Clean arrays
        self.xcgt = np.zeros((self.pts, 4))          # Contains x-Value, Camber, Gradient and Thickness
        self.upper_srf = np.zeros((self.pts, 2))     # Contains coordinates for upper surface
        self.lower_srf = np.zeros((self.pts, 2))     # Contains coordinates for lower surface

        # Calculate new Airfoil and emit
        self.calculate_airfoil()
        naca = self.getAirfoil()
        self.naca.emit(naca)


if __name__ == '__main__':
    a = Airfoil()
    b = a.getAirfoil()
    print(b.shape[0], b.shape[1])
    plt.imshow(b)
    plt.show()
