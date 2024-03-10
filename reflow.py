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
    def __init__(self):
        super().__init__()
        
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

        self.serial_port = serial.Serial(COM_PORT, 9600, timeout=1)
        self.timer = QTimer(self)
        self.timer.setInterval(500)  # Adjust as needed
        self.timer.timeout.connect(self.update_graph)

        # Connect buttons
        self.start_button.clicked.connect(self.start_reading)
        self.stop_button.clicked.connect(self.stop_reading)

        self.x_data = []
        self.y_data = []

    def start_reading(self):
        self.graph.clear()
        self.serial_port.write("doStart\n".encode())
        self.status_label.setText("Started")
        self.stop_button.setEnabled(True)
        self.start_button.setEnabled(False)
        self.x_data = []
        self.y_data = []
        self.timer.start()

    def stop_reading(self):
        self.timer.stop()
        self.serial_port.write("doStop\n".encode())
        self.status_label.setText("Stopped")
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        
    def update_graph(self):
        line = self.serial_port.readline().decode('utf-8').strip()
        if line:
            try:
                columns = re.split(r',\s+', line)
                temperature = float(columns[2])
                seconds = int(columns[1])
                status = columns[0]
                print(f"{seconds} s: {temperature} degC")
                self.status_label.setText(status)
                self.temp_label.setText(f"{seconds} s: {temperature} C\u00b0")
                self.x_data.append(seconds)
                self.y_data.append(temperature)
                self.graph.plot(self.x_data, self.y_data)
            except:
                pass  # Handle non-numeric data gracefully

#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    main = MainWindow()
#    main.show()
#    sys.exit(app.exec_())

