import PyQt5.QtCore as Qtc


class QThreadStep(Qtc.QThread):

    threadFinished = Qtc.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.model = None

    def set_model(self, model):
        self.model = model

    def run(self):
        self.model.do_step()
        self.threadFinished.emit()
