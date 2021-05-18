import PyQt5.QtWidgets as Qtw
import PyQt5.QtCore as Qtc

from gui_canvas import QCanvas
from gui_thread import QThreadStep
from fhp import FHP_Model
from airfoil import Airfoil


class MainClassAsGUI(Qtw.QWidget):

    STANDARD_MESSAGE = 'You can now set up your model and calculate'

    def __init__(self):
        super().__init__()
        self.setWindowTitle('FHP Tunnel')

        # FHP Model
        self.model = FHP_Model()
        self.time_steps = 300
        self.index = 0

        # Airfoil
        self.airfoil = Airfoil()
        self.model.insert_object(self.airfoil.getAirfoil())

        # WIDGETS
        self.canvas = QCanvas(self.model.get_array())
        self.button = Qtw.QPushButton('Start Simulation')
        self.button.setSizePolicy(Qtw.QSizePolicy.MinimumExpanding, Qtw.QSizePolicy.Fixed)
        self.button.clicked.connect(self.do_sim)

        # LAYOUT
        layout = Qtw.QGridLayout()
        layout.setAlignment(Qtc.Qt.AlignTop)
        layout.addWidget(self.canvas, 0, 0)
        layout.addWidget(self.button, 1, 0)
        self.setLayout(layout)

        # THREAD
        self.thread = QThreadStep()
        self.model.time_step.connect(self.canvas.set_array)
        self.thread.threadFinished.connect(self.do_step)

        # SHOW
        self.show()

    @Qtc.pyqtSlot()
    def do_step(self):
        if self.index<self.time_steps:
            self.index += 1
            self.thread.start()

    def do_sim(self):
        self.thread.set_model(self.model)
        self.index = 0
        self.do_step()


if __name__ == "__main__":
    app = Qtw.QApplication([])
    gui = MainClassAsGUI()
    gui.show()
    app.exec_()

