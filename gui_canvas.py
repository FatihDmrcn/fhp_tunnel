import PyQt5.QtCore as Qtc
import PyQt5.QtWidgets as Qtw
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backend_bases import FigureCanvasBase


class QCanvas(FigureCanvas):
    def __init__(self, array, parent=None):
        self.array = array
        self.aspect = 3
        self.dpi = 100
        self.fig = Figure()

        self.ax = self.fig.add_subplot()
        self.ax.set_position([0, 0, 1, 1])

        super(QCanvas, self).__init__(self.fig)
        self.plot()

    def resizeEvent(self, event):
        w = event.size().width()
        winch = w / self.dpi
        hinch = w / (self.aspect*self.dpi)
        self.setFixedHeight(w/3)
        self.fig.set_size_inches(winch, hinch, forward=False)
        self.fig.set_dpi(self.dpi)
        # pass back into Qt to let it finish
        Qtw.QWidget.resizeEvent(self, event)
        # emit our resize events
        FigureCanvasBase.resize_event(self)

    def plot(self):
        self.ax.clear()
        self.ax.axis('off')
        self.ax.imshow(self.array)
        self.draw()

    @Qtc.pyqtSlot(np.ndarray)
    def set_array(self, array):
        self.array = array
        self.plot()
