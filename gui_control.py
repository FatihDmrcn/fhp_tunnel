import PyQt5.QtWidgets as Qtw
import PyQt5.QtCore as Qtc


class ControlWidget(Qtw.QWidget):

    def __init__(self):
        super().__init__()

        # WIDGETS
        # Main control buttons
        self.button_run_pause = Qtw.QPushButton('Run')
        self.button_reset = Qtw.QPushButton('Reset')

        # Radiobuttons for display type
        self.frame_display = Qtw.QFrame()
        self.radiobutton_dens = Qtw.QRadioButton('Density')
        self.radiobutton_dens.setChecked(True)
        self.radiobutton_horz = Qtw.QRadioButton('Horizontal')
        self.radiobutton_vert = Qtw.QRadioButton('Vertical')
        layout_display = Qtw.QVBoxLayout()
        layout_display.addWidget(self.radiobutton_dens)
        layout_display.addWidget(self.radiobutton_horz)
        layout_display.addWidget(self.radiobutton_vert)
        self.frame_display.setLayout(layout_display)

        # Spinboxes for airfoil design
        self.frame_airfoil = Qtw.QFrame()
        self.label_m = Qtw.QLabel('Max. Camber [M]')
        self.spinbox_m = Qtw.QSpinBox()
        self.spinbox_m.setRange(0, 9)
        self.label_p = Qtw.QLabel('Position [P]')
        self.spinbox_p = Qtw.QSpinBox()
        self.spinbox_p.setRange(0, 90)
        self.label_xx = Qtw.QLabel('Thickness [XX]')
        self.spinbox_xx = Qtw.QSpinBox()
        self.spinbox_xx.setRange(1, 40)
        self.label_l = Qtw.QLabel('Length [L]')
        self.spinbox_l = Qtw.QSpinBox()
        self.spinbox_l.setRange(150, 450)

        layout_airfoil = Qtw.QGridLayout()
        layout_airfoil.addWidget(self.label_m, 0, 0)
        layout_airfoil.addWidget(self.spinbox_m, 0, 1)
        layout_airfoil.addWidget(self.label_p, 1, 0)
        layout_airfoil.addWidget(self.spinbox_p, 1, 1)
        layout_airfoil.addWidget(self.label_xx, 2, 0)
        layout_airfoil.addWidget(self.spinbox_xx, 2, 1)
        layout_airfoil.addWidget(self.label_l, 3, 0)
        layout_airfoil.addWidget(self.spinbox_l, 3, 1)
        self.frame_airfoil.setLayout(layout_airfoil)

        # LAYOUT
        layout = Qtw.QVBoxLayout()
        layout.setAlignment(Qtc.Qt.AlignTop)
        layout.addWidget(self.button_run_pause)
        layout.addWidget(self.button_reset)
        layout.addWidget(self.frame_display)
        layout.addWidget(self.frame_airfoil)
        self.setLayout(layout)


if __name__ == "__main__":
    app = Qtw.QApplication([])
    gui = ControlWidget()
    gui.show()
    app.exec_()

