import PyQt5.QtWidgets as Qtw
import PyQt5.QtCore as Qtc
import PyQt5.QtGui as Qtg
import numpy as np

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar


class QCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(9,3))
        self.ax = fig.add_subplot()
        super(QCanvas, self).__init__(fig)
        self.array = None

    def plot(self):
        self.ax.clear()
        self.ax.imshow(self.array)
        self.draw()

    @Qtc.pyqtSlot(np.ndarray)
    def set_array(self, array):
        self.array = array
        self.plot()
