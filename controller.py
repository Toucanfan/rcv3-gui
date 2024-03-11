import sys
import serial
import datetime
import re
from time import sleep
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QTabWidget
from PyQt5.QtCore import QTimer, QObject

from reflow import ReflowTab
from settings import SettingsTab

class ReflowController(QObject):
    def __init__(self):
        super().__init__()
        self.state = "stopped"
        self.serial_port_path = "/dev/ttyUSB0"
        self.serial_port_baud = 9600
        self.serial = serial.Serial(self.serial_port_path,
                                    self.serial_port_baud, 
                                    timeout=1)

        self.timer = QTimer(self)
        self.timer.setInterval(500)  # Adjust as needed
        self.timer.timeout.connect(self._handle_timer)

        self.callback = None

    def _writeline(self, line: str):
        self.serial.write((line + '\n').encode("ascii"))
        sleep(0.1)
        self.serial.read(len(line)+1)

    def _readline(self) -> str:
        return self.serial.readline().decode("ascii").strip()
        
    def _run_cmd(self, cmd, waittime=0.1):
        self._writeline(cmd)
        sleep(waittime)
        return self.serial.read_all().decode("ascii").strip()

    def _handle_timer(self):
        line = self._readline()
        if line:
            try:
                state, time, temp, _ = re.split(r',\s+', line)
                self.callback(state, int(time), int(temp))
            except:
                pass

    def get_temp(self):
        return int(self._run_cmd("tempshow").split(' ')[1])

    def get_parameters(self):
        r = self._run_cmd("showall", waittime=1)
        lines = r.split('\r\n')
        params = {}
        for line in lines:
            columns = re.split(r'\s+', line)
            key = columns[0]
            value = columns[1]
            value = value.replace("Sekunden", "").replace("%", "")
            params[key] = value
        return params

    def set_parameter(self, param, val):
        self._run_cmd(f"{param} {str(val)}")

    def start(self, callback):
        self.callback = callback
        self._run_cmd("tempshow 1")
        self._run_cmd("doStart")
        self.timer.start()

    def stop(self):
        self.timer.stop()
        self.serial.read_all()
        self._run_cmd("doStop")

