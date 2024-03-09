import sys
import serial
import datetime
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel
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
        self.axes.set_xlim([0, 600])
        self.axes.set_ylim([20, 180])
        self.axes.grid(True)
        self.axes.plot(x, y)
        self.draw()

    def clear(self):
        self.axes.clear()
        self.axes.set_xlim([0, 600])
        self.axes.set_ylim([20, 180])
        self.axes.grid(True)
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Live Temperature Graph')
        
        # Main widget and layout
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)

        self.graph = LiveGraph(main_widget, width=5, height=4)
        main_layout.addWidget(self.graph)

        # Control panel
        control_panel = QWidget(main_widget)
        control_layout = QHBoxLayout(control_panel)

        self.start_button = QPushButton("Start", control_panel)
        self.stop_button = QPushButton("Stop", control_panel)
        self.stop_button.setEnabled(False)
        self.status_label = QLabel("Stopped", control_panel)
        self.status_label.setStyleSheet("QLabel { border: 1px solid black; }")
        
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.status_label)
        main_layout.addWidget(control_panel)

        self.setCentralWidget(main_widget) 
        self.setWindowTitle('Live Temperature Graph')
        
        self.serial_port = serial.Serial(COM_PORT, 9600, timeout=1)
        self.timer = QTimer(self)

        # Connect buttons
        self.start_button.clicked.connect(self.start_reading)
        self.stop_button.clicked.connect(self.stop_reading)

        self.x_data = []
        self.y_data = []

    def start_reading(self):
        self.graph.clear()
        self.timer.setInterval(500)  # Adjust as needed
        self.timer.timeout.connect(self.update_graph)
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
                self.x_data.append(seconds)
                self.y_data.append(temperature)
                self.graph.plot(self.x_data, self.y_data)
            except:
                pass  # Handle non-numeric data gracefully

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

