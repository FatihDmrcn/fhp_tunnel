import PyQt5.QtWidgets as Qtw
from src.gui_main import MainClassAsGUI

if __name__ == "__main__":
    app = Qtw.QApplication([])
    gui = MainClassAsGUI()
    gui.show()
    app.exec_()
