import PyQt5.QtCore as Qtc
import PyQt5.QtWidgets as Qtw
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backend_bases import FigureCanvasBase


class QCanvas(FigureCanvas):
    def __init__(self, array, walls, parent=None):
        self.array = array
        self.walls = walls
        self.aspect = 3
        self.dpi = 100
        self.fig = Figure()
        self.fig.set_dpi(self.dpi)

        self.ax = self.fig.add_subplot()
        self.ax.set_position([0, 0, 1, 1])

        super(QCanvas, self).__init__(self.fig)
        self.setMinimumWidth(750)
        self.__sizing(self.width())
        self.plot()

    def __sizing(self, w):
        w_inch = w / self.dpi
        h_inch = w / (self.aspect * self.dpi)
        self.setFixedHeight(w/3)
        self.fig.set_size_inches(w_inch, h_inch, forward=False)

    def resizeEvent(self, event):
        w = event.size().width()
        self.__sizing(w)
        # pass back into Qt to let it finish
        Qtw.QWidget.resizeEvent(self, event)
        # emit our resize events
        FigureCanvasBase.resize_event(self)

    def plot(self):
        self.ax.clear()
        self.ax.axis('off')
        self.ax.imshow(self.array, cmap=plt.get_cmap('coolwarm'))
        data_masked = np.ma.masked_where(self.walls == 0, self.walls)
        self.ax.imshow(data_masked, cmap=plt.get_cmap('binary'), vmin = 0)
        self.draw()

    @Qtc.pyqtSlot(np.ndarray, np.ndarray)
    def set_array(self, array, walls):
        self.array = array
        self.walls = walls
        self.plot()
