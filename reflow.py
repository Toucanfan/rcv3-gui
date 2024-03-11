import sys
import serial
import datetime
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QSizePolicy
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

COM_PORT = "/dev/ttyUSB0"

class LiveGraph(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(LiveGraph, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title('Temperature vs Time')
        self.clear()
        
    def plot(self, x, y):
        self.axes.clear()
        xmax = (int(max(x)/100) + 1)*100
        ymax = (int(max(y)/100) + 1)*100
        self.axes.set_xlim([0, xmax])
        self.axes.set_ylim([0, ymax])
        self.axes.grid(True)
        self.axes.plot(x, y)
        self.draw()

    def clear(self):
        self.axes.clear()
        self.axes.set_xlim([0, 100])
        self.axes.set_ylim([0, 100])
        self.axes.grid(True)
        self.draw()

class ReflowTab(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        
        # Main widget and layout
        layout = QVBoxLayout(self)

        self.graph = LiveGraph(self, width=5, height=4)
        layout.addWidget(self.graph, 1)

        # Control panel
        control_panel = QWidget(self)
        control_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        control_layout = QHBoxLayout(control_panel)

        self.start_button = QPushButton("Start", control_panel)

        self.stop_button = QPushButton("Stop", control_panel)
        self.stop_button.setEnabled(False)

        self.status_label = QLabel("Stopped", control_panel)
        self.status_label.setStyleSheet("QLabel { border: 1px solid black; }")

        self.temp_label = QLabel("---", control_panel)
        self.temp_label.setStyleSheet("QLabel { border: 1px solid black; }")
        
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.status_label)
        control_layout.addWidget(self.temp_label)
        layout.addWidget(control_panel, 0)

        # Connect buttons
        self.start_button.clicked.connect(self.start_reading)
        self.stop_button.clicked.connect(self.stop_reading)

        self.x_data = []
        self.y_data = []

    def start_reading(self):
        self.graph.clear()
        self.controller.start(self.update_graph)
        self.stop_button.setEnabled(True)
        self.start_button.setEnabled(False)
        self.x_data = []
        self.y_data = []

    def stop_reading(self):
        self.controller.stop()
        self.status_label.setText("Stopped")
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        
    def update_graph(self, state, time, temp):
        print(f"{time} s: {temp} \u00b0C")
        self.status_label.setText(state)
        self.temp_label.setText(f"{time} s: {temp} \u00b0C")
        self.x_data.append(time)
        self.y_data.append(temp)
        self.graph.plot(self.x_data, self.y_data)

#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    main = MainWindow()
#    main.show()
#    sys.exit(app.exec_())

