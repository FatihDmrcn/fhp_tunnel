import PyQt5.QtWidgets as Qtw
import PyQt5.QtCore as Qtc


class ControlWidget(Qtw.QWidget):

    def __init__(self):
        super().__init__()

        # WIDGETS
        self.button_start_pause = Qtw.QPushButton('Start')
        self.button_reset = Qtw.QPushButton('Reset')

        self.radiobutton_display01 = Qtw.QRadioButton('Density')
        self.radiobutton_display02 = Qtw.QRadioButton('Vertical')
        self.radiobutton_display03 = Qtw.QRadioButton('Horizontal')

        self.spinbox_airfoil01 = Qtw.QSpinBox()
        self.spinbox_airfoil02 = Qtw.QSpinBox()
        self.spinbox_airfoil03 = Qtw.QSpinBox()
        self.spinbox_airfoil04 = Qtw.QSpinBox()

        # LAYOUT
        layout = Qtw.QGridLayout()
        layout.setAlignment(Qtc.Qt.AlignTop)
        layout.addWidget(self.button_start_pause, 0, 0)
        layout.addWidget(self.button_reset, 1, 0)
        layout.addWidget(self.radiobutton_display01, 2, 0)
        layout.addWidget(self.radiobutton_display02, 3, 0)
        layout.addWidget(self.radiobutton_display03, 4, 0)
        layout.addWidget(self.spinbox_airfoil01, 5, 0)
        layout.addWidget(self.spinbox_airfoil02, 6, 0)
        layout.addWidget(self.spinbox_airfoil03, 7, 0)
        layout.addWidget(self.spinbox_airfoil04, 8, 0)
        self.setLayout(layout)


if __name__ == "__main__":
    app = Qtw.QApplication([])
    gui = ControlWidget()
    gui.show()
    app.exec_()

