import PyQt5.QtWidgets as Qtw
import PyQt5.QtCore as Qtc

from .gui_canvas import QCanvas
from .gui_thread import QThreadStep
from .gui_control import QControlPanel
from .fhp import FHP_Model
from .airfoil import Airfoil


class MainClassAsGUI(Qtw.QWidget):

    STANDARD_MESSAGE = 'You can now set up your model and calculate'

    def __init__(self):
        super().__init__()
        self.setWindowTitle('FHP Tunnel')

        # FHP Model
        self.model = FHP_Model()
        self.calculated_time_steps = 0
        self.running = False

        # Airfoil
        self.airfoil = Airfoil()
        self.model.insert_object(self.airfoil.getAirfoil())

        # WIDGETS
        self.control = QControlPanel()
        self.canvas = QCanvas(self.model.get_array(), self.model.get_walls())
        self.canvas.setFixedWidth(self.control.height()*3)

        # LAYOUT
        layout = Qtw.QGridLayout()
        layout.setAlignment(Qtc.Qt.AlignTop)
        layout.addWidget(self.control, 0, 0)
        layout.addWidget(self.canvas, 0, 1)
        self.setLayout(layout)

        # THREAD
        self.thread = QThreadStep()

        self.thread.threadFinished.connect(self.do_step)
        self.control.button_run_pause.clicked.connect(self.run_pause)
        self.control.button_reset.clicked.connect(self.reset)
        self.control.toggle.connect(self.model.setDisplayType)
        self.model.field_emit.connect(self.canvas.set_array)
        self.airfoil.naca.connect(self.model.insert_object)
        self.control.spinbox.connect(self.airfoil.reset_params)

        # SHOW
        self.show()

    @Qtc.pyqtSlot()
    def do_step(self):
        if self.running:
            self.calculated_time_steps += 1
            self.thread.start()

    def reset(self):
        self.running = False
        self.calculated_time_steps = 0
        self.model.setState(self.running)
        self.control.button_run_pause.setText('Run')
        self.control.frame_airfoil.setEnabled(True)
        # In addition reset to default airfoil and default field

    def run_pause(self):
        self.running = not self.running
        self.model.setState(self.running)
        if self.running:
            self.control.button_run_pause.setText('Pause')
            self.control.frame_airfoil.setDisabled(True)
            self.thread.set_model(self.model)
            self.do_step()
        if not self.running:
            self.control.button_run_pause.setText('Run')


if __name__ == "__main__":
    app = Qtw.QApplication([])
    gui = MainClassAsGUI()
    gui.show()
    app.exec_()

