import PyQt5.QtWidgets as Qtw
import PyQt5.QtCore as Qtc


class QControlPanel(Qtw.QWidget):

    toggle = Qtc.pyqtSignal(str)
    spinbox = Qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setSizePolicy(Qtw.QSizePolicy.Fixed, Qtw.QSizePolicy.Fixed)

        # WIDGETS
        # Main control buttons
        self.button_run_pause = Qtw.QPushButton('Run')
        self.button_reset = Qtw.QPushButton('Reset')

        # Radiobuttons for display type
        self.frame_display = Qtw.QFrame()
        self.rbtn_dens = Qtw.QRadioButton('Density')
        self.rbtn_dens.toggled.connect(self.rbtn_toggled)
        self.rbtn_horz = Qtw.QRadioButton('Horizontal')
        self.rbtn_horz.toggled.connect(self.rbtn_toggled)
        self.rbtn_vert = Qtw.QRadioButton('Vertical')
        self.rbtn_vert.toggled.connect(self.rbtn_toggled)
        self.rbtn_horz.setChecked(True)
        layout_display = Qtw.QVBoxLayout()
        layout_display.addWidget(self.rbtn_dens)
        layout_display.addWidget(self.rbtn_horz)
        layout_display.addWidget(self.rbtn_vert)
        self.frame_display.setLayout(layout_display)

        # Spinboxes for airfoil design
        self.frame_airfoil = Qtw.QFrame()
        self.label_m = Qtw.QLabel('Max. Camber [M]')
        self.spinbox_m = Qtw.QSpinBox()
        self.spinbox_m.setRange(0, 9)
        self.spinbox_m.setValue(2)
        self.spinbox_m.valueChanged.connect(self.spnb_changed)
        self.label_p = Qtw.QLabel('Position [P]')
        self.spinbox_p = Qtw.QSpinBox()
        self.spinbox_p.setRange(0, 90)
        self.spinbox_p.setValue(4)
        self.spinbox_p.valueChanged.connect(self.spnb_changed)
        self.label_xx = Qtw.QLabel('Thickness [XX]')
        self.spinbox_xx = Qtw.QSpinBox()
        self.spinbox_xx.setRange(1, 40)
        self.spinbox_xx.setValue(12)
        self.spinbox_xx.valueChanged.connect(self.spnb_changed)
        self.label_l = Qtw.QLabel('Length [L]')
        self.spinbox_l = Qtw.QSpinBox()
        self.spinbox_l.setRange(150, 450)
        self.spinbox_l.setValue(200)
        self.spinbox_l.valueChanged.connect(self.spnb_changed)

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

    def spnb_changed(self):
        string = '{}_{}_{}_{}'.format(self.spinbox_m.text(),
                                      self.spinbox_p.text(),
                                      self.spinbox_xx.text(),
                                      self.spinbox_l.text())
        #print(string)
        self.spinbox.emit(string)

    def rbtn_toggled(self):
        rbtn = self.sender()
        if rbtn.isChecked():
            # print(rbtn.text())
            self.toggle.emit(rbtn.text())


if __name__ == "__main__":
    app = Qtw.QApplication([])
    gui = QControlPanel()
    gui.show()
    app.exec_()

