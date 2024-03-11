import sys
import serial
import datetime
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QTabWidget, QSizePolicy, QFormLayout, QLineEdit, QSpinBox
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SettingsTab(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.parameters = [("phttemp",    "Preheat temperature (\u00b0C)"),
                          ("phttime",    "Preheat time (s)"),
                          ("phtpwr",     "Preheat power (%)"),
                          ("soaktemp",   "Soak temperature (\u00b0C)"),
                          ("soaktime",   "Soak time (s)"),
                          ("soakpwr",    "Soak power (%)"),
                          ("reflowtemp", "Reflow temperature (\u00b0C)"),
                          ("reflowtime", "Reflow time (s)"),
                          ("reflowpwr",  "Soak power (%)"),
                          ("dwelltemp",  "Dwell temperature (\u00b0C)"),
                          ("dwelltime",  "Dwell time (s)"),
                          ("dwellpwr",   "Dwell power (%)")]
        self.spinboxes = {}

        self.layout = QVBoxLayout(self)

        self.setup_form()

        control_panel  = QWidget(self)
        control_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        control_layout = QHBoxLayout(control_panel)

        save_dev_bttn  = QPushButton("Save to device", control_panel)
        load_dev_bttn  = QPushButton("Load from device", control_panel)
        save_file_bttn = QPushButton("Save to file", control_panel)
        load_file_bttn = QPushButton("Load from file", control_panel)

        load_dev_bttn.clicked.connect(self.load_from_dev)
        save_dev_bttn.clicked.connect(self.save_to_dev)

        control_layout.addWidget(save_dev_bttn)
        control_layout.addWidget(load_dev_bttn)
        control_layout.addWidget(save_file_bttn)
        control_layout.addWidget(load_file_bttn)

        self.layout.addWidget(control_panel, 0)


    def setup_form(self):
        #form_widget = QWidget(self)
        #form_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        form = QFormLayout()

        for mnemonic, name in self.parameters:
            spinbox = QSpinBox()
            spinbox.setMinimum(0)
            spinbox.setMaximum(9999)
            spinbox.setSingleStep(1)
            form.addRow(QLabel(f"{name}"), spinbox)
            self.spinboxes[mnemonic] = spinbox

        self.layout.addLayout(form, 1)

    def load_from_dev(self):
        params = self.controller.get_parameters()

        for mnemonic, name in self.parameters:
            spinbox = self.spinboxes[mnemonic]
            spinbox.setValue(int(params[mnemonic]))

    def save_to_dev(self):
        for mnemonic, name in self.parameters:
            value = self.spinboxes[mnemonic].value()
            self.controller.set_parameter(mnemonic, value)

        self.load_from_dev()

        
#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    main = MainWindow()
#    main.show()
#    sys.exit(app.exec_())

