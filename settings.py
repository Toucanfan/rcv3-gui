import sys
import serial
import datetime
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QTabWidget, QSizePolicy, QFormLayout, QLineEdit, QSpinBox
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.setup_form()

        control_panel  = QWidget(self)
        control_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        control_layout = QHBoxLayout(control_panel)

        save_dev_bttn  = QPushButton("Save to device", control_panel)
        load_dev_bttn  = QPushButton("Load from device", control_panel)
        save_file_bttn = QPushButton("Save to file", control_panel)
        load_file_bttn = QPushButton("Load from file", control_panel)

        control_layout.addWidget(save_dev_bttn)
        control_layout.addWidget(load_dev_bttn)
        control_layout.addWidget(save_file_bttn)
        control_layout.addWidget(load_file_bttn)

        self.layout.addWidget(control_panel, 0)

    def setup_form(self):
        #form_widget = QWidget(self)
        #form_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        form = QFormLayout()

        parameters = [("Preheat temp", "degC"), 
                      ("Preheat time", "s"),
                      ("Soak temp", "degC"),
                      ("Soak time", "s"),
                      ("Reflow temp", "degC"),
                      ("Reflow time", "s")]

        for name, unit in parameters:
            spinbox = QSpinBox()
            spinbox.setMinimum(0)
            spinbox.setMaximum(9999)
            spinbox.setSingleStep(1)
            form.addRow(QLabel(f"{name} ({unit})"), spinbox)

        self.layout.addLayout(form, 1)

        
#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    main = MainWindow()
#    main.show()
#    sys.exit(app.exec_())

