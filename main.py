#!/usr/bin/env python3

import sys
import serial
import datetime
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QTabWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from reflow import ReflowTab
from settings import SettingsTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Reflow controller')

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget) 

        reflow_tab = ReflowTab()
        self.tab_widget.addTab(reflow_tab, "Reflow")

        self.settings_tab = SettingsTab()
        self.tab_widget.addTab(self.settings_tab, "Settings")

        reflow_tab.start_button.clicked.connect(self.deactivate_settings_tab)
        reflow_tab.stop_button.clicked.connect(self.activate_settings_tab)

    def deactivate_settings_tab(self):
        self.settings_tab.setEnabled(False)

    def activate_settings_tab(self):
        self.settings_tab.setEnabled(True)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

