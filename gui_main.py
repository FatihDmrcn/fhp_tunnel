import PyQt5.QtWidgets as Qtw
import PyQt5.QtCore as Qtc
import fhp_main
import gui_canvas
import gui_thread

class MainClassAsGUI(Qtw.QWidget):

    STANDARD_MESSAGE = 'You can now set up your model and calculate'

    def __init__(self):
        super().__init__()
        self.setWindowTitle('FHP Tunnel')

        self.model = fhp_main.FHP_Model()
        # MENU
        self.canvas = gui_canvas.QCanvas()
        #self.canvas.setSizePolicy(Qtw.QSizePolicy.Fixed, Qtw.QSizePolicy.Fixed)
        self.menu = Qtw.QFrame()
        self.menu.setSizePolicy(Qtw.QSizePolicy.Fixed, Qtw.QSizePolicy.Expanding)
        self.button = Qtw.QPushButton('Start Simulation')
        self.button.clicked.connect(self.do_sim)

        layout = Qtw.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.thread = gui_thread.QThreadStep()
        self.model.time_step.connect(self.canvas.set_array)
        self.thread.threadFinished.connect(self.do_step)

        self.time_steps = 300
        self.index = 0
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

